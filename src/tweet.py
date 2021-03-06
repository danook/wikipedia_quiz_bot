import tweepy
import utils
import log
import quiz

POLL_DURATION_MINUTES = 1440

logger = log.get_logger(__name__)


def get_answer_tweet_text(answer):
    return '答え: ' + answer


def reply_answer(client: tweepy.Client, tweet_id, answer):
    response = client.create_tweet(
        in_reply_to_tweet_id=tweet_id,
        text=get_answer_tweet_text(answer)
    )

    if len(response.errors) > 0:
        for error in response.errors:
            logger.error(
                "Tweet error (in replying the answer): " + utils.error_to_str(error.code, error.message))
        return -1
    else:
        logger.info("Replied the answer successfully.")
        tweet_id = int(response.data['id'])
        logger.debug("Reply Tweet ID: {0}".format(tweet_id))
        return tweet_id


def tweet(client: tweepy.Client, quiz: quiz.Quiz):
    response = client.create_tweet(
        poll_duration_minutes=POLL_DURATION_MINUTES,
        poll_options=quiz.options,
        text=quiz.sentence
    )
    if len(response.errors) > 0:
        for error in response.errors:
            logger.error("Tweet error: " +
                         utils.error_to_str(error.code, error.message))
        return -1
    else:
        logger.info("Tweeted successfully.")
        tweet_id = int(response.data['id'])
        logger.debug("Tweet ID: {0}".format(tweet_id))
        return tweet_id
