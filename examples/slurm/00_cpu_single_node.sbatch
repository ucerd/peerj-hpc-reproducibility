#!/usr/bin/env bash
#SBATCH --job-name=cpu_smoke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G
#SBATCH --time=00:10:00

set -euo pipefail
mkdir -p logs

echo "job_id=${SLURM_JOB_ID}"
echo "node=$(hostname)"
echo "cpus_per_task=${SLURM_CPUS_PER_TASK}"
srun --cpu-bind=cores bash -lc 'hostname; nproc'
