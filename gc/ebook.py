#!/usr/bin/env python3

"""
Construct an epub of talks by apostles for a given conference.
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import markdown
import os
import templates
import uuid

from datetime import date
from logger import setup_logger

logger = setup_logger(logfile=None)


UUID = uuid.uuid4()

CR_PATH = '{year}/{month}/cr/'
MIMETYPE_PATH = CR_PATH + 'mimetype'
CONTAINER_PATH = CR_PATH + 'META-INF/container.xml'
PACKAGE_PATH = CR_PATH + 'EPUB/package.opf'
NAV_PATH = CR_PATH + 'EPUB/xhtml/nav.xhtml'
TITLE_PATH = CR_PATH + 'EPUB/xhtml/title.xhtml'
LANG_PATH = CR_PATH + 'EPUB/xhtml/{lang}.xhtml'
LANG_DIR = CR_PATH + 'EPUB/xhtml/{lang}/'
TALK_PATH = LANG_DIR + 'talk.xhtml'

LANGS_FULL = {
    'eng': 'English',
    'hun': 'Hungarian',
}

MONTHS = {
    '04': 'April',
    '10': 'October',
}


def create(year, month, languages, talks):
    ensure_path_exists(CR_PATH.format(year=year, month=month))
    
    # create the mimetype file
    mimetype_path = MIMETYPE_PATH.format(year=year, month=month)
    with open(mimetype_path, 'w', encoding='utf8') as fout:
        fout.write(templates.MIMETYPE)
    
    # create the META-INF/container.xml file
    container_path = CONTAINER_PATH.format(year=year, month=month)
    ensure_path_exists(container_path)
    with open(container_path, 'w', encoding='utf8') as fout:
        fout.write(templates.CONTAINER)
    
    # create package.opf    
    ebook_uuid = uuid.uuid4()
    today = date.today()
    items = []
    refs = []
    
    for lang in languages:
        lang_part = templates.PACKAGE_ITEM_LANG_PART.format(lang=lang)
        items.append(lang_part)
        for talk in talks:
            talk_path, _, _ = talk
            talk_parts = talk_path.split('_')
            fileid = '{}-{}-{}-{}'.format(lang, talk_parts[3], talk_parts[4], talk_parts[6])
            item = templates.PACKAGE_ITEM_LANG.format(lang=lang, filename=talk, fileid=fileid)
            items.append(item)
            refs.append(templates.PACKAGE_REF_LANG_PART.format(lang=lang))
            refs.append(templates.PACKAGE_REF_LANG.format(fileid=fileid))
    
    package = templates.PACKAGE.format(
        year=year, 
        month=month, 
        uuid=ebook_uuid, 
        date=today, 
        items=''.join(items),
        refs=''.join(refs),
    )
    package_path = PACKAGE_PATH.format(year=year, month=month)
    ensure_path_exists(package_path)
    with open(package_path, 'w', encoding='utf8') as fout:
        fout.write(package)

    # create nav.xhtml
    nav_path = NAV_PATH.format(year=year, month=month)
    ensure_path_exists(nav_path)
    nav_langs = []
    for lang in languages:
        nav_talk_items = []
        for talk in talks:
            talk_path, author, title = talk
            filename = talk_path.split('/')[-1]
            nav_talk_item = templates.NAV_TALK.format(
                lang=lang, 
                filename=filename, 
                author=author, 
                title=title,
            )
            nav_talk_items.append(nav_talk_item)
        lang_name_full = LANGS_FULL[lang]
        nav_langs.append(templates.NAV_LANG.format(lang=lang, language=lang_name_full, talks=''.join(nav_talk_items)))
    nav_data = templates.NAV.format(
        month=MONTHS[month], 
        year=year, 
        contents=''.join(nav_langs),
    )
    with open(nav_path, 'w', encoding='utf8') as fout:
        fout.write(nav_data)
    
    # create title.xhtml
    title_path = TITLE_PATH.format(year=year, month=month)
    ensure_path_exists(title_path)
    with open(title_path, 'w', encoding='utf8') as fout:
        fout.write(templates.TITLE.format(year=year, month=MONTHS[month]))
    
    # create language part files
    for lang in languages:
        lang_part_path = LANG_PATH.format(year=year, month=month, lang=lang)
        ensure_path_exists(lang_part_path)
        lang_directory_path = LANG_DIR.format(year=year, month=month, lang=lang)
        ensure_path_exists(lang_directory_path)
        lang_name_full = LANGS_FULL[lang]
        with open(lang_part_path, 'w', encoding='utf8') as fout:
            fout.write(templates.LANG_PART.format(language=lang_name_full))
    
    # create talks


def ensure_path_exists(path):
    dirs = os.path.dirname(path)
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def main():
    pass


if __name__ == "__main__":
    main()
