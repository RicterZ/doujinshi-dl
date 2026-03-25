# coding: utf-8
"""Runtime configuration store for the main package.

Plugins write their paths and settings here so that generic utilities
(e.g. db.py) can read them without hard-coding any plugin name.
"""

_runtime: dict = {}


def set(key: str, value) -> None:
    _runtime[key] = value


def get(key: str, default=None):
    return _runtime.get(key, default)
