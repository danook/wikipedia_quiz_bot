import utils
import log

LANGUAGE = "ja"
NAMESPACE_MAIN = 0
BASE_URL = 'https://' + LANGUAGE + '.wikipedia.org/w/api.php'

logger = log.get_logger(__name__)


class WikipediaPage:
    def __init__(self, title, extract, link_to, linked_from):
        self.title = title
        self.extract = extract
        self.link_to = link_to
        self.linked_from = linked_from


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
    logger.info("Got a list of mostviewed pages")

    if not (resultJson.get('error') is None):
        logger.error(
            "MediaWiki API Error (in getting the most viewed pages): " + utils.error_to_str(resultJson['error']['code'], resultJson['error']['info']))
        return utils.INVALID

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
    logger.info("Got the page data (id={0})".format(id))

    if not (resultJson.get('error') is None):
        logger.error(
            "MediaWiki API Error (in getting the page data): " + utils.error_to_str(resultJson['error']['code'], resultJson['error']['info']))
        return utils.INVALID

    pageJson = resultJson['query']['pages'][str(id)]
    wikipediaPage = WikipediaPage(
        pageJson['title'],
        pageJson['extract'],
        [page['title'] for page in pageJson['links']],
        [page['title'] for page in pageJson['linkshere']])

    return wikipediaPage
