#!/usr/bin/env python3

"""
Construct an epub of talks by apostles for a given conference.
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import os

MIMETYPE_PATH = 'epub/mimetype'
CONTAINER_PATH = 'epub/META-INF/container.xml'

CR_PATH = '{year}/{month}/cr/'
PACKAGE_PATH = 'epub/EPUB/package.opf'
NAV_PATH = 'epub/EPUB/xhtml/nav.xhtml'
TITLE_PATH = 'epub/EPUB/xhtml/title.xhtml'
LANG_PATH = 'epub/EPUB/xhtml/{lang}.xhtml'
LANG_DIR = 'epub/EPUB/xhtml/{lang}/'
TALK_PATH = LANG_DIR + 'talk.xhtml'


def create(year, month, lang, talks):
    # create the mimetype file

    # create the META-INF/container.xml file
    pass


def ensure_path_exists(path):
    dirs = os.path.dirname(path)
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def main():
    pass


if __name__ == "__main__":
    main()
