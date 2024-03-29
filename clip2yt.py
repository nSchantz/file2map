import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
     
def upload(video, video_title, video_description): 
    # Set up OAuth 2.0 credentials
    CLIENT_SECRETS_FILE = "./api/client_secret.json"
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)

    # Create a YouTube API service
    youtube = build(API_NAME, API_VERSION, credentials=credentials)

    # Upload video
    request_body = {
        "snippet": {
            "title": video_title,
            "description": video_description,
            "tags": ["travel", "motorcycle", "solo travel", "cross country", "v-strom", "vstrom", "gopro"]
        },
        "status": {
            "privacyStatus": "public"
        }
    }

    print(f"Uploading {video_title}...")

    media = MediaFileUpload(video, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part=",".join(request_body.keys()),
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Video uploaded successfully! Video ID: {response['id']}")

    if response['id']:
        return response['id']
    else:
        return None
