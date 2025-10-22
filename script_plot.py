# Below parameters can be changed
import uuid

import dask.array as da
import matplotlib.pyplot as plt
import numpy as np
import spatialdata_plot  # noqa: F401
from matplotlib.colors import Normalize
from spatialdata import bounding_box_query
from spatialdata.transformations import get_transformation

import harpy as hp
from harpy.image._image import _get_spatial_element

sdata = hp.datasets.resolve_example()


img_layer = "raw_image"
labels_layer = "segmentation_mask"


channels_to_plot = [
    0,
    # "CD14",
    # "CD3",
]

dpi = 200
figsize = (10, 10)
scale = "scale3"  # set to scale0 for full resolution, will be slower
crd = [0, 6000, 0, 5000]  # set to None if you do not want to crop


se = _get_spatial_element(sdata, layer=img_layer)
channels = se.c.data

assert set(channels_to_plot).issubset(channels), (
    f"Not all channels could be found in layer '{img_layer}'. Please choose from: {channels}."
)

img_layer_crop = f"{img_layer}_{uuid.uuid4()}"
labels_layer_crop = f"{labels_layer}_{uuid.uuid4()}"

if crd is not None:
    sdata[img_layer_crop] = bounding_box_query(
        sdata[img_layer],
        axes=["x", "y"],
        min_coordinate=[crd[0], crd[2]],
        max_coordinate=[crd[1], crd[3]],
        target_coordinate_system=list(get_transformation(se, get_all=True).keys())[0],
    )

    sdata[labels_layer_crop] = bounding_box_query(
        sdata[labels_layer],
        axes=["x", "y"],
        min_coordinate=[crd[0], crd[2]],
        max_coordinate=[crd[1], crd[3]],
        target_coordinate_system=list(get_transformation(se, get_all=True).keys())[0],
    )

if len(channels_to_plot) > 1:
    axes = plt.subplots(len(channels_to_plot), 1, figsize=figsize)[1].flatten()
else:
    axes = [plt.subplots(len(channels_to_plot), 1, figsize=figsize)[1]]

for c, ax in zip(channels_to_plot, axes, strict=False):
    c_id = np.where(channels == c)[0].item()
    vmax = da.percentile(
        se.data[c_id].flatten(), q=99
    ).compute()  # clip to 99% percentile
    norm = Normalize(vmax=vmax, clip=True)
    indices_channels_for_segmentation = [
        np.where(channels == _channel)[0].item() for _channel in channels_to_plot
    ]

    sdata.pl.render_images(
        img_layer if crd is None else img_layer_crop,
        channel=c,
        cmap="grey",
        norm=norm,
        scale=scale,
    ).pl.render_labels(
        labels_layer if crd is None else labels_layer_crop,
        scale=scale,
        fill_alpha=0.2,
        outline_alpha=0.3,
    ).pl.show(
        title=str(c),
        ax=ax,
        colorbar=False,
        dpi=dpi,
        return_ax=False,
    )
    ax.tick_params(
        left=False, bottom=False, labelleft=False, labelbottom=False
    )  # to remove ticks

if crd is not None:
    del sdata[img_layer_crop]
    del sdata[labels_layer_crop]
