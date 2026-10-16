"""Smoke tests for the medbench package."""

import medbench


def test_package_version() -> None:
    """Verify that the package exposes its expected version."""
    assert medbench.__version__ == "0.1.0"