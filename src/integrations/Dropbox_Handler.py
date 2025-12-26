import webbrowser
from dropbox import Dropbox
import glob
import os
from dotenv import load_dotenv
import sys
sys.path.append("..")
from utils import write_log

load_dotenv()

ACCESS_TOKEN = os.getenv('DROPBOX_TOKEN')

def upload_dropbox(dir_path):
    if not ACCESS_TOKEN:
        print("ERROR: ACCESS_TOKEN")
        return
    
    dbx = Dropbox(ACCESS_TOKEN)
    
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
