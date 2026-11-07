import os
import pickle
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video():
    creds = Credentials.from_authorized_user_info(
        {
            "refresh_token": os.environ["YOUTUBE_REFRESH_TOKEN"],
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "token_uri": "https://oauth2.googleapis.com/token",
        },
        SCOPES,
    )

    creds.refresh(google.auth.transport.requests.Request())
    youtube = build("youtube", "v3", credentials=creds)

    video = MediaFileUpload("video.mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": os.environ.get("VIDEO_TITLE", "Food Benefits TV"),
                "description": os.environ.get("VIDEO_DESCRIPTION", ""),
                "categoryId": "26",
            },
            "status": {"privacyStatus": "private"},
        },
        media_body=video,
    )

    response = request.execute()
    print("Uploaded video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
