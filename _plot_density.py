import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from harpy.utils._keys import _GENES_KEY
from scipy.ndimage import gaussian_filter
from spatialdata import SpatialData


def plot_density(
    sdata: SpatialData,
    points_layer: str = None,
    name_gene_column: str | None = _GENES_KEY,
    genes: str | list[str] | None = None,
    table_layer: str = None,
    bin_size: float | None = None,
    smooth_sigma: float | None = None,
    cmap: str = "viridis",
    figsize: tuple = (8, 8),
    crd: tuple[int, int, int, int] | None = None,
):
    """
    Plot transcript density from a SpatialData points layer or plot cell density from a SpatialData table layer. Exactly one of `points_layer` or `table_layer` must be provided.

    Parameters
    ----------
    sdata
        SpatialData object containing the points layer or table layer.
    points_layer
        Points layer to plot from `sdata.points`.
    name_gene_column
        Column in the `points_layer` that stores the genes.
    genes
        Gene or list of genes to visualize. If not provide, will plot a density map of all transcripts.
    table_layer
        Table layer to plot from `sdata.tables`. Must contain obsm["spatial"].
    bin_size
        Width of a bin
    smooth_sigma
        Gaussian smoothing sigma. Note that this slightly misrepresents the data. If None, no smoothing applied.
    cmap
        Matplotlib colormap.
    crd
        The coordinates for a region of interest in the format `(xmin, xmax, ymin, ymax)`.
    """

    if bin_size is None:
        raise ValueError("`bin_size` must be specified.")

    if (points_layer is None and table_layer is None) or (
        points_layer is not None and table_layer is not None
    ):
        raise ValueError("Specify exactly one of `points_layer` or `table_layer`.")

    # Load transcripts
    if points_layer is not None:
        # TODO we should first subset the genes and then run compute
        df = sdata.points[points_layer].compute()

        if genes is not None:
            if name_gene_column is None:
                raise ValueError(
                    "name_gene_column must be provided if filtering genes."
                )

            if isinstance(genes, str):
                genes = [genes]

            df = df[df[name_gene_column].isin(genes)]

            if df.empty:
                raise ValueError("No transcripts found for specified gene(s).")

        label = "Transcript Count"
        title = "Transcript Density"

    elif table_layer is not None:
        coords = sdata.tables[table_layer].obsm["spatial"]
        df = pd.DataFrame(coords, columns=["x", "y"])

        label = "Cell Count"
        title = "Cell Density"

    if crd is not None:
        xmin, xmax, ymin, ymax = crd
        df = df[
            (df["x"] >= xmin)
            & (df["x"] <= xmax)
            & (df["y"] >= ymin)
            & (df["y"] <= ymax)
        ]
        if df.empty:
            raise ValueError("No data found in specified region.")
    else:
        xmin, xmax = df["x"].min(), df["x"].max()
        ymin, ymax = df["y"].min(), df["y"].max()

    x = df["x"].to_numpy()
    y = df["y"].to_numpy()

    # Create 2D histogram
    x_edges = np.arange(xmin, xmax + bin_size, bin_size)
    y_edges = np.arange(ymin, ymax + bin_size, bin_size)

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=[x_edges, y_edges])

    if smooth_sigma is not None:
        heatmap = gaussian_filter(heatmap, sigma=smooth_sigma)

    fig, ax = plt.subplots(figsize=figsize)

    im = ax.imshow(
        heatmap.T,
        origin="lower",
        cmap=cmap,
        extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
    )

    cbar = fig.colorbar(im, ax=ax, shrink=0.75)
    cbar.set_label(label, fontsize=12)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("y", fontsize=12)
    ax.set_aspect("equal")
    ax.invert_yaxis()

    plt.tight_layout()
    plt.show()
