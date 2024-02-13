import logging
import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class YouTubeUploader:
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    CLIENT_SECRETS_FILE = "client_secret.json"
    CREDENTIALS_FILE = "youtube_credentials.pickle"

    def __init__(self):
        self.youtube = self.authenticate_youtube()

    def authenticate_youtube(self):
        credentials = None
        if os.path.exists(self.CREDENTIALS_FILE):
            with open(self.CREDENTIALS_FILE, 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
                credentials = flow.run_local_server(port=0)
            with open(self.CREDENTIALS_FILE, 'wb') as token:
                pickle.dump(credentials, token)
        return build('youtube', 'v3', credentials=credentials)

    def upload_video(self, video_file_path, title, description, category_id, keywords, privacy_status):
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': keywords,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status
            }
        }
        try:
            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=MediaFileUpload(video_file_path, mimetype='video/*')
            )
            response = request.execute()
            logging.info(f"Video uploaded. ID: {response['id']}")
            return response
        except HttpError as e:
            logging.error(f"An HTTP error occurred: {e.resp.status} - {e.content}")
            return None
