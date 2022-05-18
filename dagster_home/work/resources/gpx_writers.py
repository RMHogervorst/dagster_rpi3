import os

import pandas as pd
from sqlalchemy import create_engine
import urllib.parse
from dagster import resource
from dotenv import load_dotenv

SCHEMA = "gps"
NAME_METADATATABLE = "raw_track_metadata"
NAME_TRACKTABLE = "raw_tracks"

def q(stuff):
    return urllib.parse.quote_plus(stuff)

class DatabaseFileWriter:
    """write to database"""

    def __init__(self):
        load_dotenv()
        database=os.environ["PG_DATABASE"]
        user=os.environ["gpxuser"]
        password=os.environ["gpxpassword"]
        host=os.environ["PG_HOST"]
        port=os.environ["PG_PORT"]
        #username:password@host:port/database
        conn_string = f"postgresql://{q(user)}:{q(password)}@{q(host)}:{q(port)}/{q(database)}"
        self.conn = create_engine(conn_string)
        self.schema = SCHEMA
        self.metadatatablename = NAME_METADATATABLE
        self.tracktablename = NAME_TRACKTABLE

    def write_metadata(self, metadatadict):
        df = pd.DataFrame(metadatadict, index=[0])
        df.to_sql(
            self.metadatatablename,
            con=self.conn,
            schema=self.schema,
            if_exists="append",
            index=False,
        )

    def write_track(self, trackdataframe):
        trackdataframe.to_sql(
            self.tracktablename,
            con=self.conn,
            schema=self.schema,
            if_exists="append",
            index=False,
        )


@resource
def database_file_writer(init_context):
    return DatabaseFileWriter()


class CsvFileWriter:
    """identical to DatabaseFileWriter but with csv output"""

    def __init__(self, filelocation="tmp/"):
        self.filelocation = filelocation
        self.schema = SCHEMA
        os.makedirs(os.path.join(self.filelocation, self.schema), exist_ok=True)
        self.metadatatablename = NAME_METADATATABLE
        self.tracktablename = NAME_TRACKTABLE

    def write_metadata(self, metadatadict):
        df = pd.DataFrame(metadatadict, index=[0])
        path = path = (
            os.path.join(self.filelocation, self.schema, self.metadatatablename)
            + ".csv"
        )
        df.to_csv(path, mode="a", index=False,header = False)

    def write_track(self, trackdataframe):
        path = (
            os.path.join(self.filelocation, self.schema, self.tracktablename) + ".csv"
        )
        trackdataframe.to_csv(path, mode="a", index=False,header = False)


@resource
def csv_file_writer(init_context):
    return CsvFileWriter()
