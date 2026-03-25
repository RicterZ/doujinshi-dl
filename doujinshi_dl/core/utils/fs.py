# coding: utf-8
"""Filesystem utilities: filename formatting, CBZ generation, folder management."""
import os
import zipfile
import shutil
from typing import Tuple

from doujinshi_dl.core.logger import logger
from doujinshi_dl.constant import PATH_SEPARATOR

MAX_FIELD_LENGTH = 100
EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


def format_filename(s, length=MAX_FIELD_LENGTH, _truncate_only=False):
    """
    It used to be a whitelist approach allowed only alphabet and a part of symbols.
    but most doujinshi's names include Japanese 2-byte characters and these was rejected.
    so it is using blacklist approach now.
    if filename include forbidden characters ('/:,;*?"<>|) ,it replaces space character(" ").
    """
    if not _truncate_only:
        ban_chars = '\\\'/:,;*?"<>|\t\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b'
        filename = s.translate(str.maketrans(ban_chars, ' ' * len(ban_chars))).strip()
        filename = ' '.join(filename.split())

        while filename.endswith('.'):
            filename = filename[:-1]
    else:
        filename = s

    # limit `length` chars
    if len(filename) >= length:
        filename = filename[:length - 1] + u'…'

    # Remove [] from filename
    filename = filename.replace('[]', '').strip()
    return filename


def parse_doujinshi_obj(
        output_dir: str,
        doujinshi_obj=None,
        file_type: str = ''
) -> Tuple[str, str]:
    filename = f'.{PATH_SEPARATOR}doujinshi.{file_type}'
    if doujinshi_obj is not None:
        doujinshi_dir = os.path.join(output_dir, doujinshi_obj.filename)
        _filename = f'{doujinshi_obj.filename}.{file_type}'

        if file_type == 'pdf':
            _filename = _filename.replace('/', '-')

        filename = os.path.join(output_dir, _filename)
    else:
        if file_type == 'html':
            return output_dir, 'index.html'

        doujinshi_dir = f'.{PATH_SEPARATOR}'

    if not os.path.exists(doujinshi_dir):
        os.makedirs(doujinshi_dir)

    return doujinshi_dir, filename


def generate_cbz(doujinshi_dir, filename):
    file_list = os.listdir(doujinshi_dir)
    file_list.sort()

    logger.info(f'Writing CBZ file to path: {filename}')
    with zipfile.ZipFile(filename, 'w') as cbz_pf:
        for image in file_list:
            image_path = os.path.join(doujinshi_dir, image)
            cbz_pf.write(image_path, image)

    logger.log(16, f'Comic Book CBZ file has been written to "{filename}"')


def move_to_folder(output_dir='.', doujinshi_obj=None, file_type=None):
    if not file_type:
        raise RuntimeError('no file_type specified')

    doujinshi_dir, filename = parse_doujinshi_obj(output_dir, doujinshi_obj, file_type)

    for fn in os.listdir(doujinshi_dir):
        file_path = os.path.join(doujinshi_dir, fn)
        _, ext = os.path.splitext(file_path)
        if ext in ['.pdf', '.cbz']:
            continue

        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

    shutil.move(filename, os.path.join(doujinshi_dir, os.path.basename(filename)))
