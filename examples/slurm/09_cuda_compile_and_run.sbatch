#!/usr/bin/env bash
#SBATCH --job-name=cuda_build_run
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --mem=8G
#SBATCH --time=00:10:00

set -euo pipefail
mkdir -p logs

# RTX 4070 Ti is an Ada GPU (SM 8.9). Adapt module name to the site.
# module load cuda

nvcc -O3 -arch=sm_89 examples/src/cuda_vector_add.cu \
  -o /tmp/cuda_vector_add_${SLURM_JOB_ID}

srun /tmp/cuda_vector_add_${SLURM_JOB_ID}
