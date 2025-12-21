import os
import shutil
import yaml

from File_Handler import rename_files
from integrations.Mail_Handler import download_pdfs 

# Download attachments 
# Rename attachments
# Upload to dropbox

def main():

    DIR_PATH = '../data'
    PDF_TYPE = 'invoice'
    DOWNLOAD = False

    if DOWNLOAD:
        download_pdfs()

    rename_files(dir_path= DIR_PATH, pdf_type= PDF_TYPE)


if __name__ == "__main__":
    main()