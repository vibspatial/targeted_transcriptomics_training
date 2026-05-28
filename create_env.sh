# Use uv sync so pyproject.toml, including [tool.uv] dependency overrides, is
# the single source of truth for the environment.
UV_PROJECT_ENVIRONMENT=.venv uv sync --python 3.12 --locked
