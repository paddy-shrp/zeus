import datetime as dt
import time

from googleapiclient.discovery import build

from utils.decorators import *
import utils.dt_formatter as fm
from utils.objects.module import Module

import modules.extensions.google.google_init as g_init

class GoogleCalendar(Module):
    def __init__(self):
        self.credentials = g_init.init_google_api()
 
        self.service = build("calendar", "v3", credentials=self.credentials)
        
        self.data = {}
        self.last_call_timestamp = 0

    @include_get
    def get_calendars(self):
        if self.service == None: return 500

        raw_calendars = self.service.calendarList().list().execute()
        calendars = []
        for raw_calendar in raw_calendars["items"]:

            keys = ["id", "summary", "backgroundColor", "accessRole"]
            calendar = {key: raw_calendar.get(key, "") for key in keys}
            if "summaryOverride" in raw_calendar.keys():
                 calendar["summary"] = raw_calendar["summaryOverride"]
            calendars.append(calendar)

        return calendars
    
    def get_calendar_names(self):
        return [calendar["summary"] for calendar in self.get_calendars()]

    @include_get
    def get_todays_agenda_request(self, calendars:str="primary"):
        timeMin, timeMax = fm.min_max_of_day()
        return self.get_events_request(calendars, timeMin, timeMax)
    
    def get_todays_agenda(self, calendars:list):
        timeMin, timeMax = fm.min_max_of_day()
        return self.get_events(calendars, timeMin, timeMax)
        
    @include_get
    def get_events_request(self, calendars:str="primary", timeMin=None, timeMax = None):
        calendar_names = calendars.split(",")
        return self.get_events(calendar_names, timeMin, timeMax)

    def get_events(self, calendar_names=["primary"], timeMin=None, timeMax=None):
        if self.service == None: return 500

        if "primary" in calendar_names:
             calendar_names.remove("primary")
             calendar_names.append(self.service.calendarList().get(calendarId="primary").execute()["id"])

        total_events = []

        calendars = self.get_calendars()
        for calendar in calendars:
            if (calendar["summary"] not in calendar_names) or (calendar["summary"] not in calendar_names): continue

            params = {
                 "calendarId": calendar["id"],
                 "timeMin": fm.now(),
            }

            if timeMin != None: params["timeMin"] = timeMin
            if timeMax != None: params["timeMax"] = timeMax
            
            raw_events = self.service.events().list(**params).execute()

            events = []
            for raw_event in raw_events["items"]:
                keys = ["calendarName", "summary", "status", "creator", "start", "end", "description", "location", "attachments"]
                event = {key: raw_event.get(key, None) for key in keys}
                event["calendarName"] = calendar["summary"] 

                if "creator" in event:
                    event["creator"] = event["creator"]["email"]

                if "dateTime" in event["start"]:
                    event["start"] = fm.format_to_localized_iso(event["start"]["dateTime"])

                if "dateTime" in event["end"]:
                    event["end"] = fm.format_to_localized_iso(event["end"]["dateTime"])

                # Convert start and end dates
                if "date" in event["start"]:
                    event["start"] = fm.format_to_localized_iso(event["start"]["date"])
                
                if "date" in event["end"]:
                    event["end"] = fm.format_to_localized_iso(event["end"]["date"])

                events.append(event)

            total_events.extend(events)

        sorted_events = sorted(total_events, key=lambda x: dt.datetime.fromisoformat(x["start"]))

        return sorted_events

    @include_get
    def get_data(self):

        time_diff = int(time.time()) - self.last_call_timestamp
        if time_diff > 60: 
            self.data = self.get_todays_agenda(self.get_calendar_names())
            self.last_call_timestamp = time.time()

        return self.data