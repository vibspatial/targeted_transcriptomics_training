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
