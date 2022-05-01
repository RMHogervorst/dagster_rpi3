import datetime
import os
from typing import Dict

from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def read_calendar(calendar_id: str,from_date=None, to_date=None) -> Dict:
    """Get dictionary of max 500 events in specified calendar, in specified date range"""
    service = connect_to_gcalender()
    _from_date = date_to_timestamp(from_date)
    _to_date = date_to_timestamp(to_date)
    events_result = service.events().list(calendarId=calendar_id, timeMin=_from_date,
        timeMax=_to_date,
                                              maxResults=500, singleEvents=True,
                                              orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return {}
    parsed_events = []
    for event in events:
        parsed_events.append(parse_events(event))
    return parsed_events

def parse_events(event:Dict)-> Dict:
    dict = { # these are in every event
        "start": event["start"]["dateTime"],
        "end": event["end"]["dateTime"],
        "status": event["status"],
        "created": event["created"],
        "updated": event["updated"],
        "organizer": event["organizer"]["email"],
        "creator": event["creator"]["email"],
        # these are not
        "summary": event.get("summary",None),
        "description": event.get("description",None),
        "location": event.get("location",None),
    }
    return dict

def date_to_timestamp(datevalue):
    result = None
    if datevalue is not None:
        if datevalue.tzinfo == None:
            raise ValueError(f"{datevalue} needs timezone info")
        result = datevalue.isoformat(sep="T", timespec="seconds")
    return result

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
