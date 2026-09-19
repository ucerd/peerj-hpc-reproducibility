"""Minimal Slurm-aware PyTorch distributed smoke test."""

from __future__ import annotations

import os
import socket
import torch
import torch.distributed as dist


def slurm_env() -> tuple[int, int, int]:
    try:
        rank = int(os.environ["SLURM_PROCID"])
        world = int(os.environ["SLURM_NTASKS"])
        local = int(os.environ["SLURM_LOCALID"])
    except KeyError as exc:
        raise RuntimeError("This example is intended to run inside a Slurm allocation.") from exc
    return rank, world, local


def main() -> None:
    rank, world, local_rank = slurm_env()
    os.environ["RANK"] = str(rank)
    os.environ["WORLD_SIZE"] = str(world)

    use_cuda = torch.cuda.is_available()
    backend = "nccl" if use_cuda else "gloo"

    if use_cuda:
        if local_rank >= torch.cuda.device_count():
            raise RuntimeError(
                f"SLURM_LOCALID={local_rank}, but only {torch.cuda.device_count()} GPUs are visible"
            )
        torch.cuda.set_device(local_rank)
        device = torch.device("cuda", local_rank)
    else:
        device = torch.device("cpu")

    dist.init_process_group(backend=backend, init_method="env://")

    value = torch.tensor([float(rank + 1)], device=device)
    dist.all_reduce(value, op=dist.ReduceOp.SUM)
    expected = world * (world + 1) / 2

    print(
        f"host={socket.gethostname()} rank={rank}/{world} local_rank={local_rank} "
        f"backend={backend} reduced={value.item()} expected={expected}",
        flush=True,
    )

    if abs(value.item() - expected) > 1e-5:
        raise RuntimeError("Distributed all-reduce validation failed")

    dist.barrier()
    dist.destroy_process_group()


if __name__ == "__main__":
    main()
