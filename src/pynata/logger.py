import logging
import sys

logger = logging.getLogger("pynata")
logger.addHandler(logging.StreamHandler(sys.stderr))


__all__ = ["logger"]
