from __future__ import annotations

import os
from pathlib import Path

import pooch
from pooch import Pooch
from sparrow import __version__
from spatialdata import SpatialData, read_zarr

BASE_URL = "https://objectstor.vib.be/spatial-hackathon-public/sparrow/public_datasets"


def get_registry(path: str | Path | None = None) -> Pooch:
    """
    Get the Pooch registry

    Parameters
    ----------
    path
        If None, example data will be downloaded in the default cache folder of your os. Set this to a custom path, to change this behaviour.

    Returns
    -------
    Pooch registry.
    """
    registry = pooch.create(
        path=pooch.os_cache("sparrow") if path is None else path,
        base_url=BASE_URL,
        version=__version__,
        registry={
            "transcriptomics/resolve/mouse/sdata_resolve_spatial_training.zarr.zip": "1d8dab6bbee4c94e6f7efeda6ae320e5e905266f0777fce959810e6ff07fe0b5",
        },
    )
    return registry


def sdata_resolve(output: str | Path = None) -> SpatialData:
    """Example transcriptomics dataset"""
    # Fetch and unzip the file
    registry = get_registry()
    unzip_path = registry.fetch(
        "transcriptomics/resolve/mouse/sdata_resolve_spatial_training.zarr.zip",
        processor=pooch.Unzip(),
    )
    sdata = read_zarr(os.path.commonpath(unzip_path))
    sdata.path = None
    if output is not None:
        sdata.write(output)
        sdata = read_zarr(output)
    return sdata