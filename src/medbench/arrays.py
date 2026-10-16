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


def extract_slice(
    array: npt.NDArray[np.generic],
    axis: int,
    index: int,
) -> npt.NDArray[np.generic]:
    """Extract a 2D slice from a 3D NumPy array."""
    if not isinstance(array, np.ndarray):
        raise TypeError("array must be a NumPy array")

    if array.ndim != 3:
        raise ValueError("array must be exactly 3D")

    if isinstance(axis, (bool, np.bool_)) or not isinstance(axis, (int, np.integer)):
        raise TypeError("axis must be an integer")

    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1, or 2")

    if isinstance(index, (bool, np.bool_)) or not isinstance(index, (int, np.integer)):
        raise TypeError("index must be an integer")

    axis = int(axis)
    index = int(index)

    if index < 0 or index >= array.shape[axis]:
        raise IndexError("index is out of range for the selected axis")

    if axis == 0:
        return array[index, :, :]

    if axis == 1:
        return array[:, index, :]

    return array[:, :, index]
