# University Supercomputing Design Framework — Reproducibility Release

**Version 1.2.0 — 22 November 2026**

This repository accompanies the PeerJ Computer Science revision *Implementing Supercomputing Infrastructure for Third-Generation Universities: A Design Framework for Education, Research, and Innovation* (T. Hussain, M. N. U. Islam, A. Haider, S. Alharbi and T. K. Geok).

## What can be reproduced

- CPU and GPU node counts for **manuscript Table 3**: Entry **3/1**, Intermediate **11/6**, Advanced **28/21**, with scenario **12/8** under stated *hypothetical demand* and capacity assumptions.
- A transparent example of job-level allocated resource hours, using explicit **hypothetical job records**, not CAID Slurm telemetry.
- Author-assumed, component-level storage sums: **70 TB active, 35 TB persistent, 25 TB archive**; these do not empirically justify the Table 3 storage and staffing envelopes.
- Arithmetic consistency of six strong-scaling rows transcribed from the **separately supplied** PakSupercomputer COTS technical manuscript (32.180 s at 1 node; 4.023 s at 20 nodes, ~8× speedup). **This is not a benchmark rerun; original machine logs are not supplied.**
- Sanitized, generic HPC/Slurm, CUDA, OpenMP, MPI and PyTorch examples. These are **not** a deployable, production-exact Namal system image.

## How to verify the release

From an extracted copy of the ZIP or repository root (Python 3.10+; core scripts require standard library only):

```bash
python code/validate_package.py
python code/reproduce_results.py
python -m unittest discover -s tests -v
python code/check_source_benchmark_arithmetic.py
```

Expected node-count results: Entry 3 CPU/1 GPU, Intermediate 11/6, Advanced 28/21, illustrative scenario 12/8. `code/validate_package.py` checks `CITATION.cff` at the package root, the exact file inventory and digests, source records, source-specific hardware discrepancies, archived numerical outputs and a limited publication-safety scan. CI runs the numerical tests and checks Slurm shell syntax. GPU/MPI/Slurm runtime validation is not included.

## Source distinctions and research status

- **Prior publicly available paper:** *PakSupercomputer: An Open-Source, Scalable, and Heterogeneous Supercomputing Platform*: https://pakhpc.com/PakSupercomputer_Paper.pdf ; a 2025 conference paper is listed on Namal's faculty page. A DOI was not established for this release.
- **Later supplied technical manuscript:** *PakSupercomputer: Design and Development of a COTS-Based Heterogeneous CPU–GPU–FPGA HPC Cluster* (T. Hussain, S. Alharbi, S. Khalid), 18 pages. Its publisher acceptance/publication status is **unverified**. Table 9 contains the strong-scaling numbers transcribed here. Its Data/Code Availability section says `https://github.com/ucerd/MARS-Slurm` is related software, **not** the full raw experimental archive.
- **Hardware discrepancies:** The earlier Git package calls the cluster 40× RTX 4070 Ti / '1,600 cores' / an unspecified low-latency fabric. The supplied later technical manuscript specifies 40× RTX 4090 / 800 physical cores (1,600 threads) / **10 GbE**. These records are preserved separately; no dated equipment audit was supplied to establish whether they reflect revisions or distinct deployments. See `docs/CLUSTER_CONFIG_AND_BENCHMARK_PROVENANCE.md`.
- **Institutional support:** Authors report support to University of Malakand, GIKI, and PAF-IAST, and advisory activity for BIŌN Technologies (KSA). Consortium participation is separately documented; partner go-live and consultancy completion **require external confirmation**. See `data/partner_service_claims.csv`.

### Scientific scope

This is a **design-science framework with internally validated calculations and a hypothetical scenario**, not an independently evaluated field deployment of the proposed university-wide governance method. The original 35-source/25-requirement extraction log is preserved, but missing historic platform/coder logs are **not invented**. `docs/EVALUATION_BOUNDARIES.md` identifies unresolved evidence and limitations.

### CAID institutional context (2023–22 November 2026)

A publication-safe aggregate dashboard and machine-readable register document provisional management-reported figures: 500 completed projects, 50 PoCs, 20 MVPs, six CVPs, 200 hours per user on average, and approximately 100 potential industry links. The source workbook describes 20 MVP candidates and six pre-CVP offerings, so finalization requires reconciliation. The additional reported quantity exceeding 20,000 has no defined unit and is excluded from substantive interpretation. These are not raw scheduler records, independently verified achievements, confirmed industrial partnerships, or evidence of independent artifact evaluation. Counts may overlap; no funnel, conversion rate or annual trend is inferred. See `docs/CAID_DASHBOARD_NOTES.md` and `data/caid_management_metrics.csv`.

### Package layout

- `code/`: sizing, reproduction, package integrity and source-table arithmetic checks.
- `data/Supplemental_Data_S1.xlsx`: audit, source-to-requirement mapping, example calculations and separately tagged context evidence.
- `data/*.csv`: 35-source inventory, 25 requirements, assumptions, profiles, reported benchmark tables, service-context ledger.
- `docs/`: implementation notes, security boundaries, evidence/source reconciliation and release instructions.
- `config/`: nonproduction example with provenance and explicit hardware-version discrepancy.
- `examples/`: public-safe educational workload examples, **not production config**.
- `CITATION.cff`: valid project citation; no fictional DOI.

### Submission files

Use `data/Supplemental_Data_S1.xlsx` as Supplemental Data S1 and the complete versioned repository archive as Supplemental Code S2. The updated S1 adds two explicitly contextual sheets; all original evidence CSVs and a byte-identical baseline S1 workbook are retained; Table 2 references in the sizing-assumptions source notes refer to the assumptions table, not the Table 3 node-count results. The workbook retains its original preparation date. See `docs/PEERJ_RESUBMISSION_TEXT.md` for conditional manuscript statements and `docs/GITHUB_ZENODO_RELEASE.md` for publication instructions.

### Licenses and citation

Code: MIT (`LICENSE_CODE`); data: CC BY 4.0 (`LICENSE_DATA`), subject to contributor/institutional rights confirmation. To cite this repository use the root `CITATION.cff`. Add a Zenodo DOI only **after** a real persistent DOI is issued. No placeholder DOI is advertised.

Repository intended for publication: https://github.com/ucerd/peerj-hpc-reproducibility . A local ZIP prepared for upload **does not mean the remote GitHub repository has been changed**.
