"""Validate structure, data, calculations, and publication-safety of the package."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = [
    "README.md",
    "CITATION.cff",
    "requirements.txt",
    "data/Supplemental_Data_S1.xlsx",
    "data/source_inventory.csv",
    "data/requirement_extraction.csv",
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
    if profile["gpu"]["model"] != "NVIDIA GeForce RTX 4070 Ti":
        fail("unexpected GPU model in Namal profile")
    if profile["gpu"]["count"] != 40:
        fail("unexpected GPU count in Namal profile")
    if profile["memory"]["aggregate_tb"] != 5:
        fail("unexpected aggregate RAM in Namal profile")
    if "low-latency" not in profile["network"]["fabric"].lower():
        fail("network fabric is not marked low-latency")

    # Validate the source inventory row count reported by the manuscript.
    if len(read_csv(ROOT / "data/source_inventory.csv")) != 35:
        fail("source_inventory.csv must contain exactly 35 retained sources")

    # Re-run the numerical reproduction.
    result = subprocess.run(
        [sys.executable, str(ROOT / "code/reproduce_results.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or "Validation status: PASS" not in result.stdout:
        fail("numerical reproduction did not pass")

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
    print("PASS: current Namal HPC profile matches operator-confirmed GPU/RAM/network values")
    print("PASS: 35 retained sources present")
    print("PASS: numerical reproduction passed")
    print("PASS: public examples/docs/config contain no internal IPs, historical node names, or private-key markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
