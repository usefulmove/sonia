---
name: tester
description: Unified testing and static analysis suite using uv, pytest, ty, and ruff.
---

# Tester Skill

Unified interface for ensuring code quality in the `sonia` project.

## Capabilities

### 1. Full Quality Suite
Run all tests and static analysis in sequence.
- **Action**: Execute `scripts/check.sh`

### 2. Unit Testing
Run the pytest suite.
- **Command**: `uv run pytest test/`
- **Specific Test**: `uv run pytest test/sonia/test_notedb.py::test_name`

### 3. Type Checking
Perform static type analysis using `ty`.
- **Command**: `uv run ty`

### 4. Linting & Formatting
Use `ruff` for linting and code formatting.
- **Check Linting**: `uv run ruff check`
- **Fix Linting**: `uv run ruff check --fix`
- **Check Format**: `uv run ruff format --check`
- **Format Code**: `uv run ruff format`

## Bundled Resources
- `scripts/check.sh`: Bash script to run all checks with fail-fast behavior.
