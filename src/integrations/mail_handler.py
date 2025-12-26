import msal
import sys
import os
import imaplib
import base64
import requests
from datetime import datetime, timezone, timedelta
import yaml
import sys
sys.path.append("..")
from utils import write_log



from dotenv import load_dotenv 

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SCOPES = ['IMAP.AccessAsUser.All', 'Mail.Read', 'Mail.ReadWrite']
AUTHORITY = "https://login.microsoftonline.com/common"


def get_access_token():
    try:
        app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
        result = app.acquire_token_interactive(scopes=SCOPES, prompt='select_account')
        return result
    except Exception as e:
        print(f'Cannot connect to email {str(e)}')
        write_log(f'Cannot connect to email {str(e)}')
        return None


def download_pdfs(dir_path):

    with open('../configs/email.conf.yaml', 'r') as f:
        trusted_mails = yaml.safe_load(f)

    token_result = get_access_token()
    date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%SZ')

    if not token_result or "access_token" not in token_result:
        print('Token not found')
        write_log('Token not found')
        return None
    
    access_token = token_result['access_token']
    headers = {'Authorization': f'Bearer {access_token}'}
    url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=receivedDateTime ge {date} and hasAttachments eq true&$orderby=receivedDateTime desc&$top=10"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json() 
            messages = data.get('value', [])
            if not messages:
                return 'No Emails found'
            
            pdf_count = 0 

            for mail in messages:
                message_id = mail['id']
                subject = mail['subject'] 
                mail_address = mail['sender']['emailAddress']['address']

                if mail_address not in trusted_mails:
                    print(f'Address not trusted {mail_address} will not download')
                    write_log(f'Address not trusted {mail_address} will not download')
                    continue
                
                attach_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}/attachments"
                attach_response = requests.get(attach_url, headers= headers)

                if attach_response.status_code == 200:
                    attach_data = attach_response.json()
                    attachments = attach_data.get('value', [])

                    for attachment in attachments:
                        if attachment.get('contentType') == 'application/pdf' or attachment.get('name', '').lower().endswith('.pdf'):
                            content_bytes = attachment.get('contentBytes')
                            if content_bytes:
                                filename = attachment['name']
                                filepath = os.path.join(dir_path, filename)

                                with open(filepath, 'wb') as f:
                                    f.write(base64.b64decode(content_bytes))
                                pdf_count += 1
                                print(f'downloaded {filename} from {subject}')
                                write_log(f'downloaded {filename} from {subject}')
            return write_log(pdf_count, "count")
        else:
            print(f"Graph API Error: {response.status_code}")
            print(response.text)
            write_log(f"Graph API Error: {response.status_code}")
            return None

    except Exception as e:
        print(f"Code Error: {e}")
        return None

