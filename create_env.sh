# cellpose==3.1.1.3 pulls in numpy==2.0.2 on macOS, which does not build on Python 3.13.
uv venv .venv --python 3.12
source .venv/bin/activate

uv pip install 'harpy-analysis[extra,napari] @ git+https://github.com/saeyslab/harpy.git@main'
uv pip install "harpy_vitessce @ git+https://github.com/vibspatial/harpy_vitessce.git@main"
uv pip install squidpy
uv pip install cellpose==3.1.1.3
uv pip install jupyter
uv pip install mofax
uv pip install mofapy2
uv pip install bokeh

