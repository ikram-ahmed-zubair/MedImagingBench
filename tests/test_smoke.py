"""Smoke tests for the medbench package."""

import numpy as np
import pytest

import medbench
from medbench.arrays import (
    extract_slice,
    get_array_info,
    get_volume_stats,
)


def test_package_version():
    """Check that the package exposes the expected version."""
    assert medbench.__version__ == "0.1.0"


def test_get_array_info():
    """Check basic array metadata."""
    array = np.zeros((2, 3, 4), dtype=np.float32)

    info = get_array_info(array)

    assert info["shape"] == (2, 3, 4)
    assert info["ndim"] == 3
    assert info["dtype"] == "float32"
    assert info["size"] == 24
    assert info["memory_bytes"] == 96


def test_get_volume_stats():
    """Check intensity statistics for a numeric array."""
    array = np.arange(1, 9, dtype=np.float32).reshape(2, 2, 2)

    stats = get_volume_stats(array)

    assert stats["count"] == 8
    assert stats["min"] == 1.0
    assert stats["max"] == 8.0
    assert stats["mean"] == pytest.approx(4.5)
    assert stats["std"] == pytest.approx(2.29128784747792)
    assert stats["median"] == pytest.approx(4.5)


def test_get_volume_stats_rejects_empty_array():
    """An empty array must raise ValueError."""
    array = np.array([], dtype=np.float32)

    with pytest.raises(ValueError, match="must not be empty"):
        get_volume_stats(array)


def test_get_volume_stats_rejects_non_finite_values():
    """NaN and infinity must be rejected."""
    for value in (np.nan, np.inf, -np.inf):
        array = np.array([1.0, value])

        with pytest.raises(ValueError, match="finite"):
            get_volume_stats(array)


def test_get_volume_stats_rejects_text_array():
    """Text arrays must raise TypeError."""
    array = np.array(["one", "two"])

    with pytest.raises(TypeError, match="numeric"):
        get_volume_stats(array)


def test_extract_slice_axis_0():
    """Extract a 2D slice along axis 0."""
    volume = np.arange(24).reshape(2, 3, 4)

    result = extract_slice(volume, axis=0, index=1)

    np.testing.assert_array_equal(result, volume[1, :, :])
    assert result.shape == (3, 4)


def test_extract_slice_axis_1():
    """Extract a 2D slice along axis 1."""
    volume = np.arange(24).reshape(2, 3, 4)

    result = extract_slice(volume, axis=1, index=1)

    np.testing.assert_array_equal(result, volume[:, 1, :])
    assert result.shape == (2, 4)


def test_extract_slice_axis_2():
    """Extract a 2D slice along axis 2."""
    volume = np.arange(24).reshape(2, 3, 4)

    result = extract_slice(volume, axis=2, index=2)

    np.testing.assert_array_equal(result, volume[:, :, 2])
    assert result.shape == (2, 3)


def test_extract_slice_rejects_non_3d_array():
    """A 2D array must be rejected."""
    volume = np.zeros((3, 4))

    with pytest.raises(ValueError, match="exactly 3D"):
        extract_slice(volume, axis=0, index=0)


def test_extract_slice_rejects_invalid_axis():
    """An axis outside 0, 1, and 2 must be rejected."""
    volume = np.zeros((2, 3, 4))

    with pytest.raises(ValueError, match="axis must be 0, 1, or 2"):
        extract_slice(volume, axis=3, index=0)


def test_extract_slice_rejects_out_of_range_index():
    """An index beyond the axis length must be rejected."""
    volume = np.zeros((2, 3, 4))

    with pytest.raises(IndexError, match="out of range"):
        extract_slice(volume, axis=2, index=4)


def test_extract_slice_rejects_negative_index():
    """Negative indices are deliberately rejected."""
    volume = np.zeros((2, 3, 4))

    with pytest.raises(IndexError, match="out of range"):
        extract_slice(volume, axis=0, index=-1)
