#!/usr/bin/env bash
#SBATCH --job-name=mpi_demo
#SBATCH --output=logs/%x_%j.out
#SBATCH --error=logs/%x_%j.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:10:00

set -euo pipefail
mkdir -p logs

# Adapt to the site's MPI/compiler modules if required.
# module load gcc
# module load openmpi

mpicc -O3 examples/src/hello_mpi.c -o /tmp/hello_mpi_${SLURM_JOB_ID}

# Prefer Slurm-native launch when the site MPI is built with Slurm PMI/PMIx.
srun --kill-on-bad-exit=1 /tmp/hello_mpi_${SLURM_JOB_ID}
