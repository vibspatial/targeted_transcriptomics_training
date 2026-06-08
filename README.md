# Spatial Omics Summer School

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

If you already cloned the repository, update it from inside the project directory:

```bash
git pull
```

## 2. Install uv

Make sure `uv` is installed and available on your `PATH`.

Check with:

```bash
uv --version
```

## 3. Create or sync the environment

From the repository root, create or sync the Python 3.12 course environment by running:

```bash
uv sync --python 3.12 --locked
```

This creates or updates the project environment at:

```text
.venv
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
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
. .\.venv\Scripts\Activate.ps1
```

On Windows Command Prompt:

```bat
.venv\Scripts\activate.bat
```

On Windows Git Bash:

```bash
source .venv/Scripts/activate
```

## 5. Download the course data

After activating the environment, download the datasets and model weights used in the notebooks.

On macOS, Linux, or WSL, run:

```bash
python download_data.py
```

On Windows, always set the cache directory explicitly to `C:/hp_cache`:

```powershell
python download_data.py --cache-dir-path C:/hp_cache
```

Use a short cache path on Windows to avoid path-length errors when downloading and unpacking nested dataset files. Some Windows setups still enforce the traditional 260-character path limit unless long-path support is enabled.

This downloads the course data into the selected cache directory. It also downloads the InstanSeg model and the Cellpose `cyto3` and `nuclei` models.

## 6. Use the environment in VS Code

Open this repository folder in VS Code.

Open the Command Palette and run `Python: Select Interpreter`. Select the interpreter from `.venv`.

On macOS, Linux, or WSL, choose:

```text
.venv/bin/python
```

On Windows, choose:

```text
.venv\Scripts\python.exe
```

When opening a notebook, click the kernel selector in the top-right corner and choose the same `.venv` environment. It will be named `targeted-transcriptomics-training`.

## Updating dependencies

For normal course use, do not edit `uv.lock`.

If dependencies in `pyproject.toml` are changed intentionally, update the lockfile with:

```bash
uv lock
```

Then recreate or sync the environment with:

```bash
uv sync --python 3.12 --locked
```
