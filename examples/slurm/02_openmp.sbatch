#!/usr/bin/env bash
#SBATCH --job-name=openmp_demo
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=4G
#SBATCH --time=00:10:00

set -euo pipefail

# Adapt to the site's compiler module if required.
# module load gcc

gcc -O3 -fopenmp examples/src/openmp_hello.c -o /tmp/openmp_hello_${SLURM_JOB_ID}
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OMP_PROC_BIND=close
export OMP_PLACES=cores
srun --cpu-bind=cores /tmp/openmp_hello_${SLURM_JOB_ID}
