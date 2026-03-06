uv venv .venv_harpy --python 3.13
source .venv_harpy/bin/activate

uv pip install 'harpy-analysis[extra] @ git+https://github.com/saeyslab/harpy.git@main'
#uv pip install 'harpy-analysis[napari] @ git+https://github.com/saeyslab/harpy.git@main' # do not install napari on vib compute
uv pip install squidpy
uv pip install cellpose==3.1.1.3
uv pip install jupyter
uv pip install bokeh
