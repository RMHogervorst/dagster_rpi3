# sensor to find new files.
# (make sure to sync files)
# for every track parse it and write it to database.
# maybe calculate in the database? https://gist.github.com/carlzulauf/1724506
# and do all that in dbt?
#
import os
from typing import Dict

from dagster import Out, job, op, sensor
from dotenv import load_dotenv

from ops.gpx import read_gpx_file
from resources.gpx_writers import database_file_writer


@op(out={"track": Out(), "metadata": Out()})
def process_file(filepath: str):
    with open(filepath) as f:
        gpx_file = f.read()
    (tracks, metadata) = read_gpx_file(gpx_file)
    tracks["name"] = metadata["name"]
    return tracks, metadata


@op(required_resource_keys={"filewriter"})
def write_track_metadata(context, metadata: Dict):
    context.resources.filewriter.write_metadata(metadata)


@op(required_resource_keys={"filewriter"})
def write_track(context, track):
    context.resources.filewriter.write_track(track)


@job(resource_defs={"filewriter": database_file_writer})
def ingest_gpx_to_db_job():
    """Ingest new gpx track into database"""
    track, metadata = process_file()
    write_track(track)
    write_track_metadata(metadata)


@sensor(job=ingest_gpx_to_db_job)
def scan_for_new_gpx_files():
    load_dotenv()  # stupid hack
    PROCESSFOLDER = os.environ["PROCESSFOLDER"]

    baselocation = PROCESSFOLDER + "/Gpxrecordings"
    gpx_files = [file for file in os.listdir(baselocation) if file.endswith(".gpx")]
    filepath = os.path.join(baselocation, gpx_files[0])
    for filename in gpx_files:
        filepath = os.path.join(baselocation, filename)
        if os.path.isfile(filepath):
            yield RunRequest(
                run_key=filename,
                run_config={
                    "ops": {"process_file": {"config": {"filepath": str(filepath)}}}
                },
            )
