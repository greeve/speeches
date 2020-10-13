#!/usr/bin/env python3

"""
Download Conference Addresses for the apostles from churchofjesuschrist.org
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os
import re
import requests

from bs4 import BeautifulSoup
from logger import setup_logger

logger = setup_logger(logfile=None)


TOC_URL = 'https://www.churchofjesuschrist.org/general-conference/{year}/{month}?lang={lang}'  # noqa
TALK_URL = 'https://www.churchofjesuschrist.org/general-conference/{year}/{month}/{slug}?lang={lang}'  # noqa

APOSTLES = [
    'D. Todd Christofferson',
    'Dale G. Renlund',
    'Dallin H. Oaks',
    'David A. Bednar',
    'Dieter F. Uchtdorf',
    'Gary E. Stevenson',
    'Gerrit W. Gong',
    'Henry B. Eyring',
    'Jeffrey R. Holland',
    'M. Russell Ballard',
    'Neil L. Andersen',
    'Quentin L. Cook',
    'Robert D. Hales',
    'Ronald A. Rasband',
    'Russell M. Nelson',
    'Thomas S. Monson',
    'Ulisses Soares',
]

IGNORE_SECTIONS = [
    "Conference Music",
    "Additional Resources",
    "About General Conference",
    "General Women's Session",
    "General Women’s Session",
    "Általános női ülés",
    "Women’s Session",
]

IGNORE_TITLES = [
    'The Sustaining of Church Officers',
    'Sustaining of General Authorities, Area Seventies, and General Officers of the Church',  # noqa
    'Sustaining of General Authorities, Area Seventies, and General Officers',
    'Solemn Assembly',
    'Church Auditing Department Report, 2017',
    'Ünnepélyes gyülekezet',
    'Az egyházi tisztségviselők támogatása',
    'Az Egyházi Könyvvizsgálói Osztály 2017. évi jelentése',
    'Az egyház általános felhatalmazottainak, területi hetveneseinek és általános tisztségviselőinek támogatása',  # noqa
    'Az általános felhatalmazottak, területi hetvenesek és általános tisztségviselők támogatása',  # noqa
]

FOLDER_HTML = '{year}/{month}/{lang}/html/'
FILEPATH_HTML = FOLDER_HTML + '{slug}.html'


def get_slugs(year, month, lang):
    data = []
    r = requests.get(
        TOC_URL.format(year=year, month=month, lang=lang),
    )
    soup = BeautifulSoup(r.content, 'html.parser')
    sections = soup.find_all('div', class_='section')
    for section in sections:
        section_title = section.find_all(
            'span',
            class_='section__header__title',
        )[0].text
        if section_title not in IGNORE_SECTIONS:
            speakers = section.find_all('div', class_='lumen-tile__content')
            for index, speaker in enumerate(speakers):
                speaker_name = speaker.text.replace('\xa0', ' ')
                if speaker_name in APOSTLES:
                    title = (
                        speaker.previous_sibling.previous_sibling.text.strip()
                    )
                    if title not in IGNORE_TITLES:
                        href = speaker.parent.parent['href']
                        slug = href.split('?')[:1][0].split('/')[-1]
                        data.append((
                            index + 1,
                            speaker.text.split(' ')[-1].lower(),
                            slug,
                        ))
    return data


def download_talks(slugs, year, month, lang):
    """
    """
    paths = []
    for slug_infos in slugs:
        order, last_name, slug = slug_infos

        filename = FILEPATH_HTML.format(
            lang=lang,
            month=month,
            slug=slug,
            year=year,
        )

        ensure_path_exists(filename)
        paths.append(filename)

        r = requests.get(TALK_URL.format(
            lang=lang,
            month=month,
            slug=slug,
            year=year,
        ))

        soup = BeautifulSoup(r.content, 'html.parser')

        logger.info(filename)
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(str(soup))

    return paths


def ensure_path_exists(path):
    dirs = os.path.dirname(path)
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def main(args):
    """
    Main entry point of the app
    """
    logger.info("hello world")
    logger.info(args)
    slugs = get_slugs(args.year, args.month, args.lang)
    paths = download_talks(slugs, args.year, args.month, args.lang)


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
