import re
import random
from logging import INFO, FileHandler, getLogger
from quiz import Quiz
from wikipedia_page import WikipediaPage

INVALID = -1
OPTIONS = 4
MAX_TWEET_LENGTH = 140

logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(FileHandler("log/test.log"))


def format_extract(title, extract):
    # Remove spaces and text inside brackets
    extract = re.sub('\(.*?\)|（.*?）', '', extract)
    extract = extract.replace(' ', '')
    extract = extract.replace('　', '')
    # Replace the title to '(  )'
    if extract.startswith(title + 'は'):
        extract = extract.replace(title, '(     ) ', 1)
    else:
        logger.info(
            "Failed to generate a quiz: the sentence does not start with the title of the article.")
        return INVALID
    # Extract sentences so that string becomes shorter than 140 characters
    period_index = extract[:(MAX_TWEET_LENGTH - 1)].rfind('。')
    if period_index == -1:
        logger.info("Failed to generate a quiz: the first sentence is longer than the maximum tweet length ({0} letters).".format(
            MAX_TWEET_LENGTH))
        return INVALID
    extract = extract[:(period_index + 1)]
    logger.info("Generated sentence: " + extract)
    return extract


def get_mutual_link_pages(link_to, linked_from):
    mutual_links = list(set(link_to) & set(linked_from))
    if len(mutual_links) < OPTIONS - 1:
        logger.info(
            "Failed to generate a quiz: shortage of mutually-linked pages (there are only {0}).".format(len(mutual_links)))
        return INVALID
    else:
        random.shuffle(mutual_links)
        logger.info("Quiz options (except the answer): " +
                    ", ".join(mutual_links[:(OPTIONS - 1)]))
        return mutual_links[:(OPTIONS - 1)]


def gen_quiz(wikipediaPage: WikipediaPage):
    sentence = format_extract(wikipediaPage.title, wikipediaPage.extract)
    if sentence == INVALID:
        return INVALID

    mutual_links = get_mutual_link_pages(
        wikipediaPage.link_to, wikipediaPage.linked_from)
    if mutual_links == INVALID:
        return INVALID
    options = mutual_links
    options.append(wikipediaPage.title)
    random.shuffle(options)
    logger.info("Generated options: " + ", ".join(options))

    quiz = Quiz(sentence, options, wikipediaPage.title)
    return quiz
