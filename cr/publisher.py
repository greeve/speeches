#!/usr/bin/env python3

"""
Publish Conference Addresses for the apostles from churchofjesuschrist.org
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os

from logger import setup_logger

logger = setup_logger(logfile=None)


PANDOC_CMD = 'pandoc -o cr_{year}{month}.epub {title} {talks}'
MONTHS = {
    '04': 'April',
    '10': 'October',
}
TITLE = '{month} {year} Conference Report'
TITLE_TEMPLATE = """---
title: {title}
author: Greg Reeve
rights:  Creative Commons Non-Commercial Share Alike 3.0
language: en-US
---
"""

FOLDER_ROOT = '{year}/{month}'
FOLDER_LANG = FOLDER_ROOT + '/{lang}'
FOLDER_MD = FOLDER_LANG + '/md/'
TITLE_FILE = FOLDER_ROOT + '/title.md'


def make_title(year, month):
    """
    """
    filepath = TITLE_FILE.format(year=year, month=month)
    month = MONTHS.get(month)
    title = TITLE.format(month=month, year=year)
    contents = TITLE_TEMPLATE.format(title=title)

    with open(filepath, 'w') as fout:
        fout.write(contents)


def gather_talks(year, month, languages):
    """
    """
    talks = []
    for lang in languages:
        folder_md = FOLDER_MD.format(year=year, month=month, lang=lang)
        for filepath in os.scandir(folder_md):
            talks.append(filepath.path)

    talks.sort(key=lambda x: x.split('/')[-1])
    return talks


def create_epub_cmd(year, month, talks):
    """
    """
    title_file = TITLE_FILE.format(year=year, month=month)
    talks_str = ' '.join(talks)
    command = PANDOC_CMD.format(
        year=year,
        month=month,
        title=title_file,
        talks=talks_str,
    )
    print(command)
    return


def main(args):
    """
    Main entry point of the app
    """
    logger.info(args)
    make_title(args.year, args.month)
    talks = gather_talks(args.year, args.month, args.languages)
    create_epub_cmd(args.year, args.month, talks)


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
        '--languages',
        action='store',
        dest='languages',
        default=['eng', 'hun'],
        nargs='+',
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
