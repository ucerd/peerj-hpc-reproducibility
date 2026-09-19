# Implementation guide

This guide converts the design framework into an implementation sequence.

## Phase 1 — Institutional readiness

1. Inventory teaching, research, AI, simulation, and external-project workloads.
2. Quantify monthly CPU core-hours and GPU-hours.
3. Classify data and retention requirements.
4. Assess power, cooling, rack, networking, physical security, and staffing.
5. Define initial governance, service ownership, and budget/refresh mechanism.

**Gate:** do not finalize hardware until workload, facilities, governance, and
staffing requirements are documented.

## Phase 2 — Minimum viable platform

A minimum viable shared service normally includes:

- login/management services;
- Slurm controller/accounting;
- CPU/GPU compute resources;
- managed identity/access;
- container support;
- high-performance scratch plus persistent project storage;
- monitoring and accounting;
- documented user onboarding;
- at least one beginner-friendly access path where appropriate.

## Phase 3 — Teaching and research integration

- Create teaching/research partitions or QoS classes.
- Protect scheduled course windows when needed.
- Publish resource limits and fair-use rules.
- Provide versioned software/module/container environments.
- Teach scratch vs persistent-storage behavior.
- Measure queue wait, GPU utilization, availability, and support demand.

## Phase 4 — External-service enablement

Before external or industry projects are admitted:

- define project owner and data owner;
- approve access and data-use terms;
- create isolated workspaces;
- define retention/deletion rules;
- define charging/recharge or sponsorship treatment;
- define an exit/sunset process.

## Phase 5 — Scale-out and sustainability

Scale compute/storage/staffing using measured utilization and queue telemetry,
not hardware-only targets. Maintain lifecycle plans for CPUs, GPUs, storage,
networking, and software separately.

## Slurm implementation pattern

The public examples in `examples/slurm/` demonstrate:

- single-node CPU allocation;
- multi-node launch with `srun`;
- OpenMP placement;
- MPI launch;
- single-node and multi-node GPU allocation;
- single-GPU PyTorch;
- PyTorch distributed/NCCL rendezvous;
- signal/checkpoint/requeue workflow;
- RTX 4070 Ti CUDA compilation (`sm_89`).

### Submission and monitoring

```bash
sbatch examples/slurm/00_cpu_single_node.sbatch
squeue -u "$USER"
scontrol show job <JOBID>
sacct -j <JOBID> --format=JobID,JobName,State,Elapsed,AllocCPUS,ReqMem,MaxRSS
scancel <JOBID>
```

### Engineering rules for public/reusable job scripts

1. Never hard-code private IP addresses, production node names, or NIC names.
2. Obtain the rendezvous host from `$SLURM_JOB_NODELIST`.
3. Derive or configure a collision-resistant rendezvous port.
4. Request only the GPUs/CPUs/memory the workload needs.
5. Set a finite time limit.
6. Write stdout/stderr to predictable log paths.
7. For distributed training, fail the allocation if one rank fails.
8. Use checkpoints for long-running/preemptible jobs.
9. Keep site-specific partition/QoS/module names outside reusable code when possible.
10. Use scheduler accounting and GPU telemetry to validate scaling decisions.
