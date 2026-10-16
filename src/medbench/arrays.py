"""Array utilities for biomedical imaging."""

import numpy as np
import numpy.typing as npt


def get_array_info(
    array: npt.NDArray[np.generic],
) -> dict[str, object]:
    """Return basic information about a NumPy array."""
    return {
        "shape": array.shape,
        "ndim": array.ndim,
        "dtype": str(array.dtype),
        "size": array.size,
        "memory_bytes": array.nbytes,
    }


def get_volume_stats(
    array: npt.NDArray[np.generic],
) -> dict[str, int | float]:
    """Return basic intensity statistics for a non-empty numeric array."""
    if not np.issubdtype(array.dtype, np.number):
        raise TypeError("array must contain numeric values")

    if np.issubdtype(array.dtype, np.complexfloating):
        raise TypeError("array must contain real numeric values")

    if array.size == 0:
        raise ValueError("array must not be empty")

    if not np.all(np.isfinite(array)):
        raise ValueError("array must contain only finite values")

    return {
        "count": int(array.size),
        "min": float(np.min(array)),
        "max": float(np.max(array)),
        "mean": float(np.mean(array)),
        "std": float(np.std(array)),
        "median": float(np.median(array)),
    }
