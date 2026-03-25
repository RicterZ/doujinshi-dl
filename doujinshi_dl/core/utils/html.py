# coding: utf-8
"""HTML viewer generation utilities (generic, no site-specific references)."""
import json
import os
import urllib.parse

from doujinshi_dl.core.logger import logger
from doujinshi_dl.core.utils.fs import EXTENSIONS, parse_doujinshi_obj
from doujinshi_dl.constant import PATH_SEPARATOR


def _readfile(path):
    loc = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # doujinshi_dl/

    with open(os.path.join(loc, path), 'r') as file:
        return file.read()


def generate_html(output_dir='.', doujinshi_obj=None, template='default'):
    doujinshi_dir, filename = parse_doujinshi_obj(output_dir, doujinshi_obj, 'html')
    image_html = ''

    if not os.path.exists(doujinshi_dir):
        logger.warning(f'Path "{doujinshi_dir}" does not exist, creating.')
        try:
            os.makedirs(doujinshi_dir)
        except EnvironmentError as e:
            logger.critical(e)

    file_list = os.listdir(doujinshi_dir)
    file_list.sort()

    for image in file_list:
        if not os.path.splitext(image)[1] in EXTENSIONS:
            continue
        image_html += f'<img src="{image}" class="image-item"/>\n'

    html = _readfile(f'viewer/{template}/index.html')
    css = _readfile(f'viewer/{template}/styles.css')
    js = _readfile(f'viewer/{template}/scripts.js')

    if doujinshi_obj is not None:
        name = doujinshi_obj.name
    else:
        metadata_path = os.path.join(doujinshi_dir, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as file:
                doujinshi_info = json.loads(file.read())
            name = doujinshi_info.get("title")
        else:
            name = 'Doujinshi HTML Viewer'

    data = html.format(TITLE=name, IMAGES=image_html, SCRIPTS=js, STYLES=css)
    try:
        with open(os.path.join(doujinshi_dir, 'index.html'), 'wb') as f:
            f.write(data.encode('utf-8'))

        logger.log(16, f'HTML Viewer has been written to "{os.path.join(doujinshi_dir, "index.html")}"')
    except Exception as e:
        logger.warning(f'Writing HTML Viewer failed ({e})')


def generate_main_html(output_dir=f'.{PATH_SEPARATOR}'):
    """
    Generate a main html to show all the contained doujinshi.
    With a link to their `index.html`.
    Default output folder will be the CLI path.
    """
    import shutil

    image_html = ''

    main = _readfile('viewer/main.html')
    css = _readfile('viewer/main.css')
    js = _readfile('viewer/main.js')

    element = '\n\
            <div class="gallery-favorite">\n\
                <div class="gallery">\n\
                    <a href="./{FOLDER}/index.html" class="cover" style="padding:0 0 141.6% 0"><img\n\
                            src="./{FOLDER}/{IMAGE}" />\n\
                        <div class="caption">{TITLE}</div>\n\
                    </a>\n\
                </div>\n\
            </div>\n'

    os.chdir(output_dir)
    doujinshi_dirs = next(os.walk('.'))[1]

    for folder in doujinshi_dirs:
        files = os.listdir(folder)
        files.sort()

        if 'index.html' in files:
            logger.info(f'Add doujinshi "{folder}"')
        else:
            continue

        image = files[0]  # 001.jpg or 001.png
        if folder is not None:
            title = folder.replace('_', ' ')
        else:
            title = 'Doujinshi HTML Viewer'

        image_html += element.format(FOLDER=urllib.parse.quote(folder), IMAGE=image, TITLE=title)
    if image_html == '':
        logger.warning('No index.html found, --gen-main paused.')
        return
    try:
        data = main.format(STYLES=css, SCRIPTS=js, PICTURE=image_html)
        with open('./main.html', 'wb') as f:
            f.write(data.encode('utf-8'))
        pkg_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        shutil.copy(os.path.join(pkg_dir, 'viewer/logo.png'), './')
        output_dir = output_dir[:-1] if output_dir.endswith('/') else output_dir
        logger.log(16, f'Main Viewer has been written to "{output_dir}/main.html"')
    except Exception as e:
        logger.warning(f'Writing Main Viewer failed ({e})')
