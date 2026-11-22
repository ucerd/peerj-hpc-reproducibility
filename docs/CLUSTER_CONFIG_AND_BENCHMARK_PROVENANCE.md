# Cluster configuration and benchmark provenance (release verification)

## Separate the evidence classes

**Source 1: public PakSupercomputer paper.** `https://pakhpc.com/PakSupercomputer_Paper.pdf` is a publicly accessible paper titled *PakSupercomputer: An Open-Source, Scalable, and Heterogeneous Supercomputing Platform*. Namal University's faculty listing identifies a 2025 conference publication with that title. Its PDF is not an automatically interchangeable description of the newer paper.

**Source 2: newer, supplied 18-page technical manuscript.** *PakSupercomputer: Design and Development of a COTS-Based Heterogeneous CPU–GPU–FPGA HPC Cluster* reports 20 Dell Precision 7820 compute nodes, 800 physical Intel CPU cores (1,600 hardware threads), 40 RTX 4090 GPUs, 20 Tang Mega FPGA boards, 5 TB RAM, 40 TB local NVMe in total, Lustre shared filesystem, 10 GbE switching, Rocky Linux 9.4, Slurm and monitoring. **Publisher publication/acceptance status is not independently verified.** It reports (p.13, Table 9) a 32.180 s one-node baseline and 4.023 s on 20 nodes, giving approximately 8.00x speedup and 40% efficiency, with approximately 45% communication overhead. These are **source-reported measurements**; raw benchmark logs, full run metadata and replicate-level values were not supplied with this repository. Its Data and Code Availability section explicitly says the `ucerd/MARS-Slurm` repository does **not** contain all raw logs, power traces or FPGA reports.

**Source 3: prior PeerJ Git package profile (2026-09-20).** The uploaded repo recorded 20 nodes, 1,600 'cores', 40 RTX 4070 Ti GPUs and an unspecified 'low-latency switched cluster fabric'. This conflicts with the COTS manuscript on GPU model, 800 physical cores vs. 1,600 threads, and declared network speed. The profiles may concern different versions/phases, but no dated hardware inventory was provided that establishes that conclusion. **Neither source is silently selected as the unique current configuration.** See `data/cluster_configuration_sources.csv`.

## What this package reproducibly establishes

1. Pure-Python reproduction of the PeerJ framework's assumed CPU/GPU capacity calculations (manuscript Table 3 and hypothetical scenario).
2. Input-driven example of allocated job CPU-core/GPU-hours (not measured telemetry).
3. Reproduction of an illustrative storage sum (70 TB active, 35 TB persistent, 25 TB archive) from explicit *author-assumed*, nonempirical component data.
4. Arithmetic checks on the strong-scaling values transcribed from the supplied technical manuscript. These checks **do not rerun the computational workloads** or verify underlying source logs.
5. A publication-safe Slurm example collection, not production deployment playbooks.

## Next evidence needed for stronger assertions

- A dated, de-identified hardware inventory naming the target deployment, CPU physical cores vs. threads, GPU model, network bandwidth, and change history.
- Exact benchmark source repository URL/commit; raw run logs, parameter inputs, software/driver versions, repetition counts, timestamps and checksums.
- Dated cross-institutional acceptance/commissioning notes for Malakand, PAF-IAST and GIKI; permitted BIŌN consultancy summary.
- Independent evaluation of *this design framework* by third-party HPC practitioners or a genuinely held-out case, with prespecified rubric and retained responses.
- Historical search/coding log for 35 references or an explicitly retrospective audit with source anchors.
