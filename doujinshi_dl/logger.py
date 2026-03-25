# coding: utf-8
# Compatibility shim — re-exports from new location.
# Preserves backward compatibility for: from doujinshi_dl.logger import logger
from doujinshi_dl.core.logger import *  # noqa: F401, F403
from doujinshi_dl.core.logger import logger  # noqa: F401
