# sensor to find new files.
# (make sure to sync files)
# for every track parse it and write it to database.
# maybe calculate in the database? https://gist.github.com/carlzulauf/1724506
# and do all that in dbt?
#
import os
from dagster import job, sensor, op, Out

from work.ops.gpx import read_gpx_file
from work.resources.gpx_writers import database_file_writer

PROCESSFOLDER=os.environ["PROCESSFOLDER"]

@op(out={"track": Out(), "metadata": Out()})
def process_file(config, filepath):
    with open(filepath) as f:
        gpx_file = f.read()
    (tracks, metadata) = read_gpx_file(gpx_file)
    tracks["name"] = metadata["name"]
    return tracks,metadata

@op(required_resource_keys={"filewriter"})
def write_track_metadata(config, metadata: dict)
    filewriter.write_metadata(metadata)

@op(required_resource_keys={"filewriter"})
def write_track(config, track:)
    filewriter.write_track(metadata)

@job(resource_defs= {"filewriter": database_file_writer})
def ingest_gpx_to_db_job():
    """Ingest new gpx track into database"""
    track, metadata = process_file()
    write_track(track)
    write_track_metadata(metadata)

@sensor(job=ingest_gpx_to_db_job)
def scan_for_new_gpx_files():
    baselocation = PROCESSFOLDER+"/Gpxrecordings"
    gpx_files = [file for file in os.listdir(baselocation) if file.endswith(".gpx")]
    filepath=os.path.join(baselocation, gpx_files[0])
    for filename in gpx_files:
        filepath = os.path.join(baselocation, filename)
        if os.path.isfile(filepath):
            yield RunRequest(
                run_key=filename,
                run_config={
                    "ops": {"process_file": {"config": {"filepath": filepath}}}
                },
            )
