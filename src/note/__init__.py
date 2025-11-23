"""
Expose the public API for the package in one place.

Modules keep their own ``__all__`` lists; this file aggregates them so
``from note import *`` pulls only the intended public surface.
"""

from importlib import metadata

from . import commands, console_output, notedb


_PUBLIC_MODULES = (commands, console_output, notedb)

# Explicit package export surface (modules first, then re-exported names).
__all__ = [
    "commands",
    "console_output",
    "notedb",
]

for _module in _PUBLIC_MODULES:
    __all__.extend(_module.__all__)
    for _name in _module.__all__:
        # Don't overwrite module objects already in the namespace.
        if _name in globals():
            continue
        globals()[_name] = getattr(_module, _name)

try:
    __version__ = metadata.version("note")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"

__all__.append("__version__")
