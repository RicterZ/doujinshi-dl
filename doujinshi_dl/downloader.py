# coding: utf-8
# Compatibility shim — re-exports from new location.
# Preserves backward compatibility for: from doujinshi_dl.downloader import Downloader, CompressedDownloader
from doujinshi_dl.core.downloader import *  # noqa: F401, F403
from doujinshi_dl.core.downloader import Downloader, CompressedDownloader, download_callback  # noqa: F401
