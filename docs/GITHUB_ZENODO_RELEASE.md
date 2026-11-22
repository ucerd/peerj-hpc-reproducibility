# Publishing the corrected release (author action)

1. Review the source-specific hardware discrepancies and confirm sharing rights for each data file. Never add cluster secrets, confidential partner contracts or live scheduler auth data.
2. From the unzipped root, run all commands shown in `README.md`; preserve outputs.
3. After verification, push these files to the `ucerd/peerj-hpc-reproducibility` repository (requires an authorized GitHub account). No remote update has been made by preparation of this package.
4. Tag a new revision tag e.g. `v1.2.0` **only after** remote commit is accepted. Create a GitHub Release from that tag.
5. Archive that precise release at an approved permanent repository, obtain a genuine DOI, and cite that DOI. Do not change the tagged archive after DOI issuance; any later DOI metadata edits require a new release and rebuilt checksums.
6. Upload *the same ZIP and included S1* to PeerJ and cite the resulting stable release/commit. Provide final log outputs in the resubmission record.
7. Distinguish reproducible **illustrative** source calculations from the later paper's **reported** benchmark values, which lack raw logs in this package.
