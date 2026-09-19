# Changelog

## v1.0.0 — 2026-09-20

- Added implementation checklist, KPI definitions, procurement template, and RQ traceability.
- Added current Namal HPC contextual profile using operator-confirmed RTX 4070 Ti / 40-GPU / 5-TB-RAM / low-latency-network values.
- Added publication-safe Slurm examples derived from the supplied training package.
- Added OpenMP, MPI, CUDA SM 8.9, and PyTorch distributed smoke-test code.
- Added checkpoint/requeue distributed-training example.
- Removed the core dependency on pandas/openpyxl; numerical reproduction now uses the Python standard library.
- Added unit tests and package validation, including a scan for internal addressing/hostnames in public examples.
- Expanded the supplemental workbook and release documentation.
