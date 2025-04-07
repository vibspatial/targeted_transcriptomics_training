from __future__ import annotations

import os
from pathlib import Path

import pooch
from pooch import Pooch
from harpy import __version__
from spatialdata import SpatialData, read_zarr
from spatialdata.models import Image2DModel
from harpy.datasets.registry import get_ome_registry

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
            "transcriptomics/resolve/mouse/sdata_resolve_spatial_training.zarr.zip": "162a698b86180535955c2979948cb0d7fccef43eb8396452f6e3b28053d41dd3",
            "transcriptomics/xenium/Xenium_V1_humanLung_Cancer_FFPE/sdata_9ee21b52-8472-4930-a553-73e52ef4743e.zarr.zip": "a92ec13183f64077cb36ebca313907c342b5dc486f0e8592c6be9333ae923db8",
            "transcriptomics/xenium/Xenium_V1_humanLung_Cancer_FFPE/sdata.zarr.zip": "a92ec13183f64077cb36ebca313907c342b5dc486f0e8592c6be9333ae923db8",
        },
    )
    return registry


def sdata_resolve(path: str | Path = None, output: str | Path = None) -> SpatialData:
    """Example transcriptomics dataset"""
    # Fetch and unzip the file
    registry = get_registry(path=path)
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


def sdata_xenium(path: str | Path = None, output: str | Path = None) -> SpatialData:
    """Example transcriptomics dataset"""
    # Fetch and unzip the file
    registry = get_registry(path)
    unzip_path = registry.fetch(
        "transcriptomics/xenium/Xenium_V1_humanLung_Cancer_FFPE/sdata.zarr.zip",
        processor=pooch.Unzip(),
    )
    sdata = read_zarr(os.path.commonpath(unzip_path))
    sdata.path = None
    if output is not None:
        sdata.write(output)
        sdata = read_zarr(output)
    return sdata


def sdata_vectra(path: str | Path = None, output: str | Path = None) -> SpatialData:
    from harpy.datasets.proteomics import read_tifffile

    registry = get_ome_registry(path)
    path = registry.fetch(
        "Vectra-QPTIFF/perkinelmer/PKI_fields/LuCa-7color_%5b13860,52919%5d_1x1component_data.tif"
    )

    input_data, physical_pixel_size_x, physical_pixel_size_y = read_tifffile(path)
    assert physical_pixel_size_x == physical_pixel_size_y
    # TODO use pixel metadata to set the pixel size
    sdata = SpatialData(images={"image": Image2DModel.parse(input_data, dims="cyx")})
    sdata.path = None

    if output is not None:
        sdata.write(output)
        sdata = read_zarr(output)

    return sdata
