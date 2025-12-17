#!/usr/bin/env python3
# Use the part of the subcommand, option, etc., being typed
# to provide suggested completions (suggestions).

import sys


SUBCOMMANDS_AND_OPTIONS = (
    "add",
    "capture",
    "list",
    "focus",
    "search",
    "update",
    "append",
    "tag",
    "rebase",
    "change",
    "version",
    "db",
    "decide",
)


def get_suggestions(stub: str) -> tuple[str, ...]:
    """Use the word STUB to return a list of relevant suggestions."""
    return tuple(cmd for cmd in SUBCOMMANDS_AND_OPTIONS if cmd.startswith(stub))


if __name__ == "__main__":
    # get the current word (stub) from the shell and use to give a suggestion

    # When you type sonia sub<TAB>:
    # 1.  Script: sonia_completions.py (The logic provider)
    # 2.  Command ($1 / argv[1]): sonia (The context/namespace)
    # 3.  Stub ($2 / argv[2]): sub (What you typed so far)

    stub = sys.argv[2]

    suggestions: tuple[str, ...] = get_suggestions(stub)

    match suggestions:
        case [suggestion]:
            print(suggestion)
