#!/usr/bin/env bash
#SBATCH --job-name=multinode_gpu_probe
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --time=00:10:00

set -euo pipefail

srun --label --kill-on-bad-exit=1 bash -lc '
  echo "rank=${SLURM_PROCID} host=$(hostname) visible=${CUDA_VISIBLE_DEVICES:-unset}"
  nvidia-smi --query-gpu=name,uuid --format=csv,noheader
'
