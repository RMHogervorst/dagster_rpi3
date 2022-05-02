import os

import psycopg2
from dagster import resource
from dotenv import load_dotenv


@resource
def openweathermapapikey():
    load_dotenv()
    return os.environ.get("openweathermapapikey")


@resource
def postgres_connection():
    """Create a postgres connection to the warehouse"""
    load_dotenv()
    conn = psycopg2.connect(
        database=os.environ["PG_DATABASE"],
        user=os.environ["user"],
        password=os.environ["password"],
        host=os.environ["PG_HOST"],
        port=os.environ["PG_PORT"],
    )
    return conn

@resource
def postgres_connection_receptenloader():
    """Create a postgres connection to the warehouse"""
    load_dotenv()
    conn = psycopg2.connect(
        database=os.environ["PG_DATABASE"],
        user=os.environ["recepten_user"],
        password=os.environ["recepten_password"],
        host=os.environ["PG_HOST"],
        port=os.environ["PG_PORT"],
    )
    return conn
