import tweepy
import json
import log
import quiz

POLL_DURATION_MINUTES = 1440

logger = log.get_logger(__name__, "log/test.log")


def error_to_str(error):
    return error.message + "(error code: {0})".format(error.code)


def save_tweet(file, tweet_id, answer):
    # Saves tweet id and the answer as json.
    save_data = {'tweet_id': tweet_id, 'answer': answer}
    with open(file, 'w', encoding='UTF-8') as f:
        json.dump(save_data, f, indent=4)
    logger.info("Saved the tweet data to " + file)


def load_tweet(file):
    # Loads tweet id and the answer from json
    with open(file, encoding='UTF-8') as f:
        data = json.load(f)
    return data['tweet_id'], data['answer']


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
                "Tweet error (in replying the answer): " + error_to_str(error))
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
            logger.error("Tweet error: " + error_to_str(error))
        return -1
    else:
        logger.info("Tweeted successfully.")
        tweet_id = int(response.data['id'])
        logger.debug("Tweet ID: {0}".format(tweet_id))
        return tweet_id
