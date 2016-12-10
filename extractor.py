import requests
from bs4 import BeautifulSoup

URL_TALK = 'https://www.lds.org/general-conference/{year}/{month}/{slug}?lang=eng'

SLUGS_2016_10 = [
    'emissaries-to-the-church',
    'learn-from-alma-and-amulek',
    'that-he-may-become-strong-also',
    'principles-and-promises',
    'the-perfect-path-to-happiness',
    'joy-and-spiritual-survival',
    'to-whom-shall-we-go',
    'gratitude-on-the-sabbath-day',
    'if-ye-had-known-me',
    'lest-thou-forget',
    'repentance-a-joyful-choice',
]

SELECTOR_TITLE = 'title'
SELECTOR_AUTHOR = 'article-author__name'
SELECTOR_CONTENT = 'article-content'
SELECTOR_NOTES = 'notes'

TALK_TEMPLATE = '{author} <br />{title}\n{content}\n{notes}'

def make_request(url):
    try:
        r = requests.get(url)
    except Exception as e:
        raise(e)
    return r

def cook_soup(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find_all('h1', SELECTOR_TITLE)[0]
    author = soup.find_all(class_=SELECTOR_AUTHOR)[0]
    content = soup.find_all(class_=SELECTOR_CONTENT)[0]
    notes = soup.find_all(class_=SELECTOR_NOTES)[0]
    cooked_soup = {
        'author': author.get_text(),
        'title': title.get_text(),
        'content': content.get_text(),
        'notes': notes.get_text(),
    }
    return cooked_soup

def main():
    # url = input('Enter url: ')
    for slug in SLUGS_2016_10:
        url = URL_TALK.format(year='2016', month='10', slug=slug)
        response = make_request(url)
        cooked_soup = cook_soup(response)
        filename = '{}.text'.format(slug)
        data = TALK_TEMPLATE.format(author=cooked_soup.get('author'), title=cooked_soup.get('title'), content=cooked_soup.get('content'), notes=cooked_soup.get('notes'))
        with open(filename, 'w', encoding='utf-8') as fout:
            fout.write(data)


if __name__ == '__main__':
    main()
