# HPC / Slurm implementation examples

These examples are derived from the supplied CAID training material and rewritten
for public release. They are **templates**, not production configuration files.

Important:
- Adjust partition/QoS names to the local cluster policy.
- Site-specific module names may differ.
- No internal IP addresses, node names, NIC names, credentials, or production
  scheduler configuration are included.
- The original September repository profile reports 40 RTX 4070 Ti GPUs, whereas a later COTS paper reports 40 RTX 4090 GPUs; do not assume they are the same verified hardware configuration.
- The CUDA compile example targets `sm_89`, illustrative Ada target; actual installed GPU/driver requires checking.

Submit from the repository root. Scheduler logs are written to the submission directory. Multi-node GPU examples require site-specific GPU binding, a shared checkpoint directory, functioning NCCL and a compatible Slurm signal/requeue policy. Exit 99 does not automatically requeue; checkpoints are demonstration state, not bitwise deterministic restart. These examples were syntax-checked only, not executed on a cluster for this release.
