if (!require("pak", quietly = TRUE)) {
  install.packages("pak")
}
pak::pak("scverse/anndataR")
# install.packages("hdf5r")
# on macos, if issues with Matrix package and upgrading of seurat,
# please make sure fortran is installed https://github.com/R-macos/gcc-12-branch/releases

library(anndataR)
library(Seurat )

h5ad_path <- "/var/folders/q5/7yhs0l6d0x771g7qdbhvkvmr0000gp/T/adata.h5ad" # change this path.

adata <- read_h5ad(h5ad_path)
adata

# feature matrix:
adata$X

# obs column
adata$obs$cell_ID

# convert to SingleCellExperiment
sce <- adata$to_SingleCellExperiment()

# feature matrix
sce@assays@data$X

# obs column
sce$cell_ID

# convert to Seurat object
seurat_object <- adata$to_Seurat()

# obs column
seurat_object$cell_ID

# genes
seurat_object@assays$RNA

# feauture matrix
seurat_object@assays$RNA$counts












