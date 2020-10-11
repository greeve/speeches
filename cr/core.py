#!/usr/bin/env python3

"""
Download Conference Addresses for the apostles from churchofjesuschrist.org

python core.py YYYY MM
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import extractor
import converter
import publisher

from logger import setup_logger

logger = setup_logger(logfile=None)


def main(args):
    """
    Main entry point of the app
    """
    logger.info(args)
    if args.action == 'download':
        for lang in args.languages:
            slugs = extractor.get_slugs(args.year, args.month, lang)
            paths = extractor.download_talks(
                slugs,
                args.year,
                args.month,
                lang,
            )

    if args.action == 'convert':
        for lang in args.languages:
            converter.convert_talks(args.year, args.month, lang)

    if args.action == 'publish':
        publisher.make_title(args.year, args.month)
        talks = publisher.gather_talks(args.year, args.month, args.languages)
        publisher.create_epub_cmd(args.year, args.month, talks)


if __name__ == "__main__":
    """
    This is executed when run from the command line
    """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("action", help="The action to perform.")
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
