from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCal:
    def __init__(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)
        self.calendarId = 'primary' # could also be email address
        calendar_list_entry = self.service.calendarList().get(calendarId=self.calendarId).execute()
        self.time_zone = calendar_list_entry['timeZone']
        print(calendar_list_entry['summary'])
        print(calendar_list_entry)

        self.colors = self.service.colors().get().execute()
        self.eventColors = [c for c in self.colors['event']]

        # Print available calendarListEntry colors.
        # for id, color in colors['calendar'].items():
            # print('colorId: ', id)
            # print('  Background: ', color['background'])
            # print('  Foreground: ',color['foreground'])
        # Print available event colors.
        # for id, color in colors['event'].items():
            # print('colorId: ', id)
            # print('  Background: ', color['background'])
            # print('  Foreground: ', color['foreground'])
    
    def getColorIds(self):
        return self.eventColors

    def addEvent(self, start_time, end_time, title, idx):
        colorId = str(idx % len(self.eventColors))
        event = {
            'summary' : title,
            'start' : {
                'dateTime' : start_time.isoformat(),
                'timeZone' : self.time_zone
            },
            'end' : {
                'dateTime' : end_time.isoformat(),
                'timeZone' : self.time_zone
            },
            'reminders': {
                'useDefault': False
            },
            'colorId' : colorId
        }
        print("Creating event", event)
        event = self.service.events().insert(calendarId=self.calendarId, body=event).execute()
        print('Event created:', event.get('htmlLink'))

