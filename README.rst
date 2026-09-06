doujinshi-dl
==============

`English <README.rst>`_ | `中文 <README.zh-CN.rst>`_

あなたも変態。 いいね?

|pypi| |license|

A command-line tool for searching, downloading, and organizing doujinshi through
site plugins. Supports batch IDs, favorites, an HTML reader, and CBZ, PDF, and ZIP exports.

**Install a site plugin and configure authentication before use.** This guide uses
``doujinshi-dl-nhentai`` as an example. For other plugins, refer to their documentation
for authentication, search syntax, and mirror support.
Python 3.12 is recommended; the installation commands below tell uv to select it.

.. contents:: Contents
   :local:
   :depth: 2

Quick start
-------------

Install uv following the `official installation guide <https://docs.astral.sh/uv/getting-started/installation/>`_.
On macOS, you can also use Homebrew:

.. code-block:: bash

   brew install uv

Install the application and site plugin in the same isolated environment:

.. code-block:: bash

   uv tool install --python 3.12 --with doujinshi-dl-nhentai doujinshi-dl
   uv tool update-shell

Open a new terminal and check that the command is available:

.. code-block:: bash

   doujinshi-dl --help

Get an API token from your account settings on the site and replace
``YOUR_API_TOKEN`` below with its value. Save the token and download in separate
commands: the application exits after saving the token.

.. code-block:: bash

   doujinshi-dl --token "YOUR_API_TOKEN"
   doujinshi-dl --id 123855 --output ./downloads

By default, downloads are saved in the current working directory and an HTML reader
is generated. Use ``--output`` to choose a destination.

Installation and updates
--------------------------

Manage the command-line tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``uv tool`` manages a dedicated Python environment for the application. Install the
plugin with ``--with`` so it shares that environment; plugins installed elsewhere
cannot be discovered. The application currently loads the first site plugin it finds,
so install only one site plugin per environment.

Update or uninstall:

.. code-block:: bash

   uv tool upgrade doujinshi-dl
   uv tool uninstall doujinshi-dl

For PDF export, add ``img2pdf`` while keeping the site plugin:

.. code-block:: bash

   uv tool install --python 3.12 --with doujinshi-dl-nhentai --with img2pdf doujinshi-dl

Install from source
~~~~~~~~~~~~~~~~~~~~~

Use this option for the latest repository code or development. These commands create
a virtual environment in the project directory and install the application in
editable mode alongside the site plugin:

.. code-block:: bash

   git clone https://github.com/RicterZ/doujinshi-dl.git
   cd doujinshi-dl
   uv venv --python 3.12
   uv pip install -e . doujinshi-dl-nhentai

Activate the environment to use the remaining ``doujinshi-dl`` commands in this guide:

.. code-block:: bash

   # bash / zsh
   source .venv/bin/activate
   doujinshi-dl --help

For fish, use ``source .venv/bin/activate.fish``. For Windows PowerShell, use
``.venv\Scripts\Activate.ps1``. You can also run the executable directly, for example
``.venv/bin/doujinshi-dl`` on macOS or Linux.

To enable PDF export in this environment, run ``uv pip install img2pdf``.
The project uses the Poetry build backend; uv handles build dependencies automatically,
so a separate Poetry installation is not required.

Common tasks
--------------

Download or inspect by ID
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Download multiple IDs
   doujinshi-dl --id 123855 123866 123877 --output ./downloads

   # Show information only
   doujinshi-dl --id 123855 --show

   # Read IDs from a file
   doujinshi-dl --file doujinshi.txt --output ./downloads

Place one numeric ID per line in ``doujinshi.txt``:

.. code-block:: text

   123855
   123866
   123877

Search and favorites
~~~~~~~~~~~~~~~~~~~~~~

Add ``--download`` to download results from search, artist, or favorites queries.
Page selection accepts a single page, a range, or a combination, such as ``1``,
``3-5``, or ``1,3-5,7``. Use ``--page-all`` to fetch all search results.

.. code-block:: bash

   # Search and download the first page
   doujinshi-dl --search "full color" --page 1 --download

   # Download selected favorites pages, waiting 1 second between galleries
   doujinshi-dl --favorites --page 3-5,7 --download --delay 1

Search syntax depends on the plugin. Use ``--artist`` to query by artist.
``--sorting`` accepts ``recent``, ``popular``, ``popular-today``, ``popular-week``,
or ``date``, and defaults to ``popular``. Available sorting behavior depends on the site.

Export and read
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Export a CBZ with metadata
   doujinshi-dl --id 123855 --cbz --output ./downloads

   # Export a PDF; install img2pdf first
   doujinshi-dl --id 123855 --pdf --output ./downloads

   # Download directly to ZIP, disabling HTML generation
   doujinshi-dl --id 123855 --zip --output ./downloads

   # Generate HTML readers for downloaded directories
   doujinshi-dl --html ./downloads

   # Generate an overview page after downloading
   doujinshi-dl --id 123855 --gen-main --output ./downloads

``--no-html`` disables HTML generation after downloading. ``--meta`` writes additional
metadata files provided by the plugin. Use ``--regenerate`` to request regeneration
of an existing CBZ or PDF.

Image directories are kept by default. ``--rm-origin-dir`` deletes the original
directory; use it only after confirming that export succeeds. ``--move-to-folder``
removes the original files inside the directory and moves the exported file into it.
Do not combine these two options.

Customize folder names
~~~~~~~~~~~~~~~~~~~~~~~~

The default format is ``[%i][%a][%t]``. To keep only the ID and title:

.. code-block:: bash

   doujinshi-dl --id 123855 --format '[%i]%t'

The example site plugin supports these placeholders:

.. list-table:: Folder name placeholders
   :header-rows: 1
   :widths: 20 80

   * - Placeholder
     - Value
   * - ``%i``
     - Gallery ID
   * - ``%t``
     - Title
   * - ``%s``
     - Subtitle or translated title
   * - ``%p``
     - Pretty title
   * - ``%a``
     - Artists
   * - ``%g``
     - Groups
   * - ``%ag``
     - Artists, falling back to groups
   * - ``%f``
     - Favorite count

In Windows ``.bat`` or ``.cmd`` files, write ``%%`` instead of ``%``.
In PowerShell, use the single-quoted example above as written.

Configuration and download options
------------------------------------

Authentication, language, and proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These settings are saved for future commands. The application exits after setting
a token, language, or proxy, so configure them before running a separate download command.

.. code-block:: bash

   doujinshi-dl --token "YOUR_API_TOKEN"
   doujinshi-dl --language english
   doujinshi-dl --proxy "http://127.0.0.1:1080"

   # Clear the language filter or proxy
   doujinshi-dl --language ""
   doujinshi-dl --proxy ""

The language setting appends a ``language:`` filter to keyword and artist searches.
The plugin determines where configuration and history are stored. The example plugin
normally uses ``~/.doujinshi-dl/`` and keeps using ``~/.nhentai/`` if that legacy directory
exists. On Linux, it also supports ``XDG_DATA_HOME``.

Use a compatible mirror
~~~~~~~~~~~~~~~~~~~~~~~~~

Replace the example address with the base URL of a mirror supported by your plugin:

.. code-block:: bash

   # bash / zsh
   DOUJINSHI_DL_URL=https://your-mirror.example.com doujinshi-dl --id 123855

The mirror must match the API and image URL conventions used by the plugin.
Setting this variable alone does not add support for an arbitrary site.

Download options at a glance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table:: Common download options
   :header-rows: 1
   :widths: 30 15 55

   * - Option
     - Default
     - Purpose
   * - ``--output``, ``-o``
     - ``.``
     - Destination directory
   * - ``--threads``, ``-t``
     - ``5``
     - Download threads; use a value from 1 to 15
   * - ``--timeout``, ``-T``
     - ``30``
     - Request timeout in seconds
   * - ``--delay``, ``-d``
     - ``0``
     - Seconds to wait between galleries
   * - ``--retry``
     - ``3``
     - Retry count, applied by the plugin
   * - ``--exit-on-fail``
     - Off
     - Exit when a download fails
   * - ``--no-filename-padding``
     - Off
     - Disable zero-padding of page numbers in image filenames
   * - ``--save-download-history``
     - Off
     - Record downloaded IDs and skip IDs already recorded

Enable download history explicitly on each run where you want to record downloads
or skip previously recorded IDs:

.. code-block:: bash

   doujinshi-dl --id 123855 123866 --save-download-history

Run ``doujinshi-dl --help`` for the full list of options.

Docker
--------

The included Dockerfile installs the application and example site plugin.
Build from the repository root and persist both downloads and configuration:

.. code-block:: bash

   docker build -t doujinshi-dl:latest .
   docker volume create doujinshi-dl-config
   mkdir -p downloads
   docker run --rm -it -v doujinshi-dl-config:/root/.doujinshi-dl \
     doujinshi-dl:latest --token "YOUR_API_TOKEN"
   docker run --rm -it -v doujinshi-dl-config:/root/.doujinshi-dl \
     -v "$(pwd)/downloads:/output" doujinshi-dl:latest --id 123855

Downloads appear in the host's ``downloads`` directory. To use a custom mirror,
add ``-e DOUJINSHI_DL_URL=https://your-mirror.example.com`` to ``docker run``.

Troubleshooting
-----------------

Command not found after installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing with ``uv tool install``, run ``uv tool update-shell`` and open a new
terminal. Use ``uv tool list`` to confirm that the tool is installed.

``uv pip install --system`` installs packages into the Python environment selected by
uv and places command scripts in that interpreter's scripts directory. It does not
add that directory to PATH or refresh pyenv's command shims. With multiple Python
installations, the interpreter used during installation may also differ from the one
selected in your current terminal. Check the environment and package location first:

.. code-block:: bash

   uv pip show --system doujinshi-dl doujinshi-dl-nhentai

For command-line use, follow the quick start and install with ``uv tool install``.
If you keep a pyenv-managed installation, select the Python version containing the
packages, run ``pyenv rehash``, and ensure the pyenv shims directory is on PATH.

No plugin installed
~~~~~~~~~~~~~~~~~~~~~

The application loads a plugin even when running ``--help``. If you see
``No doujinshi-dl plugin installed``, repeat the tool installation command with
``--with doujinshi-dl-nhentai``. For a source installation, run
``uv pip install doujinshi-dl-nhentai`` in the same virtual environment.

Authentication, request, or download failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Authentication failure: check that the token belongs to the current site and save it again with ``--token``.
* Connection failure: check the mirror URL and proxy. Site API changes may require a plugin update.
* Rate limiting: reduce ``--threads``, increase ``--delay``, and follow the site's request limits.
* Missing PDF output: install ``img2pdf`` in the application's environment as described in the installation section.

License
---------

This project is distributed under the `MIT license <LICENSE>`_.

.. |pypi| image:: https://img.shields.io/pypi/v/doujinshi-dl.svg
   :target: https://pypi.org/project/doujinshi-dl/
   :alt: PyPI version

.. |license| image:: https://img.shields.io/github/license/RicterZ/nhentai.svg
   :target: LICENSE
   :alt: MIT license
