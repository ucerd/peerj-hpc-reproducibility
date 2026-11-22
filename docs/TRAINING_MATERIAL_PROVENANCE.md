# Training-material provenance

The user supplied `3_Trainings_Learning.zip` as supporting implementation
material. Relevant sections cover Slurm job submission, resource requests,
multi-node execution, PyTorch distributed launch, NCCL/Gloo setup, monitoring,
troubleshooting, and checkpoint/requeue patterns.

The public examples in this repository are **rewritten engineering examples**,
not verbatim copies of the training scripts.

Publication-safety changes include:

- removal of private IP addresses;
- removal of production node names;
- removal of per-node NIC/interface mappings;
- removal of forced communication settings that may be wrong on another fabric;
- correction of incomplete shell quoting in a multi-node GPU example;
- robust Slurm-derived rank/world-size handling for PyTorch;
- job-derived rendezvous ports instead of one fixed port;
- use of `srun --kill-on-bad-exit=1` for distributed failure propagation;
- explicit checkpoint/signal behavior for requeue-capable training;
- CUDA `sm_89` build target for the the RTX 4070 Ti training example (the independently supplied later cluster manuscript reports RTX 4090 devices).

See `data/training_source_index.csv` for the source-to-public-artifact mapping.
