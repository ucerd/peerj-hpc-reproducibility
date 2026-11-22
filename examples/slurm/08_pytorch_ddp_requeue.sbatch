#!/usr/bin/env bash
#SBATCH --job-name=ddp_requeue
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --requeue
#SBATCH --signal=USR1@60

set -euo pipefail
mkdir -p checkpoints

export MASTER_ADDR
MASTER_ADDR="$(scontrol show hostnames "${SLURM_JOB_NODELIST}" | head -n 1)"
export MASTER_PORT=$((15000 + SLURM_JOB_ID % 20000))
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export CHECKPOINT_DIR="${PWD}/checkpoints/${SLURM_JOB_ID}"

# A site may requeue after preemption. Exit 99 does not itself requeue;
# verify local policy and shared checkpoint storage before use.
srun --kill-on-bad-exit=1 python examples/python/checkpoint_train.py
