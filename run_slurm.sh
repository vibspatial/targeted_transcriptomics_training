#!/bin/bash
#SBATCH --clusters=genius
#SBATCH --partition=gpu_v100
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=4      # Number of tasks (cores) per node
#SBATCH --gres=gpu:1             # Request 1 GPU
#SBATCH --time=01:00:00          # Walltime (hh:mm:ss)
#SBATCH --mem=32G                # Memory per node
#SBATCH --account=lp_edu_ont2024  # account name for this training
#SBATCH --job-name=merscope      # Job name

PATH_CONDA_ENV="/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env"

# Activate the conda environment using the Miniconda3 module of the VSC, so we do not require a local Miniconda3 installation.
# get path to the miniconda bin (/apps/leuven/rocky8/skylake/2021a/software/Miniconda3/4.12.0/bin) on the VSC via
# module load Miniconda3
# which python

# you could also use your local Miniconda3 installation, e.g. at $VSC_DATA_VO_USER/miniconda3/bin/activate, to activate the conda env.

source /apps/leuven/rocky8/skylake/2021a/software/Miniconda3/4.12.0/bin/activate $PATH_CONDA_ENV

# Run the Python script
python run_merscope.py \
 --input_dir /staging/leuven/stg_00143/spatial_data_training/merscope/0.0.1/transcriptomics/vizgen/mouse/Liver1Slice1 \
 --output_dir /staging/leuven/stg_00143/spatial_data_training/merscope \
 --crop 
