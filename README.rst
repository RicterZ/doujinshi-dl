doujinshi-dl
============

あなたも変態。 いいね?

|license|


doujinshi-dl is a CLI tool for downloading doujinshi from mirror sites.

===================
Manual Installation
===================
From Github:

.. code-block::

    git clone https://github.com/RicterZ/doujinshi-dl
    cd doujinshi-dl
    pip install --no-cache-dir .

Build Docker container:

.. code-block::

    git clone https://github.com/RicterZ/doujinshi-dl
    cd doujinshi-dl
    docker build -t doujinshi-dl:latest .
    docker run --rm -it -v ~/Downloads/doujinshi:/output doujinshi-dl --id 123855

==================
Installation
==================
From PyPI with pip:

.. code-block::

   pip install doujinshi-dl

With nhentai plugin support:

.. code-block::

   pip install "doujinshi-dl[nhentai]"

For a self-contained installation, use `pipx <https://github.com/pipxproject/pipx/>`_:

.. code-block::

   pipx install doujinshi-dl

=====
Usage
=====
**⚠️IMPORTANT⚠️**: To bypass Cloudflare, you should use ``--cookie`` and ``--useragent`` options to store your cookie and user-agent.

.. code-block:: bash

    doujinshi-dl --useragent "USER AGENT of YOUR BROWSER"
    doujinshi-dl --cookie "YOUR COOKIE"

**NOTE:**

- The format of the cookie is ``"csrftoken=TOKEN; sessionid=ID; cf_clearance=CLOUDFLARE"``
- ``cf_clearance`` cookie and useragent must be set if you encounter "blocked by cloudflare captcha" error. Make sure you use the same IP and useragent as when you got it

| To get csrftoken and sessionid, first login to your account in a web browser, then:
| (Chrome) |ve| |ld| More tools    |ld| Developer tools     |ld| Application |ld| Storage |ld| Cookies |ld| your mirror URL
| (Firefox) |hv| |ld| Web Developer |ld| Web Developer Tools                  |ld| Storage |ld| Cookies |ld| your mirror URL
|

.. |hv| unicode:: U+2630 .. https://www.compart.com/en/unicode/U+2630
.. |ve| unicode:: U+22EE .. https://www.compart.com/en/unicode/U+22EE
.. |ld| unicode:: U+2014 .. https://www.compart.com/en/unicode/U+2014

*The default download folder will be the path where you run the command (%cd% or $PWD).*

Download specified doujinshi:

.. code-block:: bash

    doujinshi-dl --id 123855 123866 123877

Download doujinshi with ids specified in a file (doujinshi ids split by line):

.. code-block:: bash

    doujinshi-dl --file=doujinshi.txt

Set search default language:

.. code-block:: bash

    doujinshi-dl --language=english

Search a keyword and download the first page:

.. code-block:: bash

    doujinshi-dl --search="tomori" --page=1 --download
    # you also can download by tags and multiple keywords
    doujinshi-dl --search="tag:lolicon, artist:henreader, tag:full color"
    doujinshi-dl --search="lolicon, henreader, full color"

Download your favorites with delay:

.. code-block:: bash

    doujinshi-dl --favorites --download --delay 1 --page 3-5,7

Format output doujinshi folder name:

.. code-block:: bash

    doujinshi-dl --id 261100 --format '[%i]%s'
    # for Windows
    doujinshi-dl --id 261100 --format "[%%i]%%s"

Supported doujinshi folder formatter:

- %i: Doujinshi id
- %f: Doujinshi favorite count
- %t: Doujinshi name
- %s: Doujinshi subtitle (translated name)
- %a: Doujinshi authors' name
- %g: Doujinshi groups name
- %p: Doujinshi pretty name
- %ag: Doujinshi authors name or groups name

Note: for Windows operation system, please use double "%", such as "%%i".

Other options:

.. code-block::

    Usage:
      doujinshi-dl --search [keyword] --download
      DOUJINSHI_DL_URL=https://mirror-url/ doujinshi-dl --id [ID ...]
      doujinshi-dl --file [filename]

    Environment Variable:
      DOUJINSHI_DL_URL        mirror url

    Options:
      -h, --help            show this help message and exit
      -D, --download        download doujinshi (for search results)
      -S, --show            just show the doujinshi information
      --id                  doujinshi ids set, e.g. 167680 167681 167682
      -s KEYWORD, --search=KEYWORD
                            search doujinshi by keyword
      -F, --favorites       list or download your favorites
      -a ARTIST, --artist=ARTIST
                            list doujinshi by artist name
      --page-all            all search results
      --page=PAGE, --page-range=PAGE
                            page number of search results. e.g. 1,2-5,14
      --sorting=SORTING, --sort=SORTING
                            sorting of doujinshi (recent / popular /
                            popular-[today|week])
      -o OUTPUT_DIR, --output=OUTPUT_DIR
                            output dir
      -t THREADS, --threads=THREADS
                            thread count for downloading doujinshi
      -T TIMEOUT, --timeout=TIMEOUT
                            timeout for downloading doujinshi
      -d DELAY, --delay=DELAY
                            slow down between downloading every doujinshi
      --retry=RETRY         retry times when downloading failed
      --exit-on-fail        exit on fail to prevent generating incomplete files
      --proxy=PROXY         store a proxy, for example: -p "http://127.0.0.1:1080"
      -f FILE, --file=FILE  read gallery IDs from file.
      --format=NAME_FORMAT  format the saved folder name
      --html                generate a html viewer at current directory
      --no-html             don't generate HTML after downloading
      --gen-main            generate a main viewer contain all the doujin in the
                            folder
      -C, --cbz             generate Comic Book CBZ File
      -P, --pdf             generate PDF file
      --rm-origin-dir       remove downloaded doujinshi dir when generated CBZ or
                            PDF file
      --move-to-folder      remove files in doujinshi dir then move new file to
                            folder when generated CBZ or PDF file
      --meta                generate a metadata file in doujinshi format
      --regenerate          regenerate the cbz or pdf file if exists
      --cookie=COOKIE       set cookie to bypass Cloudflare captcha
      --useragent=USERAGENT, --user-agent=USERAGENT
                            set useragent to bypass Cloudflare captcha
      --language=LANGUAGE   set default language to parse doujinshis
      --clean-language      set DEFAULT as language to parse doujinshis
      --save-download-history
                            save downloaded doujinshis, whose will be skipped if
                            you re-download them
      --clean-download-history
                            clean download history
      --template=VIEWER_TEMPLATE
                            set viewer template
      --legacy              use legacy searching method

======
Mirror
======
To use a mirror, set the ``DOUJINSHI_DL_URL`` environment variable to your mirror's base URL.

.. code-block:: bash

    DOUJINSHI_DL_URL=https://your-mirror.example.com doujinshi-dl --id 123456

.. image:: https://github.com/RicterZ/doujinshi-dl/raw/master/images/search.png
    :alt: search
    :align: center
.. image:: https://github.com/RicterZ/doujinshi-dl/raw/master/images/download.png
    :alt: download
    :align: center
.. image:: https://github.com/RicterZ/doujinshi-dl/raw/master/images/viewer.png
    :alt: viewer
    :align: center


.. |license| image:: https://img.shields.io/github/license/ricterz/doujinshi-dl.svg
   :target: https://github.com/RicterZ/doujinshi-dl/blob/master/LICENSE
