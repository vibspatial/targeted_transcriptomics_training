import argparse
import logging


class _SuppressHarpyMacsimaWarnings(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        suppressed_log_messages = {
            "Module 'bioio' is not installed. Install it with `pip install bioio` to use `harpy.io.macsima`.",
            "Module 'bioio-ome-tiff' is not installed. Install it with `pip install bioio-ome-tiff` to use `harpy.io.macsima`.",
        }
        message = record.getMessage()
        return message not in suppressed_log_messages and not message.startswith("no parent found for ")


spatialdata_logger = logging.getLogger("spatialdata._logging")
spatialdata_logger.addFilter(_SuppressHarpyMacsimaWarnings())
ome_zarr_logger = logging.getLogger("ome_zarr.reader")
ome_zarr_logger.addFilter(_SuppressHarpyMacsimaWarnings())

import harpy as hp
from cellpose import models
from harpy.datasets.registry import get_registry
from instanseg import InstanSeg
from loguru import logger

from summer_school_datasets import xenium_human_ovarian_cancer_course

DATASETS = [
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/tumor.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/necrosis.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/ovary.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/fallopian_tube.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/smooth_muscle.geojson",  # Region annotation from Qupath
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download data for the spatial omics training notebooks.")
    parser.add_argument(
        "--cache_dir_path",
        "--cache-dir-path",
        default=None,
        help="Directory to use as the data cache. Defaults to the OS-specific cache directory.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    registry = get_registry(path=args.cache_dir_path)

    for item in DATASETS:
        logger.info(f"Fetching {item}.")
        registry.fetch(item)

    logger.info("Fetching Xenium ovarian cancer checkpoint_1.")
    _ = xenium_human_ovarian_cancer_course(
        checkpoint="checkpoint_1",
        path=args.cache_dir_path,
    )
    logger.info("Fetching Xenium ovarian cancer checkpoint_2.")
    _ = xenium_human_ovarian_cancer_course(
        checkpoint="checkpoint_2",
        path=args.cache_dir_path,
    )

    logger.info("Fetching VectraPolaris data.")
    _ = hp.datasets.vectra_example(
        path=args.cache_dir_path,
    )

    logger.info("Fetching MACSima data.")

    _ = hp.datasets.macsima_colorectal_carcinoma_course(
        checkpoint="checkpoint_1",
        path=args.cache_dir_path,
    )

    _ = hp.datasets.macsima_colorectal_carcinoma_course(
        checkpoint="checkpoint_2",
        path=args.cache_dir_path,
    )

    logger.info("Fetching Instanseg model.")
    _ = InstanSeg("fluorescence_nuclei_and_cells", verbosity=1, device="cpu")

    logger.info("Fetching Cellpose models.")

    _ = models.CellposeModel(model_type="cyto3")
    _ = models.CellposeModel(model_type="nuclei")


if __name__ == "__main__":
    main()
