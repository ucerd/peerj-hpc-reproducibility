# HPC / Slurm implementation examples

These examples are derived from the supplied CAID training material and rewritten
for public release. They are **templates**, not production configuration files.

Important:
- Adjust partition/QoS names to the local cluster policy.
- Site-specific module names may differ.
- No internal IP addresses, node names, NIC names, credentials, or production
  scheduler configuration are included.
- The current Namal context for this release is 40 NVIDIA RTX 4070 Ti GPUs,
  5 TB aggregate RAM, and a low-latency switched cluster fabric.
- The CUDA compile example targets `sm_89`, appropriate for RTX 4070 Ti (Ada).
