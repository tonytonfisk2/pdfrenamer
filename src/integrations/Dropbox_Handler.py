import webbrowser
from dropbox import Dropbox, DropboxOAuth2FlowNoRedirect
import glob
import os
from dotenv import load_dotenv
import sys
sys.path.append("..")
from utils import write_log

load_dotenv()

ACCESS_TOKEN = os.getenv('DROPBOX_TOKEN')
REFRESH_TOKEN = os.getenv('DROPBOX_REFRESH_TOKEN')
APP_SECCRET = os.getenv('DROPBOX_SECRET')
APP_KEY = os.getenv('DROPBOX_KEY')  

def get_refresh_token():
    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY, 
        APP_SECCRET, 
        token_access_type='offline')
    
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    webbrowser.open(authorize_url)
    auth_code = input("2. Enter the authorization code here: ").strip()
    try:
        oauth_result = auth_flow.finish(auth_code)
        refresh_token = oauth_result.refresh_token
        print(f'Refresh Token: {refresh_token}')
    except Exception as e:
        print(f'Error: {e}')
        return None
    
def get_dropbox_client():
    if not REFRESH_TOKEN:
        print("ERROR: REFRESH_TOKEN")
        token = get_refresh_token()
        if token:
            print('add to env file')
        sys.exit(1) 


    try:
        dbx = Dropbox(
            oauth2_refresh_token=REFRESH_TOKEN,
            app_key=APP_KEY,
            app_secret=APP_SECCRET
        )

        dbx.users_get_current_account()
    except Exception as e:
        print(f'Error: {e}')
        return None
    return dbx

def upload_dropbox(dir_path):

    dbx = get_dropbox_client()
    if not dbx:
        print('Cant connect to dropbox ')
        return
    
    files = glob.glob(os.path.join(dir_path, '*.pdf'))

    try:
        for file_path in files:
            filename = os.path.basename(file_path)

            with open(file_path, 'rb') as f:
                dbx.files_upload(f.read(), f'/Test/{filename}')
                print(f'Uploaded: {filename}')
                write_log(f'Uploaded: {filename}')
                
    except Exception as e:
        print(f'Error: {e}')
        return
