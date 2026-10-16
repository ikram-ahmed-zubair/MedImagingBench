def test_package_imports() -> None:
    import project_name

    assert project_name.__version__ == "0.1.0"
