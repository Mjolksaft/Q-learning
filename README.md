# uv

Minimal README to start the `uv` Python project and show how to download dependencies and run linters using ruff.

## Prerequisites
- Git
- Python 3.8+

## Quick start
1. Create and activate a virtual environment
```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
.\.venv\Scripts\Activate

# Windows (CMD)
.\.venv\Scripts\activate.bat
```

2. Install dependencies
```bash
uv sync
```

## Linting and formatting with ruff
- Check for issues:
```bash
ruff check --fix
```

- Auto-format and fix simple issues:
```bash
ruff format .
ruff check .
```

- Recommended: keep ruff in `requirements-dev.txt` or install with your environment for CI.

## Testing
```bash
pip install pytest            # if not in requirements
pytest
```

## Recommended project files
- requirements.txt
- requirements-dev.txt (include ruff)
- .gitignore
- .ruff.toml (optional ruff config)
- README.md

## Contributing
- Create a branch per feature
- Run ruff and tests before opening a PR

## Troubleshooting
- If installs fail, confirm Python version and that the virtual environment is activated.
- Run `ruff format .` before `ruff check .` to fix formatting issues automatically.
- For CI, install deps then run `ruff check .` and `pytest`.

License: add a LICENSE file of your choice.
