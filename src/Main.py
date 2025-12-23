import os
import shutil
import yaml

from File_Handler import rename_files
from integrations.Mail_Handler import download_pdfs 
from integrations.Dropbox_Handler import upload_dropbox

# Security Check using AI? Or just a list with secure emails?
# Download attachments 
# Rename attachments
# Upload to dropbox

def main():

    DIR_PATH = '../data'
    RENAMED_PATH = '../data/processed'
    PDF_TYPE = 'invoice'
    DOWNLOAD = False
    UPLOAD = True
    RENAME = True

    try:
        print('Downloading...')
        if DOWNLOAD:
            download_pdfs()
        print('Renaming...')
        if RENAME:
            rename_files(dir_path= DIR_PATH, pdf_type= PDF_TYPE)
        print('Uploading...')
        if UPLOAD:
            upload_dropbox(dir_path= RENAMED_PATH)
    
    except Exception as e:
        print(str(e))
        raise

if __name__ == "__main__":
    main()