# AGENTS.md - Guide for Agentic Coding Agents


## Build/Lint/Test Commands

- **Unified Check (Preferred)**: `./skills/tester/scripts/check.sh`
- Run all tests: `pytest test/`
- Run single test: `pytest test/test_notedb.py::test_create_notes`
- Run tests with output: `pytest -s`
- Type checking: `uv run ty check`
- Lint check: `ruff check`
- Lint fix: `ruff check --fix`
- Format check: `ruff format --check`
- Format code: `ruff format`


## Skills

The project uses [Anthropic Skills](https://github.com/anthropics/skills) for specialized tasks:
- **tester**: Unified suite for testing and static analysis. See `skills/tester/SKILL.md`.


## Code Style Guidelines

### General Principles
- Follow existing code patterns and conventions
- Use descriptive variable names (e.g., `note_id` instead of `id`)
- Use type hints for all function parameters and return values
- Prefer immutable data structures (NamedTuple over class)

### Imports
- Use absolute imports: `from sonia import notedb as db`
- Group imports in order: standard library, third-party, local
- Import at the top of the file, no inline imports

### Formatting
- Use ruff for formatting (`ruff format`)
- Line length: 88 characters (default)
- Indentation: 4 spaces
- No trailing whitespace

### Types
- Use type hints for all function signatures
- Use `list[Type]` instead of `List[Type]`
- Use `tuple[Type, ...]` for variable-length tuples

### Naming Conventions
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Private functions: `_prefixed_with_underscore`

### Error Handling
- Use specific exception types when possible
- Provide clear error messages
- Handle errors gracefully with try/except blocks

### Documentation
- Use docstrings for all public functions
- Follow Google-style docstrings
- Keep comments concise and meaningful

### Testing
- Use pytest for testing
- Write tests in `test/` directory
- Use descriptive test function names
- Test one behavior per test function


## Communication
In all interactions, be extremely concise and sacrifice grammar for the sake of concision!!
