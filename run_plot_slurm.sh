#!/bin/bash
#SBATCH --clusters=genius
#SBATCH --partition=batch
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=4      # Number of tasks (cores) per node
#SBATCH --time=00:30:00          # Walltime (hh:mm:ss)
#SBATCH --mem=16G                # Memory per node
#SBATCH --account=lp_edu_ont2024  # Replace with your actual account name
#SBATCH --job-name=plot_leiden     # Job name

PATH_CONDA_ENV="/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env" # pick a path, this can be changed

source /apps/leuven/rocky8/skylake/2021a/software/Miniconda3/4.12.0/bin/activate $PATH_CONDA_ENV

python plot_leiden.py \
 --sdata_path /staging/leuven/stg_00143/spatial_data_training/merscope/sdata_merscope_crop.zarr \
 --output_dir /staging/leuven/stg_00143/spatial_data_training/merscope