import importlib
import os

import nbformat
import pyrootutils
import pytest
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor


def run_notebook(notebook_path, timeout=600):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    ep = ExecutePreprocessor(timeout=timeout, kernel_name="python3")
    try:
        ep.preprocess(nb, {"metadata": {"path": os.path.dirname(notebook_path)}})
    except CellExecutionError as e:
        raise RuntimeError(
            f"Error executing the notebook '{notebook_path}': {e}"
        ) from e


@pytest.mark.skipif(
    not importlib.util.find_spec("cellpose"),
    reason="requires the cellpose library",
)
@pytest.mark.parametrize(
    "notebook",
    [
        "0.get_data.ipynb",
        "1.sparrow_pipeline.ipynb",
    ],
)
def test_notebooks_sparrow_pipeline(notebook):
    root = str(pyrootutils.setup_root(os.getcwd(), dotenv=True, pythonpath=True))

    run_notebook(os.path.join(root, "", notebook))


@pytest.mark.skipif(
    not importlib.util.find_spec("cellpose"),
    reason="requires the cellpose library",
)
@pytest.mark.parametrize(
    "notebook",
    [
        "2.sparrow_pipeline_xenium.ipynb",
    ],
)
def test_notebooks_sparrow_pipeline_xenium(notebook):
    root = str(pyrootutils.setup_root(os.getcwd(), dotenv=True, pythonpath=True))

    run_notebook(os.path.join(root, "", notebook))


@pytest.mark.skipif(
    not importlib.util.find_spec("cellpose")
    or not importlib.util.find_spec("rioxarray"),
    reason="requires the cellpose library and the rioxarray library.",
)
@pytest.mark.parametrize(
    "notebook",
    [
        "4.sparrow_pipeline_merscope.ipynb",
    ],
)
def test_notebooks_sparrow_pipeline_merscope(notebook):
    root = str(pyrootutils.setup_root(os.getcwd(), dotenv=True, pythonpath=True))

    run_notebook(os.path.join(root, "", notebook))


@pytest.mark.skipif(
    not importlib.util.find_spec("sopa"),
    reason="requires the sopa library",
)
@pytest.mark.parametrize(
    "notebook",
    [
        "3.xenium_explorer.ipynb",
    ],
)
def test_notebooks_xenium_explorer(notebook):
    root = str(pyrootutils.setup_root(os.getcwd(), dotenv=True, pythonpath=True))

    run_notebook(os.path.join(root, "", notebook))


@pytest.mark.parametrize(
    "notebook",
    [
        "5.explore_sdata.ipynb",
    ],
)
def test_notebooks_explore_sdata(notebook):
    root = str(pyrootutils.setup_root(os.getcwd(), dotenv=True, pythonpath=True))

    run_notebook(os.path.join(root, "", notebook))
