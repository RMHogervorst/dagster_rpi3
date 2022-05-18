import os

import psycopg2
from dagster import resource
from dotenv import load_dotenv
import pandas as pd

SCHEMA = "gps"
NAME_METADATATABLE="raw_track_metadata"
NAME_TRACKTABLE="raw_tracks"


class DatabaseFileWriter:
    """write to database"""
    def __init__(self):
        load_dotenv()
        self.conn = psycopg2.connect(
            database=os.environ["PG_DATABASE"],
            user=os.environ["gpxuser"],
            password=os.environ["gpxpassword"],
            host=os.environ["PG_HOST"],
            port=os.environ["PG_PORT"],
        )
        self.schema = SCHEMA
        self.metadatatablename=NAME_METADATATABLE
        self.tracktablename=NAME_TRACKTABLE
    def write_metadata(self,metadatadict):
        df = pd.DataFrame(metadatadict,index=[0])
        df.to_sql(
            self.metadatatablename,
            con=self.conn,
            schema=self.schema,
            if_exists='append',
            index=False)
    def write_track(self, trackdataframe)
        trackdataframe.to_sql(
            self.tracktablename,
            con=self.conn,
            schema=self.schema,
            if_exists='append',
            index=False)

@resource
def database_file_writer(init_context):
    return DatabaseFileWriter()

class CsvFileWriter:
    """identical to DatabaseFileWriter but with csv output"""
    def __init__(self, filelocation = "tmp/"):
        self.filelocation = filelocation
        self.schema = SCHEMA
        os.makedirs(os.path.join(self.filelocation, self.schema), exist_ok =True)
        self.metadatatablename=NAME_METADATATABLE
        self.tracktablename=NAME_TRACKTABLE
    def write_metadata(self,metadatadict):
        df = pd.DataFrame(metadatadict,index=[0])
        path = path=os.path.join(self.filelocation,self.schema,self.metadatatablename)+".csv"
        df.to_csv(path, mode='a',index=False)
    def write_track(self, trackdataframe):
        path = os.path.join(self.filelocation,self.schema,self.tracktablename)+".csv"
        trackdataframe.to_csv(path, mode='a',index=False)

@resource
def csv_file_writer(init_context):
    return CsvFileWriter()

csv_file_writer = CsvFileWriter()
