# MedImagingBench learning roadmap

Work through one phase at a time. Each phase is complete only when its acceptance
criteria are demonstrated; planned features are not evidence that they exist.

| Phase | Learning focus | Acceptance criteria |
|---|---|---|
| 1. Python and array foundations | NumPy, package structure, tests, Git, and reproducible checks | Existing package installs in the project environment; selected array behavior is explained and covered by deterministic tests for supported inputs and invalid cases; local checks pass. |
| 2. DICOM inventory | DICOM files, identifiers, and metadata | A small inventory produces validated metadata output; tests cover representative inputs and missing/invalid metadata without using patient-identifiable data. |
| 3. Volumes and spatial metadata | Series assembly, voxel geometry, intensity scaling, and NIfTI | A controlled case preserves expected voxel values and spatial metadata, verified by tests and visual inspection. |
| 4. Quality control and preprocessing | Structural and intensity checks, warnings, and thresholds | A documented QC report identifies expected conditions and failure cases, with tests for each reported check. |
| 5. Controlled degradation | Seeded noise, blur, resolution, and intensity changes | Each transformation is reproducible from recorded parameters and seed; tests verify its key properties and metadata. |
| 6. Benchmark and analysis | Downstream task, baselines, statistics, and failure analysis | A baseline can be rerun from documented inputs and configuration; results, uncertainty, limitations, and failure cases are recorded. |

## Tomorrow's first lesson

Read `src/medbench/arrays.py` and `tests/test_smoke.py` before editing. Work out
the expected summary for a small 2D array, then add a focused test only if that
input is part of the intended contract. Run that test and
`.\scripts\check.ps1`; record the result in `LEARNING_LOG.md`.
