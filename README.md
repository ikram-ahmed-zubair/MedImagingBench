# MedImagingBench

An evolving Python project for learning and building reproducible medical-imaging
software. Its current scope and validation are limited to the code and tests in
this repository.

## Status

Early-stage learning and research code. A feature is not considered validated
merely because it is planned or present; see the tests and validation evidence.

## Quickstart

```bash
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest -q
```

## Local checks

From the repository root in PowerShell, run all project checks:

```powershell
.\scripts\check.ps1
```

The script runs tests, Ruff lint, and Ruff formatting checks using this
repository's `.venv`. GitHub Actions runs the same checks on pushes and pull
requests.

## Usage

Document one minimal command and expected output. Example:

```bash
python scripts/run_reproducible_demo.py --config configs/example.yaml
```

## Reproducibility

Record data version/licence, split strategy, config, random seed, package versions, and hardware when results depend on them. Never place patient-identifiable data in this repository.

## Validation

- Tests:
- Reference case / baseline:
- Known limitations:

## Repository map

Explain important directories when they exist.

## Data and privacy

State where users obtain data, applicable licence/access rules, and the fact that data are not included if they are excluded.

## Citation

Explain how to cite the code or associated paper once a citation record exists.

## License

Choose an explicit licence after checking dependencies, data terms, and intended reuse.
