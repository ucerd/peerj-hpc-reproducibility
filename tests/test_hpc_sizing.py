import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "code"))

from hpc_sizing import (
    SizingAssumptions,
    active_storage,
    archive_storage,
    domain_cpu_core_hours,
    domain_gpu_hours,
    persistent_storage,
    required_cpu_nodes,
    required_gpu_nodes,
)


class SizingTests(unittest.TestCase):
    def setUp(self):
        self.a = SizingAssumptions()

    def test_table3_entry(self):
        self.assertEqual(required_cpu_nodes(70000, self.a), 3)
        self.assertEqual(required_gpu_nodes(1200, self.a), 1)

    def test_table3_intermediate(self):
        self.assertEqual(required_cpu_nodes(260000, self.a), 11)
        self.assertEqual(required_gpu_nodes(8000, self.a), 6)

    def test_table3_advanced(self):
        self.assertEqual(required_cpu_nodes(700000, self.a), 28)
        self.assertEqual(required_gpu_nodes(28000, self.a), 21)

    def test_scenario(self):
        self.assertEqual(required_cpu_nodes(300000, self.a), 12)
        self.assertEqual(required_gpu_nodes(10000, self.a), 8)

    def test_domain_demand(self):
        self.assertEqual(domain_cpu_core_hours(10, 2, 8, 3), 480)
        self.assertEqual(domain_gpu_hours(10, 2, 1, 3), 60)

    def test_storage(self):
        self.assertEqual(active_storage(1, 2, 3, 4), 10)
        self.assertEqual(persistent_storage(5, 6, 7), 18)
        self.assertEqual(archive_storage(8, 9), 17)

    def test_invalid_utilization(self):
        with self.assertRaises(ValueError):
            bad = SizingAssumptions(cpu_target_utilization=1.1)
            required_cpu_nodes(10, bad)


class UpdatedMethodTests(unittest.TestCase):
    def test_individual_allocated_job_hours(self):
        from hpc_sizing import allocated_job_resource_hours
        cases=[{'Allocated_CPU_cores':2,'Allocated_GPUs':0,'Elapsed_hours_overlapping_month':10},
               {'Allocated_CPU_cores':32,'Allocated_GPUs':2,'Elapsed_hours_overlapping_month':1},
               {'Allocated_CPU_cores':8,'Allocated_GPUs':1,'Elapsed_hours_overlapping_month':4}]
        self.assertEqual(allocated_job_resource_hours(cases,'Allocated_CPU_cores'),84)
        self.assertEqual(allocated_job_resource_hours(cases,'Allocated_GPUs'),6)
    def test_negative_job_allocation_rejected(self):
        from hpc_sizing import allocated_job_resource_hours
        with self.assertRaises(ValueError):
            allocated_job_resource_hours([{'Allocated_CPU_cores':-1,'Elapsed_hours_overlapping_month':2}],'Allocated_CPU_cores')


class InputBoundaryTests(unittest.TestCase):
    def test_zero_demand(self):
        self.assertEqual(required_cpu_nodes(0, SizingAssumptions()), 0)
        self.assertEqual(required_gpu_nodes(0, SizingAssumptions()), 0)

    def test_nonfinite_demand(self):
        for value in (float('nan'), float('inf'), -1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                required_cpu_nodes(value, SizingAssumptions())

    def test_nonfinite_assumption(self):
        with self.assertRaises(ValueError):
            required_cpu_nodes(1, SizingAssumptions(peak_factor=float('inf')))


if __name__ == '__main__':
    unittest.main()
