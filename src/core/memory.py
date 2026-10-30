import gc
import logging

import torch

logger = logging.getLogger(__name__)


def flush_memory() -> None:
    """Run garbage collection and release the Apple Silicon GPU cache."""
    gc.collect()
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    logger.debug("Memory cache cleared.")


def get_memory_info() -> dict:
    """Return GPU memory usage in megabytes (Apple Silicon) or a CPU marker."""
    if not torch.backends.mps.is_available():
        return {"device": "CPU", "allocated_mb": 0, "cached_mb": 0}
    return {
        "device": "Apple Silicon GPU (MPS)",
        "allocated_mb": round(torch.mps.current_allocated_memory() / (1024**2), 2),
        "cached_mb": round(torch.mps.driver_allocated_memory() / (1024**2), 2),
    }


class VRAMGuard:
    """Context manager that releases cached memory after a block.

    The cache is not cleared before the block on purpose: clearing it forces the
    allocator to reserve the memory again on every image, which is slower.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        flush_memory()
