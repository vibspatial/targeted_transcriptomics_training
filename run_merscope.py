import os
import time

import matplotlib.pyplot as plt
import scanpy as sc
import sparrow as sp
import torch
from cellpose import models
from sparrow.image import cellpose_callable
from sparrow.image._image import _get_spatial_element
from sparrow.utils.pylogger import get_pylogger

log = get_pylogger(__name__)

# need to change these paths to vsc Leuven paths.
input_dir = "/data/gent/vo/001/gvo00163/vsc40523/VIB/DATA/merscope/0.0.1/transcriptomics/vizgen/mouse/Liver1Slice1"
output_dir = "/data/gent/vo/001/gvo00163/vsc40523/VIB/DATA/merscope"

crop = True

log.info("Start creating sdata.")

sdata = sp.io.merscope(
    path=input_dir,
    to_coordinate_system="global",
    z_layers=[
        3,
    ],
    backend=None,
    transcripts=True,
    mosaic_images=True,
    do_3D=False,
    z_projection=False,
    image_models_kwargs={"scale_factors": None},
    filter_gene_names=["blank"],
    output=os.path.join(output_dir, "sdata_merscope_crop.zarr"),
)

log.info("End creating sdata.")

# from spatialdata import read_zarr
# sdata = read_zarr(os.path.join(output_dir, "sdata_merscope_crop.zarr"))

log.info("Start cleaning.")
start = time.time()

sdata = sp.im.min_max_filtering(
    sdata,
    img_layer="mouse_Liver1Slice1_z3_global",
    output_layer="min_max_filtered",
    size_min_max_filter=[85, 135],
    overwrite=True,
)
sdata = sp.im.enhance_contrast(
    sdata,
    img_layer="min_max_filtered",
    output_layer="clahe",
    contrast_clip=[13.5, 18.5],
    crd=[20000, 40000, 20000, 40000] if crop else None,
    chunks=5000,
    overwrite=True,
)

end = time.time()
log.info(f"Cleaning took {end-start}")

img_layer = "clahe"

gpu = True
device = "cuda"
model = models.CellposeModel(
    gpu=gpu, pretrained_model="cyto3", device=torch.device(device)
)

se = _get_spatial_element(sdata, layer=img_layer)

log.info("Start segmentation.")

start = time.time()


sdata = sp.im.segment(
    sdata,
    img_layer=img_layer,
    chunks=2048,
    depth=200,
    model=cellpose_callable,
    # parameters that will be passed to the callable _cellpose
    pretrained_model=model,
    diameter=100,
    flow_threshold=0.85,
    cellprob_threshold=-4,
    channels=[
        se.c.data.tolist().index("PolyT") + 1,
        se.c.data.tolist().index("DAPI") + 1,
    ],
    output_labels_layer="segmentation_mask",
    output_shapes_layer="segmentation_mask_boundaries",
    crd=[20000, 40000, 20000, 40000]
    if crop
    else None,  # region to segment [x_min, xmax, y_min, y_max],
    overwrite=True,
)


end = time.time()
log.info(f"Segmentation took {end-start}")

sp.pl.plot_shapes(
    sdata,
    shapes_layer="segmentation_mask_boundaries",
    img_layer=[img_layer],
    crd=[20000, 25000, 20000, 25000],
    figsize=(10, 10),
    output=os.path.join(output_dir, "segmentation.png"),
)

log.info("Start allocation.")

sdata = sp.tb.allocate(
    sdata=sdata,
    labels_layer="segmentation_mask",
    points_layer="transcripts_global",
    output_layer="table_transcriptomics",
    update_shapes_layers=False,
    overwrite=True,
)

log.info("End allocation.")

sp.pl.plot_shapes(
    sdata,
    img_layer="clahe",
    shapes_layer="segmentation_mask_boundaries",
    figsize=(10, 10),
    crd=[20000, 22000, 20000, 22000],
    table_layer="table_transcriptomics",
    column="Vwf",
    output=os.path.join(output_dir, "expression_Vwf"),
)


log.info("Start analyse genes left out.")

df = sp.pl.analyse_genes_left_out(
    sdata,
    labels_layer="segmentation_mask",
    table_layer="table_transcriptomics",
    points_layer="transcripts_global",
    output=os.path.join(output_dir, "analyse_genes_left_out"),
)

log.info("End analyse genes left out.")


log.info("Start preprocess.")

# Perform preprocessing.
sdata = sp.tb.preprocess_transcriptomics(
    sdata,
    labels_layer="segmentation_mask",
    table_layer="table_transcriptomics",
    output_layer="table_transcriptomics_preprocessed",  # write results to a new slot, we could also write to the same slot (when passing overwrite==True).
    min_counts=10,
    min_cells=5,
    size_norm=True,
    n_comps=50,
    overwrite=True,
    update_shapes_layers=False,
)

log.info("End preprocess.")

sp.pl.preprocess_transcriptomics(
    sdata,
    table_layer="table_transcriptomics_preprocessed",
    output=os.path.join(output_dir, "preprocess"),
)

log.info("Start filtering on size.")

sdata = sp.tb.filter_on_size(
    sdata,
    labels_layer="segmentation_mask",
    table_layer="table_transcriptomics_preprocessed",
    output_layer="table_transcriptomics_filter",
    min_size=500,
    max_size=100000,
    update_shapes_layers=False,
    overwrite=True,
)

log.info("End filtering on size.")

log.info("Start leiden clustering.")

sdata = sp.tb.leiden(
    sdata,
    labels_layer="segmentation_mask",
    table_layer="table_transcriptomics_filter",
    output_layer="table_transcriptomics_clustered",
    calculate_umap=True,
    calculate_neighbors=True,
    n_pcs=17,
    n_neighbors=35,
    resolution=1.0,
    rank_genes=True,
    key_added="leiden",
    overwrite=True,
)

log.info("End leiden clustering")

sc.pl.umap(
    sdata.tables["table_transcriptomics_clustered"], color=["leiden"], show=False
)
plt.savefig(os.path.join(output_dir, "leiden" + "_umap.png"), bbox_inches="tight")
plt.close()

sc.pl.rank_genes_groups(
    sdata.tables["table_transcriptomics_clustered"], n_genes=8, sharey=False, show=False
)
plt.savefig(os.path.join(output_dir, "rank_genes" + "_umap.png"), bbox_inches="tight")
plt.close()

sp.pl.plot_shapes(
    sdata,
    img_layer="clahe",
    table_layer="table_transcriptomics_clustered",
    column="leiden",
    shapes_layer="segmentation_mask_boundaries",
    alpha=1,
    linewidth=0,
    channel="DAPI",
    crd=[20000, 30000, 20000, 30000],
    output=os.path.join(output_dir, "leiden"),
)