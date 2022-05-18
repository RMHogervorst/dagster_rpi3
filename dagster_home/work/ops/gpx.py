"""Turn gpx files into table.
Or in other words turn my tracks into data.
# I'm buildin on top of.
# https://github.com/JuanManuelHuerta/GPX_Analytics_with_TimeStamps/blob/main/Course_Analyzer_with_Time.ipynb
"""
from xml.etree.ElementTree import fromstring
import datetime
from typing import Dict
from copy import copy
import pandas as pd


def read_gpx_file(file) -> (pd.DataFrame, Dict[str,str]):
    track=fromstring(file)
    dict_track = dictify(track)
    ### or should I stop here and pass the dict further on?
    a='{http://www.topografix.com/GPX/1/1}'
    trackname = dict_track[a+'gpx'][a+"metadata"][0][a+"name"][0]["_text"]
    tracks = parse_tracks(dict_track[a+'gpx'][a+"trk"])
    datetimeseries = pd.to_datetime(tracks.time)
    metadata = {
    'name': trackname,
    "from_dt": datetimeseries.min().strftime('%Y-%m-%d %H:%M:%S'),
    "to_dt": datetimeseries.max().strftime('%Y-%m-%d %H:%M:%S'),
    'n_points': len(datetimeseries)
    }
    return (tracks, metadata)

# https://stackoverflow.com/questions/2148119/how-to-convert-an-xml-string-to-a-dictionary#10199714

def dictify(r,root=True):
    if root:
        return {r.tag : dictify(r, False)}
    d=copy(r.attrib)
    if r.text:
        d["_text"]=r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag]=[]
        d[x.tag].append(dictify(x,False))
    return d

def parse_tracks(tracksdict):
    """go through tracksegments.
    Don't do anything fancy with it."""
    nullvalue = [{'_text': None}]
    a='{http://www.topografix.com/GPX/1/1}'
    o = "{https://osmand.net}"
    # build lists for each type
    lat_ = []
    lon_ = []
    hdop_ = []
    time_ = []
    ele_ = []
    speed_ = []
    heading_ = []
    for segment in tracksdict[0].get(a+'trkseg'):
        for point in segment.get(a+'trkpt'):
            lat_.append(point["lat"])
            lon_.append(point["lon"])
            # deal with possible missing values
            hdop_.append(point.get(a+"hdop", nullvalue)[0]["_text"])
            time_.append(point.get(a+"time", nullvalue)[0]["_text"])
            ele_.append(point.get(a+"ele", nullvalue)[0]["_text"])
            speed_.append(point.get(a+"extensions", '{https://osmand.net}speed')[0].get(o+"speed",nullvalue)[0]["_text"])
            heading_.append(point.get(a+"extensions", '{https://osmand.net}heading')[0].get(o+"heading",nullvalue)[0]["_text"])
    # stop
    result = pd.DataFrame({
        "lat" : lat_,
         "lon": lon_,
         "hdop": hdop_,
         "time":time_,
         "ele": ele_,
         "speed":speed_,
         "heading":heading_
    })
    return result
