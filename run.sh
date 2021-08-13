#!/bin/sh
#PBS -N r_30
#PBS -q ibs_large
#PBS -l select=4:ncpus=16:mpiprocs=16:ompthreads=1
#PBS -l walltime=120:00:00
#PBS -j oe

cd $PBS_O_WORKDIR

module unload craype-x86-skylake
module unload python
module unload PrgEnv-cray
module load PrgEnv-intel
module load craype-x86-skylake
module load cray-hdf5-parallel/1.10.2.0
module load cray-fftw/3.3.8.1
module load cray-python/3.7.3.2
module load craype-hugepages8M

export ATP_ENABLED=1
export MPICH_MAX_THREAD_SAFETY=multiple
export OMP_NUM_THREADS=1
export OMP_SCHEDULE=dynamic
export KMP_AFFINITY=disabled

aprun -n 32 ~/Smilei-4.5_new/smilei ./hhg_1d.py > log 2>&1
