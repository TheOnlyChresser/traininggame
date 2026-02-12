# Repository Guidelines

## Project Structure & Module Organization
- `main.py`: application entry point and game flow/state handling.
- `ui.py`: custom Pygame UI framework (`UIDiv`, `UIText`, inputs, dropdowns).
- `Include/ai.py`: model build/training logic used by the game.
- `data/torchDATA.py`: layer, activation, and loss registries.
- `data/MNIST/`: local dataset cache; avoid committing regenerated dataset artifacts.
- `test.py`: training/evaluation script used as a smoke test.

Keep new gameplay/UI logic in `main.py` + `ui.py`, and ML/training logic in `Include/` or `data/` modules.

## Build, Test, and Development Commands
- `python -m venv .venv` creates a local virtual environment.
- `.\.venv\Scripts\Activate.ps1` activates the environment in PowerShell.
- `pip install -r requirements.txt` installs project dependencies.
- `python main.py` runs the interactive training game.
- `python test.py` runs the current model-training smoke test.
- `pipreqs --force --ignore .\lib,.\Scripts --encoding=utf8 .` refreshes `requirements.txt` when imports change.

## Coding Style & Naming Conventions
- Use Python with 4-space indentation and PEP 8 naming.
- Functions/variables: `snake_case`; classes: `PascalCase`; constants: `UPPER_SNAKE_CASE`.
- Prefer small, focused functions for parsing/validation (pattern already used in `main.py`).
- Keep UI style tokens consistent with existing class-string conventions in `ui.py`.

## Testing Guidelines
- No formal `pytest` suite is currently committed; treat `python test.py` as baseline verification.
- For new logic, add unit tests under `tests/` using `test_*.py` naming so `pytest` can be adopted cleanly.
- Validate both CPU-only behavior and failure messaging for missing ML dependencies where relevant.

## Commit & Pull Request Guidelines
- Recent history includes very short messages (`c`, `d`, `z`); improve this going forward.
- Write commits in imperative form, e.g., `Add layer parameter validation for Dropout`.
- Keep commits scoped (UI, training, or data changes separated when possible).
- PRs should include: purpose, key changes, local test steps/run output, and screenshots for UI changes.
- Link related issues/tasks and note any dataset or dependency impact.
