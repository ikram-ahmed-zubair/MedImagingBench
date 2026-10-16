# Instructions for coding-agent sessions

- Teach incrementally: focus on one concept and one small, testable outcome per
  session. Explain the relevant idea and why the change is needed in clear terms.
- Before editing, inspect the existing implementation, related tests,
  `pyproject.toml`, and `git status --short`. Preserve unrelated and
  uncommitted work; never infer that a planned function or feature exists.
- Follow the project's Python, pytest, Ruff, and PowerShell conventions. Write
  or update tests for behavior changes, using small synthetic inputs where
  possible. Do not introduce Jupyter notebooks.
- Run the relevant tests and checks available in the existing environment.
  Report the exact commands and actual pass/fail results; do not claim checks
  passed when they were not run.
- Explain the files changed, behavior, and test evidence. End with one concrete
  next learning step and record session notes in `LEARNING_LOG.md` when asked.
- Protect patient privacy: do not add patient-identifiable data, credentials,
  or restricted datasets to the repository.
- Do not commit or push unless the user explicitly requests it.
