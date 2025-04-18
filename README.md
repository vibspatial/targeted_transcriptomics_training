# Working on the HPC

Login to the HPC:

```
ssh {YOUR_VSC_USERNAME}@login.hpc.kuleuven.be
```

Then clone the repository in a folder inside `/staging/leuven/stg_00143`:

```
cd /staging/leuven/stg_00143
mkdir my_directory
cd my_directory
git clone https://github.com/vibspatial/targeted_transcriptomics_training
cd targeted_transcriptomics_training
```

## Build conda environment on the VSC

### 1. Install miniconda in `$VSC_DATA` or `$VSC_DATA_VO_USER` if a `VO` is available:

```
cd $VSC_DATA
mkdir -p miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3/miniconda.sh
bash miniconda3/miniconda.sh -b -u -p miniconda3
rm -rf miniconda3/miniconda.sh
miniconda3/bin/conda init bash 
```

Set [libmamba](https://www.anaconda.com/blog/a-faster-conda-for-a-growing-community) as the solver:

```
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

### 2. Build the Conda environment:

Change the `PATH_CONDA_ENV` parameter in the script `build_conda_slurm.sh` to the path where you want to store the conda environment. Then build the conda environment:

```
sbatch build_conda_slurm.sh
```

## Use the (prebuild) conda environment

### 1. Test the conda environment

Start an interactive session:
```
srun --account=lp_edu_ont2024 --clusters=genius --partition=interactive --ntasks 1 --cpus-per-task 8 --mem=16G --time=00:30:00 --pty bash
```

Now activate the conda environment (we use the conda installation from the VSC to activate our environment):

```
source /apps/leuven/rocky8/skylake/2021a/software/Miniconda3/4.12.0/bin/activate $PATH_CONDA_ENV
```

With `PATH_CONDA_ENV` the path to your custom build conda environment, or the path to the prebuild conda environment we provide at:

```
/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env
```

Now run following commands:

```
python
```

and then in the python shell:

```
import harpy
```

### 2. Use VS Code on the VSC

Make sure to install miniconda to be able to use the prebuild conda environment in a VS Code session:

```
cd $VSC_DATA
mkdir -p miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda3/miniconda.sh
bash miniconda3/miniconda.sh -b -u -p miniconda3
rm -rf miniconda3/miniconda.sh
miniconda3/bin/conda init bash
```

Make a symlink to the (prebuild) conda environment (only necessary if conda environment is not located at `$VSC_DATA/miniconda3/envs`).

```
cd $VSC_DATA/miniconda3/envs
ln -s /staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env
```

After launching VS Code (see below), please make sure to install the Python and Jupyter extensions, otherwise VS Code will not be able to find the Python environments.

If kernel can not be found try disabling and enabling the jupyter vs code extension.

### VSC KU Leuven

Go to [Open OnDemand](https://ondemand.hpc.kuleuven.be)

Choose Visual Studio Code.

Make sure to change the number of hours, and set the number of processes per node to 8.

Select `Launch` and then connect.

Select the kernel when you want to run Jupyter Notebooks, e.g. `/staging/leuven/stg_00143/spatial_data_training/conda_environments/spatial_data_training_env`.

### VSC Ugent

Work with a VS Code tunnel.

Follow instruction [here](https://docs.hpc.ugent.be/Linux/vscodetunnel/)

### VIB Compute

Work with a VS code tunnel.

Follow instructions [here](https://docs.datacore.vib.be/compute-cluster/entrypoints/command-line-access/#connect-using-a-visual-studio-code-tunnel)

Or via [Open OnDemand](https://docs.datacore.vib.be/compute-cluster/entrypoints/open-on-demand/vs-code-web-server).


### 3. Submit jobs

Go to the login nodes (you can check if you are on the login nodes by typing in the command line `hostname`):

In the Slurm script `run_slurm.sh`, change the `output_dir` argument in the `python run_merscope.py` command to specify your desired output directory. The resulting `SpatialData` `.zarr` store and some figures will be saved there.

Submit the job:

```
sbatch run_slurm.sh
```

This job will approximatly take half an hour to finish.

### 3. Submit job to explore the data


In the Slurm script `run_plot_slurm.sh`, change the `sdata_path` and `output_dir` argument in the `python plot_leiden.py` command to respectively the `SpatialData` `.zarr` store and the desired directory where figures will be saved.

On a login node, submit the job:

```
sbatch run_plot_slurm.sh
```

You can also explore the data using an interactive session:

```
srun --account=lp_edu_ont2024 --clusters=genius --partition=interactive --ntasks 1 --cpus-per-task 8 --mem=16G --time=02:00:00 --pty bash
```

Tip:

If your connection was closed, and you still have an interactive session running, you can connect back to it via:

```
srun --account=lp_edu_ont2024 --clusters=genius --partition=interactive  --pty --overlap --jobid YOUR-JOBID bash
```

You can get the `jobid` via the command `squeue`.

Activate your conda environment:

```
source /apps/leuven/rocky8/skylake/2021a/software/Miniconda3/4.12.0/bin/activate $PATH_CONDA_ENV
```

Run the python script:

```
python plot_leiden.py \
 --sdata_path /staging/leuven/stg_00143/spatial_data_training/merscope/sdata_merscope_crop.zarr \
 --output_dir /staging/leuven/stg_00143/spatial_data_training/merscope
```

### Excercises

For the following excercises, use the `SpatialData` `.zarr` store obtained using the `run_merscope.py` Python script and accompanying slurm script `run_slurm.sh`.

- Create a Python script that plots the leiden clusters for `x_min=30000`, `x_max=40000`, `y_min=30000`, `y_max=40000`. Submit to the HPC using a slurm script.
- Create a Python script that plots the expression level of the gene `Alas2` in the region `x_min=30000`, `x_max=40000`, `y_min=30000`, `y_max=40000`. Submit to the HPC using a slurm script.
- Create a Python script that only does leiden clustering and visualization of the leiden clusters. Modify the parameters of `hp.tb.leiden`.
- Create a notebook that does leiden clustering, and visualizes the leiden clusters. Run the notebook. Please make sure not to run the notebook on one of the login nodes of the HPC.

## Moving data to the VSC using Globus

See [here](globus/globus.ipynb) for a tutorial on how to move data to and from the VSC using Globus.


## Connect to a remote Cluster with VS Code Remote - SSH

(not recommended on the login nodes of the VSC)

### Install VS Code and the Remote - SSH Extension:

    - Open VS Code.

    - Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing Ctrl+Shift+X.

    - Search for "Remote - SSH" and install it.

### Configure SSH in VS Code:

    - Press F1 to open the Command Palette in VS Code.

    - Type Remote-SSH: Open Configuration File... and select it.

    - Choose the SSH configuration file to edit. It’s usually located at ~/.ssh/config.

    - Add the following configuration to the file:

```yaml
Host {NAME}
    HostName {YOUR_HOSTNAME}
    User {YOUR_USERNAME}
    ForwardAgent yes
```

{YOUR_HOSTNAME} is the name of the cluster you want to connect to (e.g. via ssh {YOUR_USERNAME}@{YOUR_HOSTNAME}), and {NAME} can be a name of choice.

### Connect to the Remote Server:

    - Press F1 to open the Command Palette.

    - Type Remote-SSH: Connect to Host... and select it.

    - You should see `{NAME}` in the list. Select it.

    - VS Code will open a new window and start connecting to the remote server.
    
    - You might be prompted for your SSH key passphrase or password.

