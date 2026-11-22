"""Check source-reported strong-scaling arithmetic, not a workload rerun."""
from pathlib import Path
import csv
import math
ROOT = Path(__file__).resolve().parent.parent
with (ROOT/'data/paksupercomputer_reported_strong_scaling.csv').open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
if [int(r['Nodes']) for r in rows] != [1, 2, 4, 8, 16, 20]:
    raise ValueError('Unexpected source-table node sequence')
baseline = float(rows[0]['Runtime_s_reported'])
for r in rows:
    n = int(r['Nodes']); t = float(r['Runtime_s_reported'])
    if not math.isfinite(t) or t <= 0:
        raise ValueError(f'Invalid runtime: {n} nodes')
    speedup = baseline/t; efficiency = 100*speedup/n
    if not abs(speedup-float(r['Speedup_reported'])) < 0.011:
        raise ValueError(f'Speedup mismatch: {n} nodes')
    if not abs(efficiency-float(r['Efficiency_pct_reported'])) < 0.51:
        raise ValueError(f'Efficiency mismatch: {n} nodes')
    print(f'{n:2d} nodes: calculated speedup={speedup:.4f}, efficiency={efficiency:.2f}%')
print('PASS: 6 source-reported manuscript rows checked for speedup and efficiency; raw logs NOT reproduced')
