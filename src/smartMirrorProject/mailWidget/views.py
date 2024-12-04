from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.http import JsonResponse
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


# Scopes define the level of access you want
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def fetch_emails():
    # Manually construct the credentials
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": GOOGLE_CLIENT_ID,
                "project_id": "smartmirror-442112",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": ["http://localhost:8000/oauth2callback"]
            }
        },
        SCOPES
    )
    creds = flow.run_local_server(port=0)

    # Run the OAuth flow using the predefined redirect URI
    flow.redirect_uri = "http://localhost:8000/oauth2callback"
    creds = flow.run_local_server(port=8000)  # Use a consistent port

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Fetch the list of messages
    results = service.users().messages().list(userId='me', maxResults=5).execute()
    messages = results.get('messages', [])

    email_data = []
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        snippet = msg.get('snippet', '')
        email_data.append(snippet)

    return email_data

def fetch_mail_view(request):
    try:
        emails = fetch_emails()
        return JsonResponse({"emails": emails})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)