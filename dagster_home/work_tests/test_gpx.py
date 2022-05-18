# gpx
from xml.etree.ElementTree import fromstring

from work.ops.gpx import dictify, parse_tracks

import pandas as pd

gpx_example = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<gpx version="1.1" creator="OsmAnd 4.0.7" xmlns="http://www.topografix.com/GPX/1/1" xmlns:osmand="https://osmand.net" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <name>2021-01-01_10-39example</name>
  </metadata>
  <trk>
    <trkseg>
      <trkpt lat="48.9574851" lon="5.8666369">
        <ele>256.3</ele>
        <time>2021-01-01T08:39:26Z</time>
        <hdop>8</hdop>
        <extensions>
          <osmand:speed>0.3</osmand:speed>
        </extensions>
      </trkpt>
      <trkpt lat="48.9576003" lon="5.8668417">
        <ele>255.7</ele>
        <time>2021-01-01T08:39:42Z</time>
        <hdop>6.3</hdop>
        <extensions>
          <osmand:speed>0.3</osmand:speed>
        </extensions>
      </trkpt>
      <trkpt lat="48.9577591" lon="5.8670052">
        <ele>255.6</ele>
        <time>2021-01-01T08:39:58Z</time>
        <hdop>4.3</hdop>
        <extensions>
          <osmand:speed>0.3</osmand:speed>
        </extensions>
      </trkpt>
    </trkseg>
  </trk>
</gpx>"""

def test_dictify():
    result = dictify(fromstring(gpx_example))
    for item in ["version", 'creator', '{http://www.topografix.com/GPX/1/1}metadata', '{http://www.topografix.com/GPX/1/1}trk']:
        assert item in result['{http://www.topografix.com/GPX/1/1}gpx'].keys()


def test_parse_tracks():
    a='{http://www.topografix.com/GPX/1/1}'
    input = dictify(fromstring(gpx_example))[a+'gpx'][a+"trk"]
    tracks = parse_tracks(input)

    expected= pd.DataFrame({
    "lat" : [48.9574851, 48.9576003, 48.9577591],
     "lon": [5.8666369,5.8668417,5.8670052],
     "hdop": [8, 6.3,4.3],
     "time":["2021-01-01T08:39:26Z","2021-01-01T08:39:42Z","2021-01-01T08:39:58Z"],
     "ele": [256.3,255.7,255.6],
     "speed":[0.3,0.3,0.3],
     "heading": [None] *3
    })
    assert tracks["lat"] == expected["lat"]
    assert tracks["lon"] == expected["lon"]
    
