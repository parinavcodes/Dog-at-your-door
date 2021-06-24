import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

sid = os.getenv("SID")
auth_token = os.getenv("AUTH_TOKEN")


def messager():
    client = Client(sid, auth_token)

    sender_no = ""
    receiver_no = ""

    body = "hi"
    message = client.messages.create(
        to=receiver_no, from_=sender_no, body=body)
