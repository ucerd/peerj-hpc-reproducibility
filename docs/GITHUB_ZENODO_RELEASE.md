# GitHub + Zenodo release procedure

1. Create a public GitHub repository.
2. Place the **contents** of this package at the repository root.
3. Replace `10.5281/zenodo.XXXXXXX` in `README.md` and `CITATION.cff` after a
   DOI is reserved/issued.
4. Run:
   ```bash
   python code/reproduce_results.py
   python -m unittest discover -s tests -v
   python code/validate_package.py
   ```
5. Commit only publication-safe files. Do not add production scheduler
   configuration, credentials, internal host lists, private IP addressing,
   SSH keys, or restricted datasets.
6. Tag the release `v1.0.0`.
7. Create a GitHub Release.
8. Archive the release in Zenodo or Figshare and record the DOI.
9. Update the PeerJ Data Availability and Code Availability declarations.
10. Preserve the exact archived release used in the resubmission.
