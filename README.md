# Q Learning model

 README to start the `Q Learning model` project and show how to download dependencies and run linters using ruff.

## Prerequisites
- Git
- Python 3.8+

## Quick start
1. Create and activate a virtual environment
```bash
python -m venv .venv

source .venv/bin/activate
```

2. Install dependencies
```bash
uv sync
```

3. Run project
``` 
uv run q-learning
```
## Linting and formatting with ruff
- Auto-format and fix simple issues:
```bash
ruff format .
ruff check -fix
```
