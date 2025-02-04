import base64
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from agent.utils import get_google_credentials

class GmailTools:
    def __init__(self):
        self.service = build('gmail', 'v1', credentials=get_google_credentials())

    def create_draft_email(self, recipient, subject, html_email_content):
        try:
            message = self._create_message(recipient, subject, html_email_content)
            draft = self.service.users().drafts().create(userId='me', body={
                'message': {
                    'raw': self._encode_message(message)
                }
            }).execute()
            print(f"Draft created for email for {recipient} with subject '{subject}'")
            return draft
        except Exception as error:
            print(f"An error occurred while creating draft: {error}")
            return None
        
    def send_email(self, recipient, subject, html_email_content):
        try:
            message = self._create_message(recipient, subject, html_email_content)
            sent_message = self.service.users().messages().send(userId='me', body={
                'raw': self._encode_message(message)
            }).execute()
            print(f"Email sent to {recipient} with subject '{subject}'")
            return sent_message
        except Exception as error:
            print(f"An error occurred while sending reply: {error}")
            return None

    def _create_message(self, recipient, subject, html_email_content):
        message = MIMEText(html_email_content, 'html')
        message['to'] = recipient
        message['subject'] = subject
        message['from'] = 'tekbyb@gmail.com'  
        return message

    def _encode_message(self, message):
        return base64.urlsafe_b64encode(message.as_bytes()).decode()