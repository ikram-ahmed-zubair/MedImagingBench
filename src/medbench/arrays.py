
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
