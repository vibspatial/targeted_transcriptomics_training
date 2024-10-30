#!/bin/bash -l
#PBS -l nodes=1:ppn=4:gpus=1
#PBS -l walltime=02:00:00
#PBS -l mem=64gb
#PBS -m bea
#PBS -N merscope

conda activate training_env

cd $VSC_DATA_VO_USER/VIB/code/targeted_transcriptomics_training
python run_merscope.py

#qsub -I -l nodes=1:ppn=16,mem=4G,walltime=1:00:00
#srun --pty -n 16 --mem=4G --time=1:00:00 bash
#srun --pty --overlap --jobid YOUR-JOBID bash