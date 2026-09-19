# Reproducibility notes

## What is reproduced

The package reproduces the CPU/GPU node counts in the manuscript's three
illustrative institutional profiles and the illustrative deployment scenario.

## What is not fabricated

The manuscript does not provide the component-level `D_*` inputs required to
numerically reconstruct the storage ranges in Table 2. The repository therefore
implements the storage equations but preserves those storage ranges as
manuscript-reported recommendations.

The targeted evidence synthesis was iterative rather than systematic. The
repository documents the 35 retained sources and their eligibility rationale;
it does not invent a rejected-source log or PRISMA-style candidate count.

## Context versus analytical data

`data/namal_hpc_public_context.csv` documents a real operational environment.
It is not used to compute the illustrative node counts and should not be treated
as a multi-site empirical validation dataset.
