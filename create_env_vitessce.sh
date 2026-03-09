uv venv .venv_harpy_vitessce --python 3.12
source .venv_harpy_vitessce/bin/activate
uv pip install "harpy_vitessce[vitessce] @ git+https://github.com/vibspatial/harpy_vitessce.git@main"
uv pip install jupyter
