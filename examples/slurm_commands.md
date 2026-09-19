# Slurm quick reference

```bash
# Submit
sbatch examples/slurm/00_cpu_single_node.sbatch

# Queue and allocation state
squeue -u "$USER"
sinfo -s
scontrol show job <JOBID>
scontrol show nodes

# Accounting after/during execution
sacct -j <JOBID> --format=JobID,JobName,State,Elapsed,AllocCPUS,ReqMem,MaxRSS

# Cancel
scancel <JOBID>

# Follow logs
tail -f logs/<job-name>_<jobid>.out
```

Resource requests should be explicit and proportionate to the workload. For
course or interactive service, use the locally approved partition/QoS rather
than hard-coding a production partition in public examples.
