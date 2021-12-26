from random import shuffle
import tweepy
import requests
import tokens
import wikipedia
import quiz
import tweet
import log
import utils

QUIZ_GENERATE_TRIALS = 15

logger = log.get_logger(__name__)


def reply_answer(client: tweepy.Client):
    tweet_id, answer = utils.load_tweet('data/prev_tweet.json')
    reply_id = tweet.reply_answer(client, tweet_id, answer)
    if reply_id == utils.INVALID:
        return 1
    return 0


def generate_and_tweet_quiz(client: tweepy.Client):
    with requests.Session() as session:
        page_ids = wikipedia.get_most_viewed_page_ids(session)
        shuffle(page_ids)
        for id in page_ids[:QUIZ_GENERATE_TRIALS]:
            page = wikipedia.get_page_info(id, session)
            generated_quiz = quiz.gen_quiz(page)
            if generated_quiz != utils.INVALID:
                break

        if generated_quiz == utils.INVALID:
            # Valid quiz was not generated.
            logger.error("A valid quiz was not generated (trial = {0}).".format(
                QUIZ_GENERATE_TRIALS))

    tweet_id = tweet.tweet(client, generated_quiz)
    if tweet_id == utils.INVALID:
        # Tweet failed.
        return 1

    utils.save_tweet('data/prev_tweet.json', tweet_id, generated_quiz.answer)
    return 0


if __name__ == '__main__':

    client = tweepy.Client(
        bearer_token=tokens.TWITTER_BEARER_TOKEN,
        consumer_key=tokens.TWITTER_API_KEY,
        consumer_secret=tokens.TWITTER_API_KEY_SECRET,
        access_token=tokens.TWITTER_ACCESS_TOKEN,
        access_token_secret=tokens.TWITTER_ACCESS_TOKEN_SECRET)

    reply_answer(client)
    generate_and_tweet_quiz(client)
