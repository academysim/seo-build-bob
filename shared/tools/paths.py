"""
paths.py – canonical path helpers for the academy-seo-build repo.

Replaces the repeated HERE/ROOT derivation boilerplate that previously appeared
in every pipeline script:

    HERE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.normpath(os.path.join(HERE, '..', '..'))

Usage
-----
    from shared.tools.paths import repo_root, prop_root

    ROOT = repo_root()                   # always the repo root
    D    = os.path.join(prop_root('events'), 'upload')

Both functions always return the same value regardless of the current working
directory or how the calling script was launched.
"""

import os as _os

# Compute once at import time; __file__ is always this file, so the result is
# the same for every caller regardless of cwd.
_THIS_FILE = _os.path.abspath(__file__)            # …/shared/tools/paths.py
_SHARED_TOOLS = _os.path.dirname(_THIS_FILE)       # …/shared/tools
_SHARED      = _os.path.dirname(_SHARED_TOOLS)     # …/shared
_REPO_ROOT   = _os.path.dirname(_SHARED)           # repo root


def repo_root() -> str:
    """Return the absolute path of the repository root directory."""
    return _REPO_ROOT


def prop_root(key: str) -> str:
    """Return the absolute path of a property sub-directory.

    ``key`` is one of: ``'lounge'``, ``'events'``, ``'builds'``,
    ``'driver'``, ``'health'``.

    Equivalent to ``os.path.join(repo_root(), key)``.
    """
    return _os.path.join(_REPO_ROOT, key)
