from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from datetime import datetime
from calendar import day_name
from datetime import timedelta, timezone, date
from dateutil.parser import parse

from os.path import expanduser
home = expanduser("~")

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def suffix(day_of_month):
    """
    Returns suffix for day of the month to make
    dates look pretty for eventual plotting
    
    """
    if day_of_month in [1,21,31]:
        ending = 'st'
    elif day_of_month in [2,22]:
        ending = 'nd'
    elif day_of_month in [3,23]:
        ending = 'rd'
    else:
        ending = 'th'
    return ending

def prettify_dates(date_list):
    """Input should be a python datetime object"""
    pretty_dates = []
    for day in date_list:
        label_info = {
            'weekday':day_name[day.weekday()],
            'day_of_month':day.day,
            'suffix':suffix(day.day)
        }
        label = '{weekday}, {day_of_month}{suffix}'.format(**label_info)
        pretty_dates.append(label)    
    pretty_dates[0] = 'Today'   
    return pretty_dates    

class GmailClient:
    """
    This calls the gmail api and gets a list of messages from the users inbox.

    This requires a credentials file stored in ~/cyborg/credentials.json

    Follow the instructions at the following link to enable the gmail api
    via your developer console and then download a credentials file.
    https://developers.google.com/gmail/api/quickstart/python

    An example of how to run this:
    
    >>> from gmail_client import GmailClient
    >>> gmail = GmailClient('/Users/Jack/config/cyborg/credentials.json')
    >>> daily_emails = gmail.count_daily_emails()
    >>> print(daily_emails)

    """

    def __init__(self, credentials_path: str):
        """
        Args:
            credentials_path (string): Follow the instructions at the
                following link to enable the gmail api via your developer
                console and then download a credentials file.
                https://developers.google.com/gmail/api/quickstart/python

        """
        # this will generate a token.json file in the current working 
        # directory if it doesn't already exhist
        store = file.Storage('token.json')
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, SCOPES)
            credentials = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=credentials.authorize(Http()))

        self.service = service

    def get_inbox_message_ids(self):
        # Call the Gmail API to get a list of messages in the inbox
        inbox = self.service.users().messages().list(userId='me').execute()
        # Get a list of message ids for all messages in the inbox
        message_ids = [message_dict['id'] for message_dict in inbox['messages']]
        return message_ids

    def get_message_dates(self):
        message_date_strings = []
        for message_id in self.get_inbox_message_ids():
            message = self.service.users().messages().get(
                userId='me',id=message_id).execute()
            headers = message['payload']['headers']
            headers = {item['name']:item['value'] for item in headers}
            date = headers['Date']
            message_date_strings.append(date)
        # use the datetime parse function to convert each date string into
        # a python datetime.date() object
        message_dates = [parse(date).date() for date in message_date_strings]
        return message_dates

    def count_daily_emails(self):

        message_dates = self.get_message_dates()

        today = datetime.today().date()

        daily_email_count = []
        past_two_weeks = [today-timedelta(days=i) for i in range(14)]
        for day in past_two_weeks:
            emails_per_day = message_dates.count(day)
            daily_email_count.append(emails_per_day)       

        formatted_dates = [date.strftime("%y-%m-%d") for date in past_two_weeks]

        pretty_dates = prettify_dates(message_dates)
        
        daily_emails = [
            {
                "date":date,
                "pretty_date":pretty_date,
                "email_count":email_count
            } for (date,pretty_date,email_count) in zip(
                formatted_dates,
                pretty_dates,
                daily_email_count)
            ]

        email_count_info = {
            "daily_emails":daily_emails
        }

        return email_count_info
