# coding: utf-8
# Utility helpers for the main package.
# No plugin-specific imports.

# Generic filesystem / HTML utilities
from doujinshi_dl.core.utils.fs import (  # noqa: F401
    format_filename, parse_doujinshi_obj, generate_cbz, move_to_folder,
    EXTENSIONS, MAX_FIELD_LENGTH,
)
from doujinshi_dl.core.utils.html import generate_html, generate_main_html  # noqa: F401
from doujinshi_dl.core.utils.db import Singleton, DB  # noqa: F401

# Signal handler and paging helper (kept inline — they have no site-specific code)
import sys
from doujinshi_dl.core.logger import logger  # noqa: F401


def signal_handler(_signal, _frame):
    logger.error('Ctrl-C signal received. Stopping...')
    sys.exit(1)


def paging(page_string):
    # 1,3-5,14 -> [1, 3, 4, 5, 14]
    if not page_string:
        return [1]

    page_list = []
    for i in page_string.split(','):
        if '-' in i:
            start, end = i.split('-')
            if not (start.isdigit() and end.isdigit()):
                raise Exception('Invalid page number')
            page_list.extend(list(range(int(start), int(end) + 1)))
        else:
            if not i.isdigit():
                raise Exception('Invalid page number')
            page_list.append(int(i))

    return page_list


def generate_doc(file_type='', output_dir='.', doujinshi_obj=None, regenerate=False):
    """Generate a CBZ or PDF document from a downloaded doujinshi directory.

    For CBZ, any metadata files (ComicInfo.xml, etc.) should be written to the
    directory *before* calling this function.
    """
    import os

    doujinshi_dir, filename = parse_doujinshi_obj(output_dir, doujinshi_obj, file_type)

    if os.path.exists(f'{doujinshi_dir}.{file_type}') and not regenerate:
        logger.info(f'Skipped {file_type} file generation: {doujinshi_dir}.{file_type} already exists')
        return

    if file_type == 'cbz':
        generate_cbz(doujinshi_dir, filename)

    elif file_type == 'pdf':
        try:
            import img2pdf

            file_list = [f for f in os.listdir(doujinshi_dir) if f.lower().endswith(EXTENSIONS)]
            file_list.sort()

            logger.info(f'Writing PDF file to path: {filename}')
            with open(filename, 'wb') as pdf_f:
                full_path_list = [os.path.join(doujinshi_dir, image) for image in file_list]
                pdf_f.write(img2pdf.convert(full_path_list, rotation=img2pdf.Rotation.ifvalid))

            logger.log(16, f'PDF file has been written to "{filename}"')

        except ImportError:
            logger.error("Please install img2pdf package by using pip.")
    else:
        raise ValueError('invalid file type')
