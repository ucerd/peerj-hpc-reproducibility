#!/usr/bin/env bash
#SBATCH --job-name=ddp_smoke
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --time=00:15:00

set -euo pipefail
mkdir -p logs

# Adapt to the site's managed environment:
# module load cuda
# module load nccl
# module load pytorch

export MASTER_ADDR
MASTER_ADDR="$(scontrol show hostnames "${SLURM_JOB_NODELIST}" | head -n 1)"

# Job-derived port avoids a fixed cluster-wide rendezvous port.
export MASTER_PORT=$((15000 + SLURM_JOB_ID % 20000))
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

# Useful for first-run diagnosis; reduce or remove for normal production runs.
export NCCL_DEBUG="${NCCL_DEBUG:-WARN}"

echo "master=${MASTER_ADDR}:${MASTER_PORT} tasks=${SLURM_NTASKS}"

srun --kill-on-bad-exit=1 python examples/python/ddp_smoke_test.py
