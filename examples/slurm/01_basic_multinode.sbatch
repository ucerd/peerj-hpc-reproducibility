#!/usr/bin/env bash
#SBATCH --job-name=multinode_smoke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=00:05:00

set -euo pipefail
mkdir -p logs

echo "Allocated hosts:"
scontrol show hostnames "${SLURM_JOB_NODELIST}"

echo "One task per allocated node:"
srun --label --distribution=block:block bash -lc \
  'echo rank=${SLURM_PROCID} local_rank=${SLURM_LOCALID} host=$(hostname)'
