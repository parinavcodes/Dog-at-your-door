import pickle
import base64
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from abspath import resource_path


def emailer():
    load_dotenv()
    emails = []
    with open(resource_path("email_token.pickle"), 'rb') as token:
        cred = pickle.load(token)
    with open(resource_path("email_list.txt"), 'rt') as f:
        emails = f.read().rstrip('\n').split('\n')
    service = build('gmail', 'v1', credentials=cred)

    mime_message = MIMEMultipart()
    message = "Jerry at the door"
    mime_message['to'] = ';'.join(emails)
    mime_message['subject'] = "Jerry at the door"
    mime_message.attach(MIMEText(message, 'plain'))
    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

    message = service.users().messages().send(
        userId='me', body={'raw': raw_string}).execute()
    # print(message)


# emailer()
