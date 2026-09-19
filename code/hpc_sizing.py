"""Parameterized sizing functions for the university HPC design framework.

The implementation is intentionally vendor-neutral and uses only the Python
standard library. It implements the equations reported in the manuscript.

Notation
--------
H_d_CPU = N_d * J_d * C_d * T_d
H_d_GPU = N_d * J_d * G_d * T_d

N_CPU = ceil(phi * H_CPU / (eta_CPU * M * C_node))
N_GPU = ceil(phi * H_GPU / (eta_GPU * M * G_node))

Storage:
S_active     = D_input + D_scratch + D_checkpoints + D_outputs
S_persistent = D_projects + D_shared_software + D_curated_results
S_archive    = D_retained_datasets + D_compliance_copies
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


@dataclass(frozen=True)
class SizingAssumptions:
    peak_factor: float = 1.25
    cpu_target_utilization: float = 0.70
    gpu_target_utilization: float = 0.60
    available_hours_per_month: float = 720.0
    cpu_cores_per_node: float = 64.0
    gpus_per_node: float = 4.0

    def validate(self) -> None:
        if self.peak_factor <= 0:
            raise ValueError("peak_factor must be > 0")
        for name in (
            "cpu_target_utilization",
            "gpu_target_utilization",
        ):
            value = getattr(self, name)
            if not 0 < value <= 1:
                raise ValueError(f"{name} must be in (0, 1]")
        if self.available_hours_per_month <= 0:
            raise ValueError("available_hours_per_month must be > 0")
        if self.cpu_cores_per_node <= 0:
            raise ValueError("cpu_cores_per_node must be > 0")
        if self.gpus_per_node <= 0:
            raise ValueError("gpus_per_node must be > 0")


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return value


def domain_cpu_core_hours(
    active_users_or_projects: float,
    jobs_per_user_or_project: float,
    cpu_cores_per_job: float,
    average_runtime_hours: float,
) -> float:
    """Return H_d_CPU = N_d * J_d * C_d * T_d."""
    n = _nonnegative("active_users_or_projects", active_users_or_projects)
    j = _nonnegative("jobs_per_user_or_project", jobs_per_user_or_project)
    c = _nonnegative("cpu_cores_per_job", cpu_cores_per_job)
    t = _nonnegative("average_runtime_hours", average_runtime_hours)
    return n * j * c * t


def domain_gpu_hours(
    active_users_or_projects: float,
    jobs_per_user_or_project: float,
    gpus_per_job: float,
    average_runtime_hours: float,
) -> float:
    """Return H_d_GPU = N_d * J_d * G_d * T_d."""
    n = _nonnegative("active_users_or_projects", active_users_or_projects)
    j = _nonnegative("jobs_per_user_or_project", jobs_per_user_or_project)
    g = _nonnegative("gpus_per_job", gpus_per_job)
    t = _nonnegative("average_runtime_hours", average_runtime_hours)
    return n * j * g * t


def total_demand(domain_demands: Iterable[float]) -> float:
    """Sum non-negative demand values."""
    values = [_nonnegative("domain_demand", x) for x in domain_demands]
    return float(sum(values))


def required_nodes(
    demand_hours: float,
    peak_factor: float,
    target_utilization: float,
    available_hours_per_month: float,
    capacity_per_node: float,
) -> int:
    """Return ceiling-rounded node count for a parameterized resource."""
    demand = _nonnegative("demand_hours", demand_hours)
    peak = float(peak_factor)
    util = float(target_utilization)
    month = float(available_hours_per_month)
    capacity = float(capacity_per_node)

    if peak <= 0:
        raise ValueError("peak_factor must be > 0")
    if not 0 < util <= 1:
        raise ValueError("target_utilization must be in (0, 1]")
    if month <= 0:
        raise ValueError("available_hours_per_month must be > 0")
    if capacity <= 0:
        raise ValueError("capacity_per_node must be > 0")

    raw = peak * demand / (util * month * capacity)
    return math.ceil(raw)


def required_cpu_nodes(cpu_core_hours_per_month: float, assumptions: SizingAssumptions) -> int:
    assumptions.validate()
    return required_nodes(
        cpu_core_hours_per_month,
        assumptions.peak_factor,
        assumptions.cpu_target_utilization,
        assumptions.available_hours_per_month,
        assumptions.cpu_cores_per_node,
    )


def required_gpu_nodes(gpu_hours_per_month: float, assumptions: SizingAssumptions) -> int:
    assumptions.validate()
    return required_nodes(
        gpu_hours_per_month,
        assumptions.peak_factor,
        assumptions.gpu_target_utilization,
        assumptions.available_hours_per_month,
        assumptions.gpus_per_node,
    )


def active_storage(input_data: float, scratch: float, checkpoints: float, outputs: float) -> float:
    return sum(_nonnegative("active_storage_component", x) for x in (input_data, scratch, checkpoints, outputs))


def persistent_storage(projects: float, shared_software: float, curated_results: float) -> float:
    return sum(_nonnegative("persistent_storage_component", x) for x in (projects, shared_software, curated_results))


def archive_storage(retained_datasets: float, compliance_copies: float) -> float:
    return sum(_nonnegative("archive_storage_component", x) for x in (retained_datasets, compliance_copies))
