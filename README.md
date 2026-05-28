# Spatial Omics Training

<p align="center">
  <a href="https://spatialdata.scverse.org/">
    <img src="https://raw.githubusercontent.com/scverse/spatialdata/main/docs/_static/img/spatialdata_horizontal.png" alt="SpatialData" height="120">
  </a>
  <br>
  <img src="img/logo-plus.svg" alt="plus" height="32">
  <br>
  <a href="https://github.com/saeyslab/harpy">
    <img src="https://raw.githubusercontent.com/saeyslab/harpy/main/docs/_static/img/logo.png" alt="Harpy" height="170">
  </a>
</p>

<br>

This repository contains course material for the [Spatial Omics Summer School](https://www.vibconferences.be/events/spatial-omics-summer-school). The notebooks guide participants through working with [`SpatialData`](https://spatialdata.scverse.org/) objects, targeted transcriptomics data and spatial proteomics data.

The tutorials use [Harpy](https://github.com/saeyslab/harpy) for spatial omics analysis workflows and [napari-harpy](https://github.com/vibspatial/napari-harpy) for interactive inspection and visualization in napari.

# Installation

This project uses [`uv`](https://docs.astral.sh/uv/) to manage the Python environment.

Dependencies are defined in `pyproject.toml` and locked in `uv.lock`. Use the lockfile for the course environment so everyone gets the same package versions.

## 1. Get the repository

Clone this repository and move into the project directory:

```bash
git clone https://github.com/vibspatial/targeted_transcriptomics_training.git
cd targeted_transcriptomics_training
```

## 2. Install uv

Make sure `uv` is installed and available on your `PATH`.

Check with:

```bash
uv --version
```

## 3. Create the environment

From the repository root, run this on macOS, Linux, WSL, or Git Bash:

```bash
bash create_env.sh
```

On Windows PowerShell, run:

```powershell
.\create_env.ps1
```

The script creates or updates a Python 3.12 environment at:

```text
.venv
```

Internally, it runs:

```bash
UV_PROJECT_ENVIRONMENT=.venv uv sync --python 3.12 --locked
```

This means:

- `.venv` is created if it does not exist
- packages are installed from `uv.lock`
- `uv.lock` is not modified
- the command fails if `pyproject.toml` and `uv.lock` are out of sync

## 4. Activate the environment

On macOS, Linux, or WSL:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
. .\.venv\Scripts\Activate.ps1
```

On Windows Git Bash:

```bash
source .venv/Scripts/activate
```

## 5. Use the environment in VS Code

Open this repository in VS Code.

Select the Python interpreter from `.venv`:

```text
.venv/bin/python
```

On Windows, choose:

```text
.venv\Scripts\python.exe
```

When opening a notebook, click the kernel selector in the top-right corner and choose the same `.venv` interpreter.

## Updating dependencies

For normal course use, do not edit `uv.lock`.

If dependencies in `pyproject.toml` are changed intentionally, update the lockfile with:

```bash
uv lock
```

Then recreate or sync the environment with:

```bash
bash create_env.sh
```

On Windows PowerShell, use:

```powershell
.\create_env.ps1
```
