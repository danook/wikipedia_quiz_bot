import json
import googleapiclient.discovery
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
import log
import tokens

logger = log.get_logger(__name__)

INVALID = -1

TWEET_OPTIONS = 4
MAX_TWEET_LENGTH = 140

TMP_PATH = '/tmp/'
GOOGLE_DRIVE_FILE_ID = '1lislCoO16jPtH4mMIjBuuaJxcqoqcOdF'  # TODO: Set this to env?


def error_to_str(code, message):
    return message + "(error code: {0})".format(code)


# TODO: Handle Google Drive API in a different file?
# TODO: Maybe we can integrate the rest of utils.py with tokens.py
# TODO: Move error_to_str to log.py?

def get_google_drive_service():
    creds = Credentials.from_authorized_user_info(
        json.loads(tokens.GOOGLE_DRIVE_API_TOKENS))
    print(creds)
    if not creds:
        logger.error("Failed to get valid Google Drive API credentials")
    service = googleapiclient.discovery.build(
        'drive', 'v3', credentials=creds)
    return service


# Saves the tweet id and the answer as a json file and uploads it to Google Drive
# Returns the file ID
def save_tweet(tweet_id, answer, google_drive_service):
    save_data = {'tweet_id': tweet_id, 'answer': answer}
    media = MediaInMemoryUpload(json.dumps(save_data).encode('utf-8'),
                                mimetype='application/json')
    google_drive_service.files().update(
        fileId=GOOGLE_DRIVE_FILE_ID,
        media_body=media).execute()
    logger.info('Updated the file in Google Drive successfully')


def load_tweet(google_drive_service):
    # Load the file content as byte string
    file_id = GOOGLE_DRIVE_FILE_ID
    content = google_drive_service.files().get_media(fileId=file_id).execute()

    # Load tweet id and the answer from json
    json_data = json.loads(content.decode('utf-8'))
    logger.info('Loaded the file from Google Drive successfully')
    return json_data.get('tweet_id'), json_data.get('answer')
