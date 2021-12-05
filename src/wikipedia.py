import requests
from wikipedia_page import WikipediaPage

LANGUAGE = "ja"
NAMESPACE_MAIN = 0
BASE_URL = 'https://' + LANGUAGE + '.wikipedia.org/w/api.php'


def get_most_viewed_page_ids(session):
    params = {
        'action': 'query',
        'format': 'json',
        'generator': 'mostviewed',
        'gpvimlimit': 100
    }
    resultJson = session.get(
        BASE_URL,
        params=params).json()

    idlist = list()
    for page in resultJson['query']['pages'].values():
        if page['ns'] == NAMESPACE_MAIN:
            idlist.append(page['pageid'])
    return idlist


def get_page_info(id, session):
    params = {
        'action': 'query',
        'format': 'json',
        'prop': 'extracts|links|linkshere',
        'pageids': id,
        'exchars': 200,
        'exintro': 1,
        'explaintext': 1,
        'pllimit': 500,
        'lhlimit': 500
    }
    resultJson = session.get(
        BASE_URL,
        params=params).json()

    pageJson = resultJson['query']['pages'][str(id)]
    wikipediaPage = WikipediaPage(
        pageJson['title'],
        pageJson['extract'],
        [page['title'] for page in pageJson['links']],
        [page['title'] for page in pageJson['linkshere']])
    return wikipediaPage


# TEST
if __name__ == '__main__':
    with requests.Session() as session:
        pageids = get_most_viewed_page_ids(session)
        print(pageids)
        page = get_page_info(pageids[0], session)
        print(page.title)
        print(page.link_to)
        print(page.linked_from)
        print(page.extract)
