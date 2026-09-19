"""Reproduce the manuscript's CPU/GPU node-count examples.

No third-party Python package is required.

Run:
    python code/reproduce_results.py

Optional:
    python code/reproduce_results.py --data-dir data --output-dir outputs
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from hpc_sizing import SizingAssumptions, required_cpu_nodes, required_gpu_nodes


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def load_assumptions(path: Path) -> SizingAssumptions:
    raw = {row["Parameter_Key"]: float(row["Value"]) for row in read_csv(path)}
    return SizingAssumptions(
        peak_factor=raw["peak_factor"],
        cpu_target_utilization=raw["cpu_target_utilization"],
        gpu_target_utilization=raw["gpu_target_utilization"],
        available_hours_per_month=raw["available_hours_per_month"],
        cpu_cores_per_node=raw["cpu_cores_per_node"],
        gpus_per_node=raw["gpus_per_node"],
    )


def reproduce_profiles(data_dir: Path, output_dir: Path, a: SizingAssumptions):
    out = []
    for row in read_csv(data_dir / "institutional_profiles.csv"):
        calc_cpu = required_cpu_nodes(float(row["CPU_Core_Hours_Per_Month"]), a)
        calc_gpu = required_gpu_nodes(float(row["GPU_Hours_Per_Month"]), a)
        out.append({
            **row,
            "Calculated_CPU_Nodes": calc_cpu,
            "Calculated_GPU_Nodes": calc_gpu,
            "CPU_Match": str(calc_cpu == int(row["Manuscript_CPU_Nodes"])),
            "GPU_Match": str(calc_gpu == int(row["Manuscript_GPU_Nodes"])),
        })
    write_csv(output_dir / "table2_reproduced.csv", out)
    return out


def reproduce_scenario(data_dir: Path, output_dir: Path, a: SizingAssumptions):
    out = []
    for row in read_csv(data_dir / "illustrative_scenario.csv"):
        calc_cpu = required_cpu_nodes(float(row["CPU_Core_Hours_Per_Month"]), a)
        calc_gpu = required_gpu_nodes(float(row["GPU_Hours_Per_Month"]), a)
        out.append({
            **row,
            "Calculated_CPU_Nodes": calc_cpu,
            "Calculated_GPU_Nodes": calc_gpu,
            "CPU_Match": str(calc_cpu == int(row["Manuscript_CPU_Nodes"])),
            "GPU_Match": str(calc_gpu == int(row["Manuscript_GPU_Nodes"])),
        })
    write_csv(output_dir / "illustrative_scenario_reproduced.csv", out)
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", type=Path, default=ROOT / "data")
    p.add_argument("--output-dir", type=Path, default=ROOT / "outputs")
    args = p.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    assumptions = load_assumptions(args.data_dir / "sizing_assumptions.csv")
    profiles = reproduce_profiles(args.data_dir, args.output_dir, assumptions)
    scenario = reproduce_scenario(args.data_dir, args.output_dir, assumptions)

    ok_profiles = all(r["CPU_Match"] == "True" and r["GPU_Match"] == "True" for r in profiles)
    ok_scenario = all(r["CPU_Match"] == "True" and r["GPU_Match"] == "True" for r in scenario)
    status = "PASS" if ok_profiles and ok_scenario else "FAIL"

    lines = [f"Validation status: {status}", "", "Table 2 institutional profiles:"]
    for r in profiles:
        lines.append(
            f"- {r['Profile']}: CPU {r['Calculated_CPU_Nodes']} "
            f"(reported {r['Manuscript_CPU_Nodes']}), GPU {r['Calculated_GPU_Nodes']} "
            f"(reported {r['Manuscript_GPU_Nodes']})"
        )
    lines += ["", "Illustrative scenario:"]
    for r in scenario:
        lines.append(
            f"- {r['Scenario']}: CPU {r['Calculated_CPU_Nodes']} "
            f"(reported {r['Manuscript_CPU_Nodes']}), GPU {r['Calculated_GPU_Nodes']} "
            f"(reported {r['Manuscript_GPU_Nodes']})"
        )
    lines += [
        "",
        "Storage note:",
        "Storage equations are implemented in code/hpc_sizing.py, but the manuscript",
        "does not report the component-level D_* inputs needed to reconstruct the",
        "Table 2 storage ranges. Those ranges are therefore preserved as reported",
        "rather than reverse-engineered from invented inputs.",
    ]
    report = "\n".join(lines) + "\n"
    (args.output_dir / "validation_report.txt").write_text(report, encoding="utf-8")
    print(report)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
