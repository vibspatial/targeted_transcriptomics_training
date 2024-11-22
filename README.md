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

## Optional: build conda environment on the VSC

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

## Use the (prebuild) conda environment and submit jobs

### 1. Test the conda environment

Start an interactive session:
```
srun --account=lp_edu_ont2024 --clusters=genius --partition=interactive --ntasks 1 --cpus-per-task 8 --mem=16G --time=00:30:00 --pty bash
```

Now activate the conda environment (no need to have a conda installation, we will use the conda installation from the VSC to activate our environment):

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
import sparrow
```

### 2. Submit jobs

Go to the login nodes if you are still in an interactive session (you can check if you are on the login nodes by typing in the command line `hostname`):

```
exit
```

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

## Moving data to the VSC using Globus

See [here](globus/globus.ipynb) for a tutorial on how to move data to and from the VSC using Globus.


- **Dag 1 (9h30-17h):**
  - Korte presentatie als inleiding (<30 min; 9h30-10h)
    - Targeted transcriptomics
      - Hoe wordt data gegenereerd? ✓ Julien
      - Ruwe data ✓
  -  Download data. 0.get_data.ipynb. To be tested on windows.
      - Checken of installaties correct zijn (op voorhand documentatie voor installatie sturen)

  - Introductie notebook (1h; 10h-12h) # 5.explore_sdata.ipynb Arne( images/labels) Frank( shapes/tables/points )
    - Oefening: voorbereid sdata (points layer, table, layer, img layer, etc.) inlezen + een aantal plots maken. ✓
    - Terugkoppelen naar introductie Janick. Tonen wat onderliggende data is (numpy arrays, dataframes, gdf, Anndata...) ✓

  - Lever resolve notebook, deel 1 (13h-16h) 1.sparrow_pipeline.ipynb ✓ Frank/Julien vanaf de table
    - Pipeline stappen worden uitgelegd + basic (en optionele advanced) oefeningen en vragen. ✓
    - basic oefeningen toevoegen, parameters/crops/plots...
    - Interactieve plots in Napari
      - Basic: Output bekijken, Segmentatie fine-tunen, segmentatie met en zonder cleaning stappen, ander cropje testen
      - Advanced: Custom preprocessing stappen (image * 2, layer toevoegen aan sdata, ...) ✓
    - Downstream with squidpy, ... etc TODO Julien

  - Xenium data ( 9h30-10h30) 2.sparrow_pipeline_xenium.ipynb Frank
    - oefeningen toevoegen 
    - Bekijk ruwe data ✓
    - Bekijk data in Xenium Explorer ✓
    - Notebook maken om data in te lezen (test spatialdata io) + resolve notebook aanpassen voor xeniumdata ✓

  - Xenium explorer (11-12h) 3.xenium_explorer.ipynb Arne
    - tissuumaps Julien
    - xenium explorer installatie
    - hands on

  - Merscope (13h-15h) - 4.sparrow_pipeline_merscope.ipynb
    - remove VScode TODO
    - notebook show. Julien.
    - HPC. Test: Frank. TODO
    - HPC: Arne
    - oefening scp ...
    - excerise ploting.
    - (moeilijke) exercise, leiden cluster, parameters aanpassen.

  Bonus
  - Anndata to r
  - Bigwarp
  - Advanced spatialdata/coordinate systems



  


  


    - Sparrow/Harpy
      - Door wie
      - Doel
      - Grote stappen van pipeline ✓
    - SpatialData + Anndata

  - Pauze (15 min; 10h45-11h)

    - Dag 1 vermoedelijk tot en met clustering
  - Middagpauze (1h; 12h-13h)
  - Lever resolve notebook, deel 2 (4h; 13h-17h (+ 15 minuten pauze)) ✓

- **Dag 2 (9h30-17h):**
  - Lever resolve notebook, deel 3 (2h; 9h30-11h30)
    - Integratie met scanpy en squidpy (annotatie, neighborhoods, ...)
    - Iets zeggen over TissUUmaps, BigWarp??
  - Pauze (15 min; 11h30-11h45)
  - Xenium data (45 min; 11h45-12h30)
    - Bekijk ruwe data ✓
    - Bekijk data in Xenium Explorer ✓
    - Notebook maken om data in te lezen (test spatialdata io) + resolve notebook aanpassen voor xeniumdata ✓
  - Middagpauze (1h; 12h30-13h30)
  - HPC (1.5h; 13h30-15h)
    - Shared conda  ✓ TODO: to be tested by group members of lp_edu_ont2024 if all works fine (can run_slurm.sh be run?)
    - Script klaarzetten door ons ✓
    - Hoe data op HPC krijgen (link naar documentatie globus (van HPC) ✓
    - Vizgen data (spatialdata io bekijken). Grote crop nemen, maar uitleggen. ✓
    - Ruwe Vizgen data ook eens bekijken.
  - Pauze (15 min, 15h-15h15)
  - Advanced spatialdata (15h15-16h15) ? maybe for this part we could show notebook on coordinate systems https://harpy.readthedocs.io/en/latest/tutorials/advanced/coordinate_systems.html
  I think we cover a lot already in notebook 5.explore_sdata.ipynb
  - Vragenuurtje (45 min, 16h15-17h)
