import json
import os
from datetime import datetime
from typing import Dict

import requests
from dagster import ScheduleDefinition, job, op
from resources.connectors import openweathermapapikey, postgres_connection


@op(required_resource_keys={"openweathermapapikey"})
def retrieve_current_weather(context) -> Dict:
    key = context.resources.openweathermapapikey
    lat = os.environ.get("GEOlat")
    lon = os.environ.get("GEOlon")  # could default to NSA headquarters? 39.109 -76.77
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric&lang=nl"
    response_API = requests.get(url)
    context.log.info(f"request result was {response_API.status_code}")
    data = json.loads(response_API.text)
    context.log.info(f"retrieved result for {data['name']}")
    return data


@op(required_resource_keys={"warehouse_credentials"})
def write_current_weather_to_db(context, data: Dict) -> None:
    result = payload_to_dict(data)
    # connection
    conn = context.resources.warehouse_credentials
    conn.autocommit = True
    cursor = conn.cursor()
    # TODO: this is sql injection sensitive!
    sqlquery = """INSERT INTO openweathermap.raw_current_weather ({}
    ) VALUES ({});""".format(
        ", ".join(result.keys()),
        ", ".join(["'" + item + "'" for item in result.values()]),
    )
    context.log.debug(sqlquery)
    cursor.execute(sqlquery)
    #


def payload_to_dict(data):
    return {
        "created_at": unix_to_timestamp(data["dt"]),
        # Time of data calculation, unix, UTC
        "place": data["name"],
        "lat": str(data["coord"]["lat"]),
        "lon": str(data["coord"]["lon"]),
        "sunrise_at": unix_to_timestamp(data["sys"]["sunrise"]),
        "sunset_at": unix_to_timestamp(data["sys"]["sunset"]),
        "temp_celcius": str(data["main"]["temp"]),
        "temp_feels_like_celcius": str(data["main"]["feels_like"]),
        "temp_celcius_min": str(
            data["main"]["temp_min"]
        ),
        "temp_celcius_max": str(data["main"]["temp_max"]),
        "humidity_percent": str(data["main"]["humidity"]),
        "sea_level_pressure_hpa": str(data["main"]["pressure"]),
        "wind_speed_ms": str(data["wind"]["speed"]),
        "wind_dir_degree": str(data["wind"]["deg"]),
        "cloudiness_percent": str(data["clouds"]["all"]),
    }


def unix_to_timestamp(value):
    return f'{datetime.fromtimestamp(int(value)).strftime("%Y-%m-%d %H:%M:%S UTC")}'


@job(
    resource_defs={
        "warehouse_credentials": postgres_connection,
        "openweathermapapikey": openweathermapapikey,
    },
    description="""Fill the table raw_current_weather in
    schema openweathermap with weather values"""
)
def load_current_weather():
    write_current_weather_to_db(retrieve_current_weather())


current_weather_during_day = ScheduleDefinition(
    job=load_current_weather,
    cron_schedule="*/15 6-22 * * *"
    # every 15 minutes from 6 through 22.
)
