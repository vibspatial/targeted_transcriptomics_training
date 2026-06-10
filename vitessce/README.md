# Vitessce Hands-On Environment

The main course environment pins `spatialdata==0.7.2`. Current `harpy-vitessce`
requires a newer SpatialData stack, so the Vitessce notebooks use a separate
environment managed from this directory.

From the repository root, create or sync the Vitessce environment with:

```bash
cd vitessce
uv sync --python 3.12 --locked
```

Activate it on macOS, Linux, or WSL:

```bash
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
. .\.venv\Scripts\Activate.ps1
```

Then select this environment as the notebook kernel when running the Vitessce
notebooks in this directory.
