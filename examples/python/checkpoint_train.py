"""Small Slurm-aware DDP training example with checkpoint-on-signal behavior."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import sys

import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP


checkpoint_requested = False


def on_usr1(signum, frame):
    global checkpoint_requested
    checkpoint_requested = True


def main() -> None:
    signal.signal(signal.SIGUSR1, on_usr1)

    rank = int(os.environ["SLURM_PROCID"])
    world = int(os.environ["SLURM_NTASKS"])
    local_rank = int(os.environ["SLURM_LOCALID"])
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world)

    if not torch.cuda.is_available():
        raise RuntimeError("GPU/CUDA is required for this example")
    torch.cuda.set_device(local_rank)
    device = torch.device("cuda", local_rank)

    dist.init_process_group("nccl", init_method="env://")

    model = torch.nn.Linear(128, 16).to(device)
    ddp = DDP(model, device_ids=[local_rank])
    optim = torch.optim.AdamW(ddp.parameters(), lr=1e-3)

    ckpt_dir = Path(os.environ.get("CHECKPOINT_DIR", "checkpoints"))
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    ckpt = ckpt_dir / "state.pt"

    start_epoch = 0
    if ckpt.exists():
        state = torch.load(ckpt, map_location=device)
        ddp.module.load_state_dict(state["model"])
        optim.load_state_dict(state["optimizer"])
        start_epoch = int(state["epoch"]) + 1

    for epoch in range(start_epoch, 1000):
        x = torch.randn(128, 128, device=device)
        target = torch.randn(128, 16, device=device)
        optim.zero_grad(set_to_none=True)
        loss = torch.nn.functional.mse_loss(ddp(x), target)
        loss.backward()
        optim.step()

        if rank == 0 and epoch % 10 == 0:
            print(f"epoch={epoch} loss={loss.item():.6f}", flush=True)

        if checkpoint_requested:
            if rank == 0:
                torch.save(
                    {"epoch": epoch, "model": ddp.module.state_dict(), "optimizer": optim.state_dict()},
                    ckpt,
                )
                print(f"checkpoint_saved={ckpt}", flush=True)
            dist.barrier()
            dist.destroy_process_group()
            # Non-zero tells the scheduler/site policy that the run ended early;
            # the allocation itself is marked requeue-capable.
            raise SystemExit(99)

    if rank == 0:
        torch.save(
            {"epoch": 999, "model": ddp.module.state_dict(), "optimizer": optim.state_dict()},
            ckpt,
        )
    dist.barrier()
    dist.destroy_process_group()


if __name__ == "__main__":
    main()
