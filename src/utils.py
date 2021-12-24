import json
import log

logger = log.get_logger(__name__, "log/test.log")

INVALID = -1

TWEET_OPTIONS = 4
MAX_TWEET_LENGTH = 140


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
