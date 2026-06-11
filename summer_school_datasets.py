from __future__ import annotations

import os
from pathlib import Path
from typing import Literal

import pooch
from pooch import Pooch
from spatialdata import SpatialData, read_zarr

# from harpy import __version__
__version__ = "0.0.1"  # Do not automatically update dataset Cache for each release, because it downloads a lot of data.

BASE_URL = "https://objectstor.vib.be/spatial-hackathon-public/sparrow/public_datasets"


def get_registry_summer_school(path: str | Path | None = None) -> Pooch:
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
        env="HARPY_POOCH_CACHE",
        registry={
            "transcriptomics/xenium/Xenium_human_ovarian_cancer/summer_school_2026/sdata_xe_11_6_1.zarr.zip": "f1318ac482ba2881ca8f3cb6dca402051cd269f5c724580e6c93bb35426e0a64",
            "transcriptomics/xenium/Xenium_human_ovarian_cancer/summer_school_2026/sdata_xe_11_6_2.zarr.zip": "3d41c87a01673abf468ea662f4b34ca40909ff69a746149204ea0f17e15bf351",
        },
    )
    return registry


def xenium_human_ovarian_cancer_course(
    checkpoint: Literal["checkpoint_1", "checkpoint_2"],
    output: str | Path | None = None,
    path: str | Path | None = None,
) -> SpatialData:
    """
    Human ovarian cancer Xenium course dataset.

    Parameters
    ----------
    checkpoint
        Course checkpoint to load. ``"checkpoint_1"`` loads the first checkpoint and
        ``"checkpoint_2"`` loads the second checkpoint.
    output
        The path where the resulting `SpatialData` object will be backed. If `None`, it will not be backed to a Zarr store.
    path
        If `None`, the example data will be downloaded into the default cache
        directory for your OS. Provide a custom path to change this behavior.

    Returns
    -------
    A SpatialData object.
    """
    checkpoints = {
        "checkpoint_1": "transcriptomics/xenium/Xenium_human_ovarian_cancer/summer_school_2026/sdata_xe_11_6_1.zarr.zip",
        "checkpoint_2": "transcriptomics/xenium/Xenium_human_ovarian_cancer/summer_school_2026/sdata_xe_11_6_2.zarr.zip",
    }
    if checkpoint not in checkpoints:
        raise ValueError(
            f"Invalid checkpoint {checkpoint!r}. Expected one of {', '.join(repr(key) for key in checkpoints)}."
        )

    registry = get_registry_summer_school(path)
    unzip_path = registry.fetch(checkpoints[checkpoint], processor=pooch.Unzip())
    sdata = read_zarr(os.path.commonpath(unzip_path))
    sdata.path = None
    if output is not None:
        sdata.write(output)
        sdata = read_zarr(output)
    return sdata
