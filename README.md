# Assignment1

Board Game Assignment

## Project Title

Assignment 1 – AI Board Game Project


## Game Overview

Add the name of your chosen board game here.

## How to Run the Code

Update these steps to match your implementation.

1. Open the project folder in VS Code.
2. Make sure Python is installed.
3. Install dependencies with `pip install -e .`.
4. Run the main program from the project root.

Example:

`python main.py`

2048 project for the AI board game assignment.

## Requirements

- Python 3.12 or newer
- `pip`
- Git, if you want to use the pre-commit hooks

## Install

Install the project dependencies:

```powershell
pip install -e .
```

Install the local quality-check tools:

```powershell
pip install pre-commit
```

Install mypy (type checker):

```powershell
pip install mypy
```

Set up Git hooks:

```powershell
pre-commit install
pre-commit install --hook-type pre-push
```

## Run The Game

Start the game with:

```powershell
python main.py
```

## Run Checks Locally (.ruff_cache)

Run all commit-stage checks:

```powershell
pre-commit run --all-files
```

Run the push-stage checks manually:

```powershell
pre-commit run --hook-stage pre-push --all-files
```

## Type Check (.mypy_cache)

Type-check a single file:

```powershell
mypy main.py
```

Type-check the whole project:

```powershell
mypy .
```

## Check YAML Files

To validate YAML files only, run:

```powershell
pre-commit run check-yaml --all-files
```

This checks files such as:

- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml`

## Tests (.pytest_cache)

If test files exist under `tests/`, run them with:

```powershell
python -m pytest tests
```

The local `pre-push` hook and the GitHub Actions workflow both run `pytest` only when `tests/test_*.py` files exist.


## Folder Structure

```text
Assignment1/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .pre-commit-config.yaml
├── main.py
├── pyproject.toml
├── README.md
├── src/
│   ├── game/
│   │   └── game.py
│   ├── ai/
│   │   ├── expectimax.py
│   │   ├── mcts.py
│   │   └── heuristics.py
│   ├── benchmark/
│   │   └── runner.py
└── tests/
	└── test_game.py
```
