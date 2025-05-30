#!/bin/bash
#SBATCH --clusters=genius
#SBATCH --partition=batch
#SBATCH --nodes=1               # Number of nodes
#SBATCH --ntasks-per-node=8      # Number of tasks (cores) per node
#SBATCH --time=02:00:00          # Walltime (hh:mm:ss)
#SBATCH --mem=16G                # Memory per node
#SBATCH --account=lp_edu_ont2024  # Replace with your actual account name
#SBATCH --job-name=build_conda      # Job name

#1) install miniconda in $VSC_DATA_VO_USER if VO is available, else in $VSC_DATA:
# mkdir -p miniconda3
# wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3/miniconda.sh
# bash miniconda3/miniconda.sh -b -u -p miniconda3
# rm -rf miniconda3/miniconda.sh

# miniconda3/bin/conda init bash

#2) set libmamba as the solver
# conda install -n base conda-libmamba-solver
# conda config --set solver libmamba

#PATH_CONDA_ENV="/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env_14_4_25" # pick a path, this can be changed
PATH_CONDA_ENV="/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env_30_5_25" # pick a path, this can be changed

source $VSC_DATA_VO_USER/miniconda3/bin/activate

conda env create --prefix $PATH_CONDA_ENV -f environment_vib_compute.yml

# activate the environment
source $VSC_DATA_VO_USER/miniconda3/bin/activate $PATH_CONDA_ENV

export PIP_NO_CACHE_DIR=off
pip install git+https://github.com/saeyslab/harpy.git@main#egg=harpy-analysis[test,basic,opencv,clustering,cellpose,instanseg]
pip install cellpose==3.1.1.2 

# Optional: run a test script, to check if everything installed correctly
python run_test.py

# need to do
# cd $VSC_DATA_VO_USER/miniconda3/envs
#ln -s /staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env_7_4_25/