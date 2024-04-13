from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from utils.settings import get_extension_settings

from os.path import exists

GOOGLE_EXT_NAME = "google_apis"
TOKEN_PATH = "./credentials/google-token.json"

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def init_google_api():
        
    credentials = None

    if exists(TOKEN_PATH):
        credentials = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            default_settings = {
                "installed": {
                    "client_id": "YOUR_CLIENT_ID",
                    "project_id": "YOUR_PROJECT_ID",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": "YOUR_CLIENT_SECRET",
                    "redirect_uris": ["http://localhost"]
                }
            }
            settings = get_extension_settings(GOOGLE_EXT_NAME, default_settings)
            flow = InstalledAppFlow.from_client_config(settings, SCOPES)
            credentials = flow.run_local_server(port=0)
            
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(credentials.to_json())
    
    return credentials