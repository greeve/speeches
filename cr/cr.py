#!/usr/bin/env python3

"""
Download the Apostles' General Conference talks and create a conference report
"""

__author__ = "Greg Reeve"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import requests

from bs4 import BeautifulSoup
from logger import setup_logger

logger = setup_logger(logfile=None)


class Conference:

    CR_ROOT = 'https://www.churchofjesuschrist.org/general-conference'
    CR_PATH = '/{year}/{month}'
    CR_URL = CR_ROOT + CR_PATH
    TALK_URL = CR_URL + '/{slug}'

    LANGUAGES = {
        'eng': 'English',
        'hun': 'Hungarian',
    }

    TITLE = '{language} Conference Addresses'

    SESSIONS = {
        'Saturday Morning Session': 'sat-am',
        'Saturday Afternoon Session': 'sat-pm',
        'General Priesthood Session': 'sat-ps',
        'Sunday Morning Session': 'sun-am',
        'Sunday Afternoon Session': 'sun-pm',
        'Szombat délelőtti ülés': 'sat-am',
        'Szombat délutáni ülés': 'sat-pm',
        'Általános papsági ülés': 'sat-ps',
        'Vasárnap délelőtti ülés': 'sun-am',
        'Vasárnap délutáni ülés': 'sun-pm',
    }

    APOSTLES = [
        'D. Todd Christofferson',
        'Dale G. Renlund',
        'Dallin H. Oaks',
        'David A. Bednar',
        'Dieter F. Uchtdorf',
        'Gary E. Stevenson',
        'Henry B. Eyring',
        'Jeffrey R. Holland',
        'M. Russell Ballard',
        'Quentin L. Cook',
        'Robert D. Hales',
        'Ronald A. Rasband',
        'Russell M. Nelson',
        'Thomas S. Monson',
    ]

    IGNORE_SECTIONS = [
        "Conference Music",
        "Additional Resources",
        "About General Conference",
        "General Women's Session",
        "Általános női ülés",
    ]

    IGNORE_TITLES = [
        'The Sustaining of Church Officers',
    ]

    FILEPATH = '{year}/{month}/{lang}/gc_{year}_{month}_{session_abrv}_{order}_{last_name}.text'  # noqa

    def __init__(self, year, month, lang):
        self.year = year
        self.month = month
        self.lang = lang
        self.language = self.LANGUAGES[lang]
        self.talks = []
        self.title = self.TITLE.format(language=self.language)

    def download_talks(self):
        url = self.CR_URL.format(year=self.year, month=self.month)
        params = {'lang': self.lang}
        r = requests.get(url, params=params)
        talks = self.parse_response(r)
        return talks

    def parse_response(self, response):
        soup = BeautifulSoup(response.content, 'html.parser')
        sections = soup.find_all('div', class_='section')
        return list(self._parse_sections(sections))

    def _parse_sections(self, sections):
        for section in sections:
            section_title = section.find_all(
                'span',
                class_='section__header__title',
            )[0].text
            if section_title not in self.IGNORE_SECTIONS:
                speakers = section.find_all('div', class_='lumen-tile__content')
                for index, speaker in enumerate(speakers):
                    if speaker.text in self.APOSTLES:
                        title = (
                            speaker.previous_sibling.previous_sibling.text.strip()
                        )
                        if title not in self.IGNORE_TITLES:
                            href = speaker.parent.parent['href']
                            slug = href.split('?')[:1][0].split('/')[-1]
                            author = speaker.text
                            last_name = author.split(' ')[-1].lower(),
                            order = index + 1
                            session = section_title
                            session_abrv = self.SESSIONS[section_title]
                            filepath = self.FILEPATH.format(
                                year=self.year,
                                month=self.month,
                                session_abrv=session_abrv,
                                order=order,
                                last_name=last_name,
                                lang=self.lang,
                            )

                            url = self.TALK_URL.format(
                                year=self.year,
                                month=self.month,
                                slug=slug,
                                lang=self.lang,
                            )

                            yield Talk.from_url(
                                url,
                                self.lang,
                                author=author,
                                title=title,
                                slug=slug,
                                session=session,
                                order=order,
                                filepath=filepath,
                            )


class Talk:

    SESSIONS = {
        'Saturday Morning Session': 'sat-am',
        'Saturday Afternoon Session': 'sat-pm',
        'General Priesthood Session': 'sat-ps',
        'Sunday Morning Session': 'sun-am',
        'Sunday Afternoon Session': 'sun-pm',
        'Szombat délelőtti ülés': 'sat-am',
        'Szombat délutáni ülés': 'sat-pm',
        'Általános papsági ülés': 'sat-ps',
        'Vasárnap délelőtti ülés': 'sun-am',
        'Vasárnap délutáni ülés': 'sun-pm',
    }

    def __init__(self, author, title, slug, session, order, filepath, full_text):
        self.author = author
        self.title = title
        self.slug = slug
        self.session = session
        self.session_abrv = self.SESSIONS[session]
        self.order = order
        self.filepath = filepath
        self.full_text = full_text

    @classmethod
    def from_url(cls, url, lang,  **kwargs):
        author = kwargs.get('author')
        title = kwargs.get('title')
        slug = kwargs.get('slug')
        session = kwargs.get('session')
        order = kwargs.get('order')
        filepath = kwargs.get('filepath')

        talk = cls(
            author,
            title,
            slug,
            session,
            order,
            filepath,
            None,
        )

        talk.full_text = talk.download_to_markdown(url, lang)
        return talk

    def download_to_markdown(self, url, lang):
        data = []
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        section = soup.find_all(
            'section',
            class_='article-page lumen-template-read',
        )[0]

        # title
        title = section.find_all('h1', class_='title')[0].text

        # author
        if lang == 'eng':
            author = section.find_all('a', class_='article-author__name')[0].text.replace('By ', '')  # noqa
        else:
            author = section.find_all('div', class_='article-author')[0].text.split('\n')[1:][0].strip()  # noqa

        data.append('# {} <br />{}'.format(author, title))

        # address content
        content = section.find_all('div', class_='body-block')[0]

        # speech paragraphs
        paragraphs = content.find_all('p')

        # modify footnotes in each paragraph
        for p in paragraphs:
            footnotes = p.find_all('sup', class_='marker')
            if footnotes:
                for f in footnotes:
                    f.string.replace_with('[^{}]'.format(f.string))

        speech = '\n\n'.join([p.text for p in content.find_all('p')])
        data.append(speech)

        # references
        references = section.find(id='toggledReferences')

        if references:
            notes = references.find_all('li')
            for n in notes:
                note = n.find_all('p')[0]
                n.string = '[^{}]: {}'.format(n['data-marker'].replace('.', ''), note.text)  # noqa
            footnotes = '\n'.join([n.text for n in notes])
            data.append(footnotes)

        return '\n\n'.join(data)


class ConferenceReport:

    MONTHS = {
        '04': 'April',
        '10': 'October',
    }

    TITLE = '{month} {year} Conference Report'

    def __init__(self, year, month, conferences):
        self.year = year
        self.month = month
        self.month_name = self.MONTHS[month]
        self.conferences = conferences
        self.title = self.TITLE.format(
            month=self.MONTHS[month],
            year=year,
        )

    def create_epub(self):
        return


def main(args):
    """
    Main entry point of the app
    """
    logger.info(args)
    eng_conference = Conference(args.year, args.month, args.languages[0])
    eng_conference.talks = eng_conference.download_talks()
    logger.info(len(eng_conference.talks))
    logger.info(eng_conference.talks[-1].full_text)


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
