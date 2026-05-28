# Use uv sync so pyproject.toml, including [tool.uv] dependency overrides, is
# the single source of truth for the environment.
UV_PROJECT_ENVIRONMENT=.venv uv sync --python 3.12 --locked

if [ -f ".venv/bin/activate" ]; then
    . .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    . .venv/Scripts/activate
else
    echo "Could not find virtual environment activation script."
    exit 1
fi
