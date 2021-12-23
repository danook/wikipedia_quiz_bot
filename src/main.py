from random import shuffle
import tweepy
import requests
import twitter_api_tokens
import wikipedia
import quiz
import tweet
import log

QUIZ_GENERATE_TRIALS = 15

logger = log.get_logger(__name__, "log/test.log")

if __name__ == '__main__':

    with requests.Session() as session:
        page_ids = wikipedia.get_most_viewed_page_ids(session)
        shuffle(page_ids)
        for id in page_ids[:QUIZ_GENERATE_TRIALS]:
            page = wikipedia.get_page_info(id, session)
            generated_quiz = quiz.gen_quiz(page)
            if generated_quiz != quiz.INVALID:
                break

        if generated_quiz == quiz.INVALID:
            # Valid quiz was not generated.
            logger.error("A valid quiz was not generated (trial = {0}).".format(
                QUIZ_GENERATE_TRIALS))

    client = tweepy.Client(
        bearer_token=twitter_api_tokens.BEARER_TOKEN,
        consumer_key=twitter_api_tokens.API_KEY,
        consumer_secret=twitter_api_tokens.API_KEY_SECRET,
        access_token=twitter_api_tokens.ACCESS_TOKEN,
        access_token_secret=twitter_api_tokens.ACCESS_TOKEN_SECRET)

    tweet_id = tweet.tweet(client, generated_quiz)
    if tweet_id == -1:
        # Tweet failed.
        exit(1)

    tweet.save_tweet('data/prev_tweet.json', tweet_id, generated_quiz.answer)
    exit(0)
