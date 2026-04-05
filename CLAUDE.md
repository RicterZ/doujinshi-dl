# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`doujinshi-dl` is a Python CLI tool for downloading doujinshi from mirror sites. Entry point: `nhentai.command:main`. PyPI distribution name: `doujinshi-dl`, Python package name: `nhentai`.

## Development Setup

```bash
# Install in editable mode
pip install --no-cache-dir .

# With nhentai plugin
pip install -e . -e ../doujinshi-dl-nhentai/

# Or with Poetry
poetry install
```

## Running the CLI

```bash
doujinshi-dl --id <ID>
doujinshi-dl --search "keyword" [--download]
doujinshi-dl --favorites --download
```

## Tests

All tests are integration tests that make real HTTP requests and require environment variables:

```bash
export DDL_COOKIE="<cookie>"
export DDL_UA="<user-agent>"
export DOUJINSHI_DL_URL="<mirror-url>"

# Run all tests
python -m unittest discover tests/

# Run a specific test file
python -m unittest tests.test_parser

# Run a single test case
python -m unittest tests.test_parser.TestParser.test_search
```

## Architecture

The pipeline flows through these modules in sequence:

1. **`cmdline.py`** — Parses CLI arguments; loads/saves config from `~/.doujinshi-dl/config.json`
2. **`parser.py`** — Scrapes mirror site via BeautifulSoup and HTTP; functions: `doujinshi_parser`, `galleries_by_tag_parser`, `search_parser`, `favorites_parser`
3. **`doujinshi.py`** — `Doujinshi` model holding metadata and building the download queue; folder-name format tokens: `%i` (ID), `%t` (title), `%a` (artist), etc.
4. **`downloader.py`** — Async image downloading via `httpx` + `asyncio`; `Downloader` writes files directly, `CompressedDownloader` writes `.zip`
5. **`utils.py`** — HTTP helpers (`request()`, `async_request()`), HTML generation, PDF/CBZ creation, SQLite history DB
6. **`serializer.py`** — Writes `metadata.json`, `ComicInfo.xml`, `info.txt` alongside downloaded images
7. **`command.py`** — Orchestrates the full pipeline; the `main()` entry point

## Key Constants & Environment Variables

All URLs, paths, and defaults live in **`constant.py`** (plugin package).

| Variable | Purpose |
|----------|---------|
| `DOUJINSHI_DL_URL` | Mirror base URL (required to run) |
| `DEBUG` | Enable debug logging; `DEBUG=NODOWNLOAD` skips actual downloads |
| `DDL_COOKIE` | Cookie for authentication (also used by tests) |
| `DDL_UA` | User-agent string (also used by tests) |

## Persistence

- **Config:** `~/.doujinshi-dl/config.json` (cookie, user-agent, proxy, language, template)
- **History DB:** `~/.doujinshi-dl/history.sqlite3` (SQLite, tracks downloaded IDs to avoid re-downloading)
- On Linux, `$XDG_DATA_HOME` is respected for these paths

## Viewer Templates

`doujinshi_dl/viewer/` contains bundled HTML viewer templates (`default/`, `minimal/`) used by `generate_html()` in `utils.py` to produce a local browsing interface after download.
