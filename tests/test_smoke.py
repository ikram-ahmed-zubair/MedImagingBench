"""Tests for the medbench package."""

import numpy as np
import pytest

import medbench
from medbench.arrays import get_array_info, get_volume_stats


def test_package_version() -> None:
    """Verify that the package exposes its expected version."""
    assert medbench.__version__ == "0.1.0"


def test_get_array_info() -> None:
    """Verify array shape, type, size, and memory information."""
    array = np.zeros((2, 3, 4), dtype=np.float32)

    info = get_array_info(array)

    assert info["shape"] == (2, 3, 4)
    assert info["ndim"] == 3
    assert info["dtype"] == "float32"
    assert info["size"] == 24
    assert info["memory_bytes"] == 96


def test_get_volume_stats() -> None:
    """Verify intensity statistics for a 3D volume."""
    array = np.arange(1, 9, dtype=np.float32).reshape(2, 2, 2)

    stats = get_volume_stats(array)

    assert stats["count"] == 8
    assert stats["min"] == 1.0
    assert stats["max"] == 8.0
    assert stats["mean"] == 4.5
    assert stats["median"] == 4.5
    assert np.isclose(stats["std"], np.std(array))


def test_get_volume_stats_rejects_empty_array() -> None:
    """Verify that empty arrays are rejected."""
    with pytest.raises(ValueError, match="must not be empty"):
        get_volume_stats(np.array([]))


def test_get_volume_stats_rejects_non_finite_values() -> None:
    """Verify that NaN and infinity are rejected."""
    with pytest.raises(ValueError, match="finite values"):
        get_volume_stats(np.array([1.0, np.nan]))


def test_get_volume_stats_rejects_text() -> None:
    """Verify that non-numeric arrays are rejected."""
    with pytest.raises(TypeError, match="numeric values"):
        get_volume_stats(np.array(["CT", "MRI"]))
