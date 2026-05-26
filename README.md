# Spatial Omics Training

This repository contains course material for the [Spatial Omics Summer School](https://www.vibconferences.be/events/spatial-omics-summer-school). The notebooks guide participants through working with [`SpatialData`](https://spatialdata.scverse.org/) objects, targeted transcriptomics data and spatial proteomics data.

The exercises use [Harpy](https://github.com/saeyslab/harpy) for spatial omics analysis workflows and [napari-harpy](https://github.com/vibspatial/napari-harpy) for interactive inspection and visualization in napari.

# Installation

The repository includes a `create_env.sh` helper script that creates a Python 3.12 virtual environment in `.venv` and installs the packages listed in `requirements.txt`.

Make sure [`uv`](https://docs.astral.sh/uv/) is installed and available on your `PATH`.

From the repository root, run:

```bash
bash create_env.sh
```

After the installation finishes, activate the environment:

```bash
source .venv/bin/activate
```

When using Jupyter notebooks, select the Python interpreter from `.venv`.
