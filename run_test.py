import torch

from harpy.utils.pylogger import get_pylogger

log = get_pylogger(__name__)

log.info("test")
log.info(f"CUDA available: {torch.cuda.is_available()}")
