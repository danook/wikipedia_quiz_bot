import json
import googleapiclient.discovery
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import log
import tokens

logger = log.get_logger(__name__)

INVALID = -1

TWEET_OPTIONS = 4
MAX_TWEET_LENGTH = 140
MAX_POLL_OPTION_LENGTH = 25


def error_to_str(code, message):
    return message + "(error code: {0})".format(code)

# TODO: Handle Google Drive API in a different file?
# TODO: Maybe we can integrate the rest of utils.py with tokens.py
# TODO: Move error_to_str to log.py?


def get_google_drive_service():
    creds = Credentials.from_authorized_user_info(
        json.loads(tokens.GOOGLE_DRIVE_API_TOKENS))
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            logger.info(
                "Failed to get valid Google Drive API credentials from the user info")
            return INVALID

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
        fileId=tokens.GOOGLE_DRIVE_FILE_ID,
        media_body=media).execute()
    logger.info('Updated the file in Google Drive successfully')


def load_tweet(google_drive_service):
    # Load the file content as byte string
    file_id = tokens.GOOGLE_DRIVE_FILE_ID
    content = google_drive_service.files().get_media(fileId=file_id).execute()

    # Load tweet id and the answer from json
    json_data = json.loads(content.decode('utf-8'))
    logger.info('Loaded the file from Google Drive successfully')
    return json_data.get('tweet_id'), json_data.get('answer')
