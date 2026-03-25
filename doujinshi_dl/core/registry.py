# coding: utf-8
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from doujinshi_dl.core.plugin import BasePlugin


def get_plugin(name: str) -> 'BasePlugin':
    from importlib.metadata import entry_points
    eps = entry_points(group='doujinshi_dl.plugins')
    for ep in eps:
        if ep.name == name:
            return ep.load()
    raise KeyError(
        f"Plugin {name!r} not found. "
        f"Install it with: pip install doujinshi-dl-{name}"
    )


def get_first_plugin() -> 'BasePlugin':
    from importlib.metadata import entry_points
    eps = list(entry_points(group='doujinshi_dl.plugins'))
    if not eps:
        raise RuntimeError(
            "No doujinshi-dl plugin installed. "
            "Install a plugin from PyPI, e.g.: pip install doujinshi-dl-<name>"
        )
    return eps[0].load()
