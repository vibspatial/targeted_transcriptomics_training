# VSC account info

Disk quota, Virtual Organization (VO) membership, ...

https://account.vscentrum.be/

# Accessing the KULeuven VSC HPC

SSH to login node from the command line:

```bash
ssh login.hpc.kuleuven.be
```

In the browser:
```
https://ondemand.hpc.kuleuven.be/
```

with useful options (for this training)

- Login Server Shell Access
- Interactive Shell
- Visual Studio Code

# Course prep

Login on the KULeuven VSC cluster and perform (the relevant parts of) the following steps:

## Clone training repo

```
cd /staging/leuven/stg_00143
mkdir YOURNAME
cd YOURNAME
git clone https://github.com/vibspatial/targeted_transcriptomics_training.git
```

## Link to training conda environment

Check if you have a link to the common training conda env `training_env_janick` already:

```bash
conda env list
```

If not, link to it:

```bash
cd `conda info --base`/envs
ln -s /staging/leuven/stg_00143/janick/spatial/environments/spatial_data_training_env training_env_janick
```

Make sure `training_env_janick` shows up now:

```bash
conda env list
```

## Source data for notebook 5.sparrow_pipeline_mercscope.ipynb

The data for the notebook is downloaded and available on the HPC already. Instead of all downloading it ourselves, in the notebook we'll access it with:

```bash
registry = get_registry(path = "/staging/leuven/stg_00143/spatial_data_training/merscope")
```

# Visual Studio Code on the HPC

Via https://ondemand.hpc.kuleuven.be/ start Visual Studio Code with the following resources:

```txt
Cluster: Genius
Partition: interactive
Account: lp_edu_ont2024
Number of hours: 3 (or 4)
Number of nodes: 1
Number of processes per node: 8
Memory per core in MB: 4000
Number of GPUs: 0
```

Press "Connect to Visual Studio Code".

When it's opened, load your training repo folder:

Three horizontal lines icon > File > Open Folder > /staging/leuven/stg_00143/YOURNAME/targeted_transcriptomics_training/

Open the file 5.sparrow_pipeline_merscope.ipynb.

Select kernel `training_env_janick`.

Modify the path where the data is read:

```bash
...
registry = get_registry(path = "/staging/leuven/stg_00143/spatial_data_training/merscope")
...
```

# Useful commands

Start a shell to perform interactive work *on a compute node*:

```bash
srun -A lp_edu_ont2024 -M genius -p interactive -N 1 -n 8 –mem=40000m -t 4:00:00 –pty bash -l
```

Alias to show my jobs in the queue:

```bash
alias sqme='squeue --format="%.18i %.22P %.20j %T %.10M %.12l %.20R" --me'
```

Alias to show recent jobs (running and completed):

```bash
alias sac='sacct --format=jobid,elapsed,ncpus,ntasks,state'
```

Job info:

```bash
slurm_jobinfo YOURJOBID
```

Job efficiency (after it completed):

```bash
seff YOURJOBID
```
