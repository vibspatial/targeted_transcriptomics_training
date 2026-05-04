# cellpose==3.1.1.3 pulls in numpy==2.0.2 on macOS, which does not build on Python 3.13.
uv venv .venv --python 3.12
source .venv/bin/activate

uv pip install -r requirements.txt
