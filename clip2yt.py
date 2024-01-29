import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up OAuth 2.0 credentials
CLIENT_SECRETS_FILE = "./client_secret.json"  # Replace with your client secrets file
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
credentials = flow.run_local_server(port=0)

# Create a YouTube API service
youtube = build(API_NAME, API_VERSION, credentials=credentials)

# Specify video details
video_title = "My Video Title"
video_description = "Description for my video"
video_tags = ["tag1", "tag2"]

# Upload video
request_body = {
    "snippet": {
        "title": video_title,
        "description": video_description,
        "tags": video_tags
    },
    "status": {
        "privacyStatus": "private"  # You can change this to "public" if you want the video to be public
    }
}

media = MediaFileUpload("", chunksize=-1, resumable=True)

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
