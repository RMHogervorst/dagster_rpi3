import datetime
import zoneinfo

import pytest

from work.ops.gcalendar import (
    create_event_dict,
    insert_event,
    parse_events,
    read_calendar,
)


def test_create_event_dict():
    tz = zoneinfo.ZoneInfo("Europe/Amsterdam")
    start = datetime.datetime(2020, 5, 17, 14, 1, 0, 0, tz)
    end = datetime.datetime(2020, 5, 17, 15, 1, 0, 0, tz)
    bare_minimum = create_event_dict(start, end)
    assert bare_minimum["start"]["dateTime"] == "2020-05-17T14:01:00+02:00"
    assert bare_minimum["end"]["dateTime"] == "2020-05-17T15:01:00+02:00"
    assert bare_minimum["status"] == "confirmed"
    assert bare_minimum["visibility"] == "default"
    assert bare_minimum["transparency"] == "transparent"


def test_create_event_dict_fails_on_missing_tz():
    # test if it raises an error on missing timezone info.
    start = datetime.datetime(2020, 5, 17, 14, 1, 0, 0)
    end = datetime.datetime(2020, 5, 17, 15, 1, 0, 0)
    with pytest.raises(ValueError):
        bare_minimum = create_event_dict(start, end)


def test_create_event_dict_create_title():
    tz = zoneinfo.ZoneInfo("Europe/Amsterdam")
    start = datetime.datetime(2020, 5, 17, 14, 1, 0, 0, tz)
    end = datetime.datetime(2020, 5, 17, 15, 1, 0, 0, tz)
    event_dict = create_event_dict(start, end, "A nice title", "a cool description")
    assert event_dict["summary"] == "A nice title"
    assert event_dict["description"] == "a cool description"


# def test_insert_event():
#     """This works, but creates an actual event, so that is annoying"""
#     tz=zoneinfo.ZoneInfo('Europe/Amsterdam')
#     start = datetime.datetime(2020, 5, 17, 14,1,0,0,tz)
#     end = datetime.datetime(2020, 5, 17, 15,1,0,0,tz)
#     event_dict = create_event_dict(start, end,"A nice title", "a cool description")
#     cal_id="447883an888q1ldagsqe9pj7ts@group.calendar.google.com"
#     result= insert_event(cal_id, event_dict)
#     assert result["description"] == "a cool description"
#     assert result["end"]["dateTime"] == "2020-05-17T15:01:00+02:00"


def test_parse_events():
    typical_event = {
        "kind": "calendar#event",
        "etag": '"3302606516904000"',
        "id": "kg7thrpitiveo6c3imt4buc78s",
        "status": "confirmed",
        "htmlLink": "https://www.google.com/calendar/event?eid=superlongid",
        "created": "2022-04-30T07:20:58.000Z",
        "updated": "2022-04-30T07:20:58.452Z",
        "summary": "A summary",
        "description": "a description",
        "creator": {"email": "username@nicename.iam.gserviceaccount.com"},
        "organizer": {
            "email": "randomdigits@group.calendar.google.com",
            "displayName": "Recepten",
            "self": True,
        },
        "start": {"dateTime": "2022-04-30T18:30:00+02:00", "timeZone": "UTC"},
        "end": {"dateTime": "2022-04-30T19:30:00+02:00", "timeZone": "UTC"},
        "transparency": "transparent",
        "iCalUID": "otherrandomdigits@google.com",
        "sequence": 0,
        "reminders": {"useDefault": True},
        "eventType": "default",
    }
    result = parse_events(typical_event)
    expected_keys = [
        "start",
        "end",
        "status",
        "created",
        "updated",
        "organizer",
        "creator",
        "summary",
        "description",
        "location",
    ]
    keys = result.keys()
    for expected in expected_keys:
        assert expected in keys
    assert result["location"] is None


# def test_read_calendar():
#     """This one reads all the calendar events so it's non deterministic"""
#     read_calendar(calendar_id="447883an888q1ldagsqe9pj7ts@group.calendar.google.com")


def test_read_calendar_expect_empty_calendar():
    """In the future everyone will be famous, but also empty"""
    tz = zoneinfo.ZoneInfo("Europe/Amsterdam")
    start = datetime.datetime(2030, 1, 17, 14, 1, 0, 0, tz)
    events = read_calendar(
        calendar_id="447883an888q1ldagsqe9pj7ts@group.calendar.google.com",
        from_date=start,
    )
    assert len(events) == 0
