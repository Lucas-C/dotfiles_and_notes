#!/usr/bin/env python3
import json, os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

def get_creds(credentials_file="credentials.json", token_file="token.json"):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())
    return creds

def dump_file_acls(pageSize=100):
    service = build("drive", "v3", credentials=get_creds())
    # Adjust the 'q' parameter if you want to target a specific folder or file type
    results = service.files().list(
        pageSize=pageSize, 
        fields="nextPageToken, files(id, name, mimeType)",
        includeItemsFromAllDrives=True,  # Optional: Includes shared drives
        supportsAllDrives=True
    ).execute()
    files = results.get("files", [])
    print(f"Found {len(files)} files. Fetching permissions...")
    
    acl_dump = []
    for file in files:
        try:
            perm_results = service.permissions().list(
                fileId=file["id"],
                fields="permissions(id, type, role, emailAddress)",
                supportsAllDrives=True
            ).execute()
            acl_dump.append({
                "file_name": file["name"],
                "file_id": file["id"],
                "mime_type": file["mimeType"],
                "permissions": perm_results.get("permissions", [])
            })
        except Exception as error:
            print("File ID:", file["id"], "- File name:", file["name"], "- Error:", error)

    with open("google_drive_acl_dump.json", "w", encoding="utf-8") as f:
        json.dump(acl_dump, f, indent=4, ensure_ascii=False)
    print("ACL dump completed! Data saved to google_drive_acl_dump.json")

if __name__ == "__main__":
    dump_file_acls(pageSize=1000)
