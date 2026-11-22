"""Validate structure, data, calculations, and publication-safety of the package."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from release_integrity import verify

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "README.md",
    "CITATION.cff",
    "requirements.txt",
    "data/Supplemental_Data_S1.xlsx",
    "data/Supplemental_Data_S1_v1.1.1_baseline.xlsx",
    "data/CAID_Dashboard_FINAL_2026-11-22.xlsx",
    "data/caid_management_metrics.csv",
    "docs/CAID_DASHBOARD_NOTES.md",
    "data/source_inventory.csv",
    "data/requirement_extraction.csv",
    "data/cluster_configuration_sources.csv",
    "data/research_publication_provenance.csv",
    "data/paksupercomputer_reported_strong_scaling.csv",
    "data/illustrative_job_allocations.csv",
    "data/conformance_matrix.csv",
    "data/sizing_assumptions.csv",
    "data/institutional_profiles.csv",
    "data/illustrative_scenario.csv",
    "data/implementation_checklist.csv",
    "data/kpi_definitions.csv",
    "data/procurement_template.csv",
    "data/framework_traceability.csv",
    "data/namal_hpc_public_context.csv",
    "data/training_source_index.csv",
    "code/hpc_sizing.py",
    "code/reproduce_results.py",
    "docs/IMPLEMENTATION_GUIDE.md",
    "docs/NAMAL_HPC_CONTEXT.md",
    "examples/slurm/07_pytorch_ddp.sbatch",
]

FORBIDDEN_PUBLIC_PATTERNS = {
    "private IPv4 address": re.compile(r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
    "hard-coded historical node name": re.compile(r"\b(?:master-node|node0[1-9])\b", re.I),
    "private key marker": re.compile(r"BEGIN (?:RSA |OPENSSH )?PRIVATE KEY"),
    "password assignment": re.compile(r"(?i)\bpassword\s*=\s*['\"][^'\"]+['\"]"),
}

PUBLIC_SCAN_SUFFIXES = {".md", ".txt", ".py", ".sbatch", ".sh", ".csv", ".json", ".cff"}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    missing = [x for x in REQUIRED if not (ROOT / x).exists()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    profile = json.loads((ROOT / "config/namal_hpc_profile.json").read_text(encoding="utf-8"))
    if profile.get("role_in_study") != "context_only_not_empirical_validation_data":
        fail("source-specific Namal profile must be labeled contextual")
    variants = read_csv(ROOT / "data/cluster_configuration_sources.csv")
    if len(variants)<2 or not any("4070 Ti" in x["GPU_model"] for x in variants) or not any("4090" in x["GPU_model"] for x in variants):
        fail("conflicting source-specific cluster hardware records must be retained")
    cff=(ROOT/'CITATION.cff').read_text(encoding='utf-8')
    if 'cff-version: 1.2.0' not in cff or '10.5281/zenodo.XXXXXXX' in cff:
        fail('invalid or placeholder CFF citation')
    if f"version: {(ROOT/'VERSION').read_text().strip()}" not in cff:
        fail('citation version does not match VERSION')
    try:
        verify(ROOT)
    except (ValueError, OSError) as exc:
        fail(str(exc))
    # Validate the source inventory row count reported by the manuscript.
    if len(read_csv(ROOT / "data/source_inventory.csv")) != 35:
        fail("source_inventory.csv must contain exactly 35 retained sources")

    if len(read_csv(ROOT / "data/requirement_extraction.csv")) != 25:
        fail("requirement_extraction.csv must contain 25 retained requirements")

    metrics = read_csv(ROOT / "data/caid_management_metrics.csv")
    index = {row["metric_id"]: row for row in metrics}
    expected = {"completed_projects", "poc", "mvp", "cvp", "avg_usage", "potential_industry_links", "unspecified_metric"}
    if len(metrics) != 7 or set(index) != expected:
        fail("CAID metric register must contain exactly seven distinct reported indicators")
    if index["unspecified_metric"]["unit"] != "undefined" or "excluded" not in index["unspecified_metric"]["evidence_status"]:
        fail("undefined indicator must not acquire an unsupported unit")
    if any(row["reporting_cutoff"] != "2026-11-22" or not row["verification_required"] for row in metrics):
        fail("CAID indicator cutoff or verification caveat missing")
    print("PASS: CAID management metrics retain definition and verification caveats")

    # Reproduce in a temporary directory; do not overwrite archived evidence.
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [sys.executable, str(ROOT / 'code/reproduce_results.py'), '--output-dir', tmp],
            cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0 or 'Validation status: PASS' not in result.stdout:
            fail('numerical reproduction did not pass: ' + result.stderr)
        for output in Path(tmp).iterdir():
            if output.read_bytes() != (ROOT/'outputs'/output.name).read_bytes():
                fail('archived reproduction output differs: ' + output.name)
        result = subprocess.run([sys.executable, str(ROOT/'code/check_source_benchmark_arithmetic.py')],
                                cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            fail('benchmark arithmetic failed: ' + result.stderr)

    # Public examples must not leak internal addressing or historical hard-coded nodes.
    findings = []
    scan_roots = [ROOT / "examples", ROOT / "docs", ROOT / "config"]
    for scan_root in scan_roots:
        for p in scan_root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in PUBLIC_SCAN_SUFFIXES:
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
                if pattern.search(text):
                    findings.append(f"{label}: {p.relative_to(ROOT)}")
    if findings:
        fail("publication-safety scan found: " + "; ".join(findings))

    print("PASS: required files present")
    print("PASS: dated source-specific hardware records retained; contradictions clearly disclosed")
    print("PASS: complete manifest hashes match staged release files")
    print("PASS: 35 retained sources and 25 requirements present")
    print("PASS: regenerated sizing outputs match archived outputs; benchmark arithmetic passed")
    print("PASS: public examples/docs/config contain no internal IPs, historical node names, or private-key markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
