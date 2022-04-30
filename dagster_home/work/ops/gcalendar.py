import datetime
import os

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def insert_event(calendar_id, event_dict):
    service = connect_to_gcalender()
    event = service.events().insert(calendarId=calendar_id, body=event_dict).execute()
    return event


def create_event_dict(
    startdatetime,
    enddatetime,
    title=None,
    description=None,
    location=None,
    status="confirmed",
    visibility="default",
    transparency="transparent",
):
    """check for datetime, timezone, end after start"""
    if startdatetime.tzinfo == None or enddatetime.tzinfo == None:
        raise ValueError("start and end date need to have timezone info")

    startdatestamp = startdatetime.isoformat(sep="T", timespec="seconds")
    enddatestamp = enddatetime.isoformat(sep="T", timespec="seconds")
    # TODO: check transparancy, visibility and status against what is allowed.
    # fill in everything we already know.
    event_dict = {
        "start": {"dateTime": startdatestamp},
        "end": {"dateTime": enddatestamp},
        "transparency": transparency,
        "visibility": visibility,
        "status": status,
    }
    if title is not None:
        event_dict["summary"] = title

    if description is not None:
        event_dict["description"] = description

    if location is not None:
        event_dict["location"] = location

    return event_dict


# tz = pytz.timezone('Europe/Amsterdam')
# year, month, day, hour, minute, second, microsecond, tzone
# test data will be datetime.datetime(2020, 5, 17, 14,1,0,0,tz)
# test if it raises an error on missing timezone info.
# test if location is filled in.


def connect_to_gcalender():
    """Use service account to get credentials and
    connect to google calendar."""
    load_dotenv()
    keylocation = os.environ["gcp_key_loc"]
    credentials = service_account.Credentials.from_service_account_file(
        keylocation, scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=credentials)
    return service
