from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import matplotlib.pylab as plt

from datetime import datetime
from calendar import day_name
from datetime import timedelta, timezone, date
from dateutil.parser import parse

from os.path import expanduser
home = expanduser("~")

def suffix(day_of_month):
    """ 
    Return the suffix for a given day of the month
    
    Arguments:
        day_of_month (int): day of the month    

    Returns:
        ending (string): suffix for the day of the month

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


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

class gmail_client(object):
    """
    This calls the gmail api and gets a list of messages from the users inbox.

    This requires a credentials file stored in ~/cyborg/credentials.json

    Follow the instructions at the following link to enable the gmail api
    via your developer console and then download a credentials file.
    https://developers.google.com/gmail/api/quickstart/python

    An example of how to run this:
    
    >>> from gmail_client import gmail_client
    >>> gmail = gmail_client('/Users/Jack/config/cyborg/credentials.json')
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
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credentials_path, SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))

        self.service = service


    def get_inbox_message_ids(self):
        # Call the Gmail API to get a list of messages in the inbox
        inbox = self.service.users().messages().list(userId='me').execute()
        # Get a list of message ids for all messages in the inbox
        message_ids = [message_dict['id'] for message_dict in inbox['messages']]
        return message_ids

    def count_daily_emails(self):
        """
        Returns the emails per day form the last two weeks.


        """
        # get the date from each message
        # this is obtained as a string
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
        inbox_dates = [parse(date).date() for date in message_date_strings]
        today = datetime.today().date()

        daily_emails = []
        past_two_weeks = [today-timedelta(days=i) for i in range(14)]
        for day in past_two_weeks:
            emails_per_day = inbox_dates.count(day)
            daily_emails.append(emails_per_day)


        nice_date_labels = []
        for day in past_two_weeks:
            label_info = {
                'weekday':day_name[day.weekday()],
                'day_of_month':day.day,
                'suffix':suffix(day.day)
            }
            label = '{weekday}, {day_of_month}{suffix}'.format(**label_info)
            nice_date_labels.append(label)
        nice_date_labels[0] = 'Today'      

        return list(zip(past_two_weeks, nice_date_labels, daily_emails))
