# sonia
## . simple capture .

`sonia` is a command-line application designed to help you capture, organize, and manage your notes and thoughts without leaving the terminal. It combines `duckdb` for robust local storage and `rich` for beautiful, readable output.

---

## Features

*   **Fast Capture**: Add single or multiple notes quickly.
*   **Tagging System**: Use tags like `:mit:` (Most Important Task) or `:tod:` (Today) to organize workflow.
*   **Focus Mode**: Instantly filter for your most important tasks.
*   **Search**: Full-text search and dedicated tag filtering.
*   **Edit & Append**: Modify notes in place without recreating them.
*   **Persistent**: Data is stored locally in a high-performance `DuckDB` file.
*   **Beautiful Output**: Formatted tables and colors via `Rich`.

## Installation

### Option 1: From a clone (recommended)
Install from a local checkout so you can run `sonia` from anywhere:

```bash
pipx install .
# OR
pip install .
# OR
uv tool install .
```

### Option 2: For Developers

If you want to contribute or modify the source code, this project uses `uv` for dependency management and specialized [Anthropic Skills](https://github.com/anthropics/skills) for development.

1.  **Clone the repository:**
...
    ```bash
    uv sync
    ```

3.  **Run quality checks:**

    ```bash
    ./skills/tester/scripts/check.sh
    ```

4.  **Run locally:**


    ```bash
    python -m sonia list
    ```

## Usage

Once installed, use the `sonia` command.

### Capture
Add one note or multiple notes at once.
```bash
sonia add "buy milk" "call the mechanic about the car"
# Alias
sonia a "quick note"
```

### Retrieve & Organize

**List All**
View your history with IDs and timestamps.
```bash
sonia list
# Alias: sonia ls
```

**Focus Mode**
Show only notes tagged with `:mit:` (Most Important Task) or `:tod:` (Today).
```bash
sonia focus
# Alias: sonia fls
```

**Search**
Find notes containing specific text.
```bash
sonia search "mechanic"
# Alias: sonia s "mechanic"
```

**Filter by Tag**
Find notes with a specific tag.
```bash
sonia tag "book"
# Alias: sonia t "book"
```

### Manage

**Update**
Replace the text of a note (requires Note ID).
```bash
sonia update 1 "buy almond milk"
# Alias: sonia u 1 "..."
```

**Append**
Add text to the end of an existing note.
```bash
sonia append 1 ":done:"
# Alias: sonia app 1 "..."
```

**Delete**
Mark tasks as done or remove them using their ID.
```bash
sonia done 1
# Alias: sonia d 1
```

### Maintenance

**Rebase**
Re-index Note IDs to be sequential (1, 2, 3...) after deletions.
```bash
sonia rebase
```

**Clear All**
*Warning: This permanently deletes all data.*
```bash
sonia --clear
```

## Command Reference

| Command | Aliases | Description |
|---|---|---|
| `add` | `a`, `capture` | Create new notes |
| `list` | `ls`, `all` | Show all notes |
| `focus` | `fls`, `focusls` | Show notes tagged `:mit:` or `:tod:` |
| `short` | `sls`, `important` | Show notes NOT tagged `:que:` |
| `search` | `s`, `f` | Search text in notes |
| `tag` | `t` | Search for specific tags |
| `update` | `u`, `edit` | Overwrite note text |
| `append` | `app` | Append text to note |
| `delete` | `d`, `rm`, `done` | Delete notes |
| `rebase` | | Reset Note IDs |
| `change` | `replace` | Bulk find/replace text in notes |
| `decide` | `...` | Get an oblique strategy or Taoist wisdom |

## Technologies

  * **[DuckDB](https://duckdb.org/)**: Local SQL OLAP database.
  * **[Rich](https://rich.readthedocs.io/en/stable/)**: Terminal formatting.
  * **[uv](https://github.com/astral-sh/uv)**: Python package and project manager.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.
