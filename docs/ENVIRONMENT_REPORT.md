# Environment report

Generated during repository initialization on 2026-09-19 (Asia/Shanghai). Values below are observations from this machine, not assumptions.

## Operating environment

- OS version: Windows NT `10.0.26200.0` (`x64`). The Windows caption query was unavailable under the current permissions.
- PowerShell: `7.6.6`
- Locale: `zh-CN`

## Tools detected

| Tool | Observed result |
| --- | --- |
| Git | `2.46.2.windows.1` |
| GitHub CLI (`gh`) | `2.94.0` |
| Git LFS | `3.5.1` |
| uv | `0.6.12` |
| VS Code | `1.134.0` |
| Python system command | Present on PATH but not executable; it resolves to a broken Cygwin shim. |
| Python launcher (`py`) | Present, but reports no installed Python. |

## GitHub CLI authentication

`gh auth status` found an existing account configuration, but the active token was invalid. No remote repository was created and no GitHub write operation was attempted.

## Project Python environment

- Selected method: `uv`-managed project virtual environment at `.venv`.
- Interpreter line: CPython `3.12` (the environment was created as CPython `3.12.11`).
- The bootstrap script uses a project-local ignored `.uv-cache/` because the default machine-level uv cache was not readable under the current permissions.
- Core and development dependencies are declared in `pyproject.toml`; Jupyter is optional and is not installed by the core bootstrap.

### Installed package versions

These versions were reported by `scripts/check_env.py` from the project virtual environment:

| Package | Version |
| --- | --- |
| matplotlib | `3.11.2` |
| numpy | `2.5.3` |
| pandas | `2.3.3` |
| pydantic | `2.13.5` |
| pytest | `8.4.2` |
| rich | `13.9.4` |
| ruff | `0.16.8` |
| scipy | `1.18.1` |

## Missing or unusable components

- A usable system-wide Python command is unavailable. This is intentionally not repaired globally.
- GitHub CLI re-authentication is required before creating or pushing the private remote.

## Changes made during this initialization

- Created the project-local `.venv` using `uv`.
- No system-wide Python, PATH, credentials, or unrelated machine configuration was changed.
