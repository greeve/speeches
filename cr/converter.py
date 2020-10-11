#!/usr/bin/env python3

"""
Convert Conference Addresses for the apostles from churchofjesuschrist.org
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os
import re

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from logger import setup_logger

logger = setup_logger(logfile=None)


FOLDER_HTML = '{year}/{month}/{lang}/html/'
FOLDER_MD = '{year}/{month}/{lang}/md/'
FILEPATH_MD = FOLDER_MD + '{slug}.md'

EMPTY_LINE = r'^\s*$'
LINE_SPACES = r'^ +'
NOTE_NUMBER = r'^(\d+)\.'
NOTE_NUMBER2 = r'\[(\d+)\]\(/#note\d+\)'
NOTES_REGEX = re.compile(NOTE_NUMBER, re.MULTILINE)
NOTES_REGEX2 = re.compile(NOTE_NUMBER2, re.MULTILINE)
SPACES_REGEX = re.compile(LINE_SPACES, re.MULTILINE)

CONTENT_TEMPLATE = '{body}\n\n## References\n\n{notes}'


def convert_talks(year, month, lang):
    """
    """
    md_dir = FOLDER_MD.format(year=year, month=month, lang=lang)
    ensure_path_exists(md_dir)

    html_dir = FOLDER_HTML.format(year=year, month=month, lang=lang)
    for filepath in os.scandir(html_dir):
        content = ''
        with open(filepath) as fin:
            data = fin.read()

        soup = BeautifulSoup(data, 'html.parser')

        section = soup.find_all(
            'article',
            class_='global-template-mobile_article',
        )[0]

        panel = soup.find_all('div', class_='panelContent-2dg-k')[1]

        body = md(str(section), heading_style='ATX')
        body = re.sub(SPACES_REGEX, '', body)
        body = re.sub(NOTES_REGEX2, '[^\\1]', body)

        notes = md(str(panel), heading_style='ATX', strip=['a'])
        notes = notes.replace('\n\n', '\n')
        notes = re.sub(NOTES_REGEX, '[^\\1]: ', notes)
        notes = re.sub(SPACES_REGEX, '', notes)

        content = CONTENT_TEMPLATE.format(
            body=body.strip(),
            notes=notes.strip(),
        )

        _, slug = os.path.split(filepath)
        slug = slug.replace('.html', '')

        filename = FILEPATH_MD.format(
            year=year,
            month=month,
            lang=lang,
            slug=slug,
        )

        logger.info(filename)

        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(content)


def ensure_path_exists(path):
    dirs = os.path.dirname(path)
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def main(args):
    """
    Main entry point of the app
    """
    logger.info(args)
    convert_talks(args.year, args.month, args.lang)


if __name__ == "__main__":
    """
    This is executed when run from the command line
    """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("year", help="The year of the conference (e.g. 2017).")
    parser.add_argument(
        "month",
        help="The month of the conference (i.e. 04 or 10).",
    )

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        '-l',
        '--lang',
        action='store',
        dest='lang',
        default='eng',
    )

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)",
    )

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    args = parser.parse_args()
    main(args)
