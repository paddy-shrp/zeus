import datetime as dt
import pytz
import pandas as pd
import utils.settings as settings

def get_timezone():
    return pytz.timezone(settings.get_settings()["timezone"])

def now():
    return dt.datetime.now(get_timezone()).isoformat()

def min_max_of_day(timestamp:dt.datetime = None):
    if timestamp == None: timestamp = dt.datetime.now()
    timeMin = dt.datetime.combine(timestamp, dt.time.min).astimezone(get_timezone()).isoformat()
    timeMax = dt.datetime.combine(timestamp, dt.time.max).astimezone(get_timezone()).isoformat()
    print(timeMax)
    return (timeMin, timeMax)

def format_to_localized_iso(datetime:str):
    convert = pd.to_datetime(datetime, format="mixed")
    if convert.tzinfo != None:
        return convert.tz_convert(get_timezone()).isoformat()
    else:
        return convert.tz_localize(get_timezone()).isoformat()