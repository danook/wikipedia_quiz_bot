import re
import random
from wikipedia import WikipediaPage
import log
import utils

logger = log.get_logger(__name__, "log/test.log")


class Quiz:
    def __init__(self, sentence, options, answer):
        self.sentence = sentence
        self.options = options
        self.answer = answer
        pass


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
        return utils.INVALID
    # Extract sentences so that string becomes shorter than 140 characters
    period_index = extract[:(utils.MAX_TWEET_LENGTH - 1)].rfind('。')
    if period_index == -1:
        logger.info("Failed to generate a quiz: the first sentence is longer than the maximum tweet length ({0} letters).".format(
            utils.MAX_TWEET_LENGTH))
        return utils.INVALID
    extract = extract[:(period_index + 1)]
    logger.debug("Generated sentence: " + extract)
    return extract


def get_mutual_link_pages(link_to, linked_from):
    mutual_links = list(set(link_to) & set(linked_from))
    if len(mutual_links) < utils.TWEET_OPTIONS - 1:
        logger.info(
            "Failed to generate a quiz: shortage of mutually-linked pages (there are only {0}).".format(len(mutual_links)))
        return utils.INVALID
    else:
        random.shuffle(mutual_links)
        logger.debug("Quiz options (except the answer): " +
                     ", ".join(mutual_links[:(utils.TWEET_OPTIONS - 1)]))
        return mutual_links[:(utils.TWEET_OPTIONS - 1)]


def gen_quiz(wikipediaPage: WikipediaPage):
    sentence = format_extract(wikipediaPage.title, wikipediaPage.extract)
    if sentence == utils.INVALID:
        return utils.INVALID

    mutual_links = get_mutual_link_pages(
        wikipediaPage.link_to, wikipediaPage.linked_from)
    if mutual_links == utils.INVALID:
        return utils.INVALID
    options = mutual_links
    options.append(wikipediaPage.title)
    random.shuffle(options)
    logger.debug("Generated options: " + ", ".join(options))

    quiz = Quiz(sentence, options, wikipediaPage.title)
    logger.info("Quiz generated successfully.")
    return quiz
