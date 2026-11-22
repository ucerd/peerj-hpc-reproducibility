# Changelog

## 1.2.0 — Context dashboard update (2026-11-22)
- Add aggregate-only CAID dashboard and provisional management-metric register.
- Extend S1 with two contextual sheets; preserve original S1 baseline and evidence CSVs.
- Explicitly flag unknown units, stage discrepancies, and missing independent verification.
- Rebuild release inventory and integrity checks.

## 1.1.1 — Submission package maintenance (2026-11-22)
- Preserve original S1 workbook and evidence CSVs, including unresolved provenance.
- Verify exact file inventory and both integrity manifests; compare regenerated outputs in a temporary directory.
- Add numerical input-boundary tests and explicit strong-scaling arithmetic checks.
- Correct Slurm log paths, shared MPI executable location, and coordinated DDP checkpoint-stop behavior; site execution remains unverified.
- Add a Python CI matrix, submission-file mapping, and reproducible release instructions.

## 1.1.0 — PeerJ major-revision candidate (2026-11-16)
- Correct manuscript Table 3 and audit stale Table 2 references.
- Reconcile prior paper, later supplied technical manuscript, and repository profile **without asserting equivalence**.
- Add individual-job allocated resource-hour method, worked hypothetical storage calculation and source-table benchmark arithmetic check.
- Add independent vs contextual evidence constraints; source-specific partner ledger; strengthen validator with content checksums and 25-requirement count.
- Confirm root `CITATION.cff` present and remove fake Zenodo DOI template language.
- Update workbook and build a new release artifact; remote GitHub deployment remains an author action.

## 1.0.0 — Original candidate (2026-09-20)
- Original source inventory, sizing scripts and educational HPC examples.
