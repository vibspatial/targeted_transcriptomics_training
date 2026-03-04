uv venv .venv_harpy --python 3.13
source .venv_harpy/bin/activate

uv pip install 'harpy-analysis[extra] @ git+https://github.com/saeyslab/harpy.git@main'
uv pip install 'harpy-analysis[napari] @ git+https://github.com/saeyslab/harpy.git@main'
uv pip install squidpy
uv pip install cellpose==3.1.1.3
