from work.ops.gcalendar import _create_event_dict, insert_event
import zoneinfo

import datetime

import pytest

def test__create_event_dict():
    tz=zoneinfo.ZoneInfo('Europe/Amsterdam')
    start = datetime.datetime(2020, 5, 17, 14,1,0,0,tz)
    end = datetime.datetime(2020, 5, 17, 15,1,0,0,tz)
    bare_minimum = _create_event_dict(start, end)
    assert bare_minimum["start"]["dateTime"]=="2020-05-17T14:01:00+02:00"
    assert bare_minimum["end"]["dateTime"]=="2020-05-17T15:01:00+02:00"
    assert bare_minimum["status"]=="confirmed"
    assert bare_minimum["visibility"]=="default"
    assert bare_minimum["transparency"]=="transparent"

def test__create_event_dict_fails_on_missing_tz():
    # test if it raises an error on missing timezone info.
    start = datetime.datetime(2020, 5, 17, 14,1,0,0)
    end = datetime.datetime(2020, 5, 17, 15,1,0,0)
    with pytest.raises(ValueError):
        bare_minimum = _create_event_dict(start, end)

def test__create_event_dict_create_title():
    tz=zoneinfo.ZoneInfo('Europe/Amsterdam')
    start = datetime.datetime(2020, 5, 17, 14,1,0,0,tz)
    end = datetime.datetime(2020, 5, 17, 15,1,0,0,tz)
    event_dict = _create_event_dict(start, end,"A nice title", "a cool description")
    assert event_dict["title"] == "A nice title"
    assert event_dict["description"] == "a cool description"

# def test_insert_event():
#     """This works, but creates an actual event, so that is annoying"""
#     tz=zoneinfo.ZoneInfo('Europe/Amsterdam')
#     start = datetime.datetime(2020, 5, 17, 14,1,0,0,tz)
#     end = datetime.datetime(2020, 5, 17, 15,1,0,0,tz)
#     event_dict = _create_event_dict(start, end,"A nice title", "a cool description")
#     cal_id="447883an888q1ldagsqe9pj7ts@group.calendar.google.com"
#     result= insert_event(cal_id, event_dict)
#     assert result["description"] == "a cool description"
#     assert result["end"]["dateTime"] == "2020-05-17T15:01:00+02:00"
