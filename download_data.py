import argparse

import harpy as hp
from harpy.datasets.registry import get_registry
from loguru import logger

DATASETS = [
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/tumor.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/necrosis.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/ovary.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/fallopian_tube.geojson",  # Region annotation from Qupath
    "transcriptomics/xenium/Xenium_human_ovarian_cancer/training_march_2026/smooth_muscle.geojson",  # Region annotation from Qupath
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download data for the targeted transcriptomics training notebooks."
    )
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
    _ = hp.datasets.xenium_human_ovarian_cancer(
        training="checkpoint_1",
        path=args.cache_dir_path,
    )
    logger.info("Fetching Xenium ovarian cancer checkpoint_2.")
    _ = hp.datasets.xenium_human_ovarian_cancer(
        training="checkpoint_2", path=args.cache_dir_path
    )

    logger.info("Fetching VectraPolaris data.")
    _ = hp.datasets.vectra_example(
        path=args.cache_dir_path,
    )


if __name__ == "__main__":
    main()
