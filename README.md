# Implementing Supercomputing Infrastructure for Third-Generation Universities

## Reproducibility and implementation package

This repository accompanies the manuscript:

**Implementing Supercomputing Infrastructure for Third-Generation Universities: A Design Framework for Education, Research, and Innovation**

Authors: Tassadaq Hussain; Muhammad Najam Ul Islam; Amna Haider; Soltan Alharbi; Tan Kim Geok.

The package makes the design-science artifact, evidence traceability, sizing
method, worked examples, implementation checklist, KPI definitions, and
publication-safe HPC/Slurm examples auditable and reusable.

## Methodological boundary

This is **not** a republished institutional outcome dataset. The manuscript
develops and evaluates a generalizable design artifact. The Namal HPC profile
included here is contextual implementation evidence only and does not determine
the illustrative sizing calculations.

## Repository structure

```text
.
├── README.md
├── VERSION
├── CHANGELOG.md
├── CITATION.cff
├── LICENSE_CODE
├── LICENSE_DATA
├── SECURITY.md
├── requirements.txt
├── config/
│   └── namal_hpc_profile.json
├── code/
│   ├── hpc_sizing.py
│   ├── reproduce_results.py
│   └── validate_package.py
├── data/
│   ├── Supplemental_Data_S1.xlsx
│   ├── source_inventory.csv
│   ├── requirement_extraction.csv
│   ├── conformance_matrix.csv
│   ├── sizing_assumptions.csv
│   ├── institutional_profiles.csv
│   ├── illustrative_scenario.csv
│   ├── rounding_rules.csv
│   ├── implementation_checklist.csv
│   ├── kpi_definitions.csv
│   ├── procurement_template.csv
│   ├── framework_traceability.csv
│   ├── namal_hpc_public_context.csv
│   ├── training_source_index.csv
│   └── data_dictionary.csv
├── examples/
│   ├── slurm/
│   ├── src/
│   └── python/
├── docs/
├── tests/
└── outputs/
```

## Supplemental Data S1

`data/Supplemental_Data_S1.xlsx` contains:

1. retained source inventory;
2. retained-source eligibility rationale;
3. requirement-extraction matrix;
4. authoritative-source conformance matrix;
5. sizing assumptions;
6. institutional profile inputs;
7. formula-driven reproduction of manuscript Table 2;
8. illustrative scenario calculation;
9. rounding/handling rules;
10. data dictionary;
11. implementation checklist;
12. KPI definitions;
13. procurement/specification template;
14. research-question-to-artifact traceability;
15. Namal HPC contextual profile;
16. training-source provenance/index.

The manuscript reports a targeted, iterative evidence synthesis rather than a
systematic review. Therefore this package documents the 35 retained sources and
does not fabricate a rejected-source log or PRISMA-style candidate count.

## Core equations

```text
H_d^CPU = N_d × J_d × C_d × T_d
H_d^GPU = N_d × J_d × G_d × T_d

N_CPU = ceil(φ × H_CPU / (η_CPU × M × C_node))
N_GPU = ceil(φ × H_GPU / (η_GPU × M × G_node))

S_active     = D_input + D_scratch + D_checkpoints + D_outputs
S_persistent = D_projects + D_shared_software + D_curated_results
S_archive    = D_retained_datasets + D_compliance_copies
```

The worked examples use:

| Parameter | Value |
|---|---:|
| Design peak factor, φ | 1.25 |
| CPU target utilization, η_CPU | 0.70 |
| GPU target utilization, η_GPU | 0.60 |
| Available hours/month, M | 720 |
| CPU cores/node, C_node | 64 |
| GPUs/node, G_node | 4 |

## Reproduce the manuscript calculations

Core reproduction requires **Python 3.10+ only**.

```bash
python code/reproduce_results.py
```

Expected results:

| Case | CPU nodes | GPU nodes |
|---|---:|---:|
| Entry | 3 | 1 |
| Intermediate | 11 | 6 |
| Advanced | 28 | 21 |
| Illustrative scenario | 12 | 8 |

A successful run prints:

```text
Validation status: PASS
```

## Run the tests and package validation

```bash
python -m unittest discover -s tests -v
python code/validate_package.py
```

The validator checks required files, the 35-source inventory, numerical
reproduction, the current contextual Namal profile, and publication safety of
the public examples.

## Slurm and systems examples

The supplied training/learning archive included practical Slurm, MPI, GPU,
PyTorch distributed, NCCL/Gloo, monitoring, and troubleshooting material.
The public examples in this repository are rewritten and sanitized rather than
copied verbatim.

Examples include:

- single-node CPU;
- multi-node `srun`;
- OpenMP;
- MPI;
- single-node GPU;
- multi-node GPU probe;
- single-GPU PyTorch;
- PyTorch DDP/NCCL;
- checkpoint/requeue DDP;
- CUDA compilation for RTX 4070 Ti (`sm_89`).

See `docs/TRAINING_MATERIAL_PROVENANCE.md`.

## Namal HPC contextual profile

For this release, the operational context is recorded as:

- 20 compute nodes;
- 1,600 aggregate CPU cores;
- **40 NVIDIA GeForce RTX 4070 Ti GPUs**;
- **5 TB aggregate RAM**;
- **low-latency switched cluster fabric**;
- Slurm workload management.

The GPU count/model, RAM, and network description above are operator-confirmed
for this release and supersede conflicting older summary values. These values
are **context only** and are not used to derive the manuscript's illustrative
sizing results.

Public CAID site: https://caid.namal.edu.pk/

## Storage reproducibility limitation

The storage equations are implemented in `code/hpc_sizing.py`. The manuscript
does not report the component-level `D_*` values needed to reconstruct the
Table 2 storage ranges numerically. The package therefore preserves the storage
ranges as reported and does not reverse-engineer missing inputs.

## Security/publication safety

Do not publish production Slurm configuration, private IP addresses, internal
hostnames, NIC mappings, authentication material, user lists, or credentials.
The included examples contain none of these.

## Citation

After the release is archived, replace `10.5281/zenodo.XXXXXXX` below and in
`CITATION.cff`.

> Hussain, T., Islam, M. N. U., Haider, A., Alharbi, S., & Geok, T. K. (2026).
> *Reproducibility materials for “Implementing Supercomputing Infrastructure
> for Third-Generation Universities: A Design Framework for Education,
> Research, and Innovation”* (Version 1.0.0). Zenodo.
> https://doi.org/10.5281/zenodo.XXXXXXX

## License

- Code: MIT License (`LICENSE_CODE`)
- Data/reproducibility tables: CC BY 4.0 (`LICENSE_DATA`)

Confirm institutional/journal licensing requirements before public release.

## Contact

Tassadaq Hussain
tassadaq@ucerd.com
