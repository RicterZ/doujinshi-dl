# coding: utf-8
import os
import shutil
import sys
import signal
import platform
import urllib3.exceptions

from doujinshi_dl.cmdline import cmd_parser, banner, write_config
from doujinshi_dl.core.registry import get_first_plugin
from doujinshi_dl.core import config as core_config
from doujinshi_dl.downloader import Downloader, CompressedDownloader
from doujinshi_dl.logger import logger
from doujinshi_dl.utils import (
    generate_html, generate_doc, generate_main_html,
    paging, signal_handler, DB, move_to_folder,
)


def _check_env():
    if not os.getenv('DOUJINSHI_DL_URL', ''):
        logger.error('Please set the DOUJINSHI_DL_URL environment variable to specify the target URL.')
        sys.exit(1)


def main():
    banner()

    if sys.version_info < (3, 0, 0):
        logger.error('doujinshi-dl requires Python 3.x')
        sys.exit(1)

    _check_env()

    plugin = get_first_plugin()
    parser = plugin.create_parser()
    serializer = plugin.create_serializer()

    options = cmd_parser()

    # Let the plugin configure its own CONFIG and register runtime values
    plugin.configure(options)

    # Read common config values registered by the plugin
    plugin_config = core_config.get('plugin_config', {})
    base_url = core_config.get('base_url', os.getenv('DOUJINSHI_DL_URL', ''))
    logger.info(f'Using mirror: {base_url}')

    # CONFIG['proxy'] may have been updated after cmd_parser()
    proxy = plugin_config.get('proxy', '')
    if proxy:
        if isinstance(proxy, dict):
            proxy = proxy.get('http', '')
            plugin_config['proxy'] = proxy
            logger.warning(f'Update proxy config to: {proxy}')
            write_config()
        logger.info(f'Using proxy: {proxy}')

    if not plugin_config.get('template'):
        plugin_config['template'] = 'default'

    template = plugin_config.get('template', 'default')
    language = plugin_config.get('language', '')
    logger.info(f'Using viewer template "{template}"')

    # Check authentication
    plugin.check_auth()

    doujinshis = []
    doujinshi_ids = []

    page_list = paging(options.page)

    if options.favorites:
        if not options.is_download:
            logger.warning('You do not specify --download option')

        doujinshis = parser.favorites(page=page_list) if options.page else parser.favorites()

    elif options.keyword:
        if language:
            logger.info(f'Using default language: {language}')
            options.keyword += f' language:{language}'

        doujinshis = parser.search(
            options.keyword,
            sorting=options.sorting,
            page=page_list,
            legacy=options.legacy,
            is_page_all=options.page_all,
        )

    elif options.artist:
        doujinshis = parser.search(
            options.artist,
            sorting=options.sorting,
            page=page_list,
            is_page_all=options.page_all,
            type_='ARTIST',
        )

    elif not doujinshi_ids:
        doujinshi_ids = options.id

    plugin.print_results(doujinshis)
    if options.is_download and doujinshis:
        doujinshi_ids = [i['id'] for i in doujinshis]

    if options.is_save_download_history:
        with DB() as db:
            data = set(map(int, db.get_all()))

        doujinshi_ids = list(set(map(int, doujinshi_ids)) - set(data))
        logger.info(f'New doujinshis account: {len(doujinshi_ids)}')

    if options.zip:
        options.is_nohtml = True

    if not options.is_show:
        downloader = (CompressedDownloader if options.zip else Downloader)(
            path=options.output_dir,
            threads=options.threads,
            timeout=options.timeout,
            delay=options.delay,
            exit_on_fail=options.exit_on_fail,
            no_filename_padding=options.no_filename_padding,
        )

        for doujinshi_id in doujinshi_ids:
            meta = parser.fetch(str(doujinshi_id))
            if not meta:
                continue

            doujinshi_model = plugin.create_model(meta, name_format=options.name_format)
            doujinshi = doujinshi_model.doujinshi
            doujinshi.downloader = downloader

            if doujinshi.check_if_need_download(options):
                doujinshi.download()
            else:
                logger.info(
                    f'Skip download doujinshi because a PDF/CBZ file exists of doujinshi {doujinshi.name}'
                )

            doujinshi_dir = os.path.join(options.output_dir, doujinshi.filename)

            if options.generate_metadata:
                serializer.write_all(meta, doujinshi_dir)
                logger.log(16, f'Metadata files have been written to "{doujinshi_dir}"')

            if options.is_save_download_history:
                with DB() as db:
                    db.add_one(doujinshi.id)

            if not options.is_nohtml:
                generate_html(options.output_dir, doujinshi, template=template)

            if options.is_cbz:
                # Write ComicInfo.xml metadata before packaging
                serializer.write_all(meta, doujinshi_dir)
                generate_doc('cbz', options.output_dir, doujinshi, options.regenerate)

            if options.is_pdf:
                generate_doc('pdf', options.output_dir, doujinshi, options.regenerate)

            if options.move_to_folder:
                if options.is_cbz:
                    move_to_folder(options.output_dir, doujinshi, 'cbz')
                if options.is_pdf:
                    move_to_folder(options.output_dir, doujinshi, 'pdf')

            if options.rm_origin_dir:
                if options.move_to_folder:
                    logger.critical('You specified both --move-to-folder and --rm-origin-dir options, '
                                    'you will not get anything :(')
                shutil.rmtree(os.path.join(options.output_dir, doujinshi.filename), ignore_errors=True)

        if options.main_viewer:
            generate_main_html(options.output_dir)
            serializer.finalize(options.output_dir)

        if not platform.system() == 'Windows':
            logger.log(16, '🍻 All done.')
        else:
            logger.log(16, 'All done.')

    else:
        for doujinshi_id in doujinshi_ids:
            meta = parser.fetch(str(doujinshi_id))
            if not meta:
                continue
            doujinshi_model = plugin.create_model(meta, name_format=options.name_format)
            doujinshi = doujinshi_model.doujinshi
            doujinshi.show()


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    main()
