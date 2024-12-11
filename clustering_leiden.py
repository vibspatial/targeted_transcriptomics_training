import argparse
import os
from pathlib import Path

import matplotlib.pyplot as plt
import scanpy as sc
import harpy as hp
from spatialdata import read_zarr

from harpy.utils.pylogger import get_pylogger

log = get_pylogger(__name__)


def main(sdata_path: str | Path, output_dir: str | Path):
    sdata = read_zarr(sdata_path)

    sdata = hp.tb.leiden(
        sdata,
        labels_layer="segmentation_mask",
        table_layer="table_transcriptomics_filter",
        output_layer="table_transcriptomics_clustered",
        calculate_umap=True,
        calculate_neighbors=True,
        n_pcs=10,
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

    plt.savefig(
        os.path.join(output_dir, "leiden_redo" + "_umap.png"), bbox_inches="tight"
    )
    plt.close()

    sc.pl.rank_genes_groups(
        sdata.tables["table_transcriptomics_clustered"],
        n_genes=8,
        sharey=False,
        show=False,
    )
    plt.savefig(
        os.path.join(output_dir, "rank_genes_redo" + "_umap.png"), bbox_inches="tight"
    )
    plt.close()

    hp.pl.plot_shapes(
        sdata,
        img_layer="clahe",
        table_layer="table_transcriptomics_clustered",
        column="leiden",
        shapes_layer="segmentation_mask_boundaries",
        alpha=1,
        linewidth=0,
        channel="DAPI",
        crd=[20000, 30000, 20000, 30000],
        output=os.path.join(output_dir, "leiden_redo"),
    )


if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Set the output directory.")

    # Add arguments
    parser.add_argument("--sdata_path", type=str, help="Path to sdata.", required=True)
    parser.add_argument(
        "--output_dir", type=str, help="Output directory", required=True
    )

    # Parse arguments
    args = parser.parse_args()

    main(sdata_path=args.sdata_path, output_dir=args.output_dir)
