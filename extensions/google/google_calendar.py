import datetime as dt
import pytz
from utils.decorators import *
from utils.objects.extension import Extension

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import extensions.google.google_init as g_init

DT_TIME_ZONE = pytz.timezone("Europe/Berlin")

class GoogleCalendar(Extension):
    def __init__(self):

        self.credentials = g_init.init_google_api()

        try: 
            self.service = build("calendar", "v3", credentials=self.credentials)
        except HttpError as error:
            self.service = None
            print(f"An error occured: {error}")

    @include_get
    async def get_todays_agenda(self, calendar_names):

        timeMin = dt.datetime.combine(dt.datetime.now(), dt.time.min, DT_TIME_ZONE).isoformat()
        timeMax = dt.datetime.combine(dt.datetime.now(), dt.time.max, DT_TIME_ZONE).isoformat()
        events_today = self.get_events(calendar_names, timeMin, timeMax)
        
        return events_today

    @include_get
    async def get_calendars(self):
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
        
    @include_get
    async def get_events(self, calendar_names=["primary"], timeMin=None, timeMax=None):
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
                 "timeMin": dt.datetime.now(DT_TIME_ZONE).isoformat(),
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
                    event["start"] = dt.datetime.fromisoformat(event["start"]["dateTime"]).astimezone(DT_TIME_ZONE).isoformat()

                if "dateTime" in event["end"]:
                    event["end"] = dt.datetime.fromisoformat(event["end"]["dateTime"]).astimezone(DT_TIME_ZONE).isoformat()

                # Convert start and end dates
                if "date" in event["start"]:
                    event["start"] = dt.datetime.strptime(event["start"]["date"], "%Y-%m-%d").astimezone(DT_TIME_ZONE).isoformat()
                    pass
                
                if "date" in event["end"]:
                    event["end"] = dt.datetime.strptime(event["end"]["date"], "%Y-%m-%d").astimezone(DT_TIME_ZONE).isoformat()
                    pass

                events.append(event)
        
            total_events.extend(events)

        sorted_events = sorted(total_events, key=lambda x: dt.datetime.fromisoformat(x["start"]))

        return sorted_events

    @include_get
    async def get_data(self):
        return {}