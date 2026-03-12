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
4. Run the main program from the `src` folder.

Example:

`python src/game.py`

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

Set up Git hooks:

```powershell
pre-commit install
pre-commit install --hook-type pre-push
```

## Run The Game

Start the game with:

```powershell
python src/game.py
```

## Run Checks Locally

Run all commit-stage checks:

```powershell
pre-commit run --all-files
```

Run the push-stage checks manually:

```powershell
pre-commit run --hook-stage pre-push --all-files
```

## Check YAML Files

To validate YAML files only, run:

```powershell
pre-commit run check-yaml --all-files
```

This checks files such as:

- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml`

## Tests

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
├── pyproject.toml
├── README.md
├── src/
│   ├── AIplayer.py
│   ├── benchmark.py
│   └── game.py
└── tests/
```
