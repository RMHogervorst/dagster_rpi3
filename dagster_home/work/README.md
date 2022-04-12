# dbt project work

This is a project with the uninspiring name 'work'.
It contains
* [jobs](jobs/)
* [operators in ops](ops/)
* [resources](resources/)
* [sql files](sql/)
* a repo.py that binds them all

## Jobs
I'm using this project to trigger stuff but I'm also building data engineering
pipelines.

### Non pipeline jobs
* trigger websites (triggers netlify to rebuild my blog and notes pages), daily
* create_openweathermap_tables creates the first table for openweathermap, incidently to rebuild the table

### Pipeline jobs

Weather
* get data from openweathermap every 15 minutes (ingestion job) write to raw_current_weather
* dbt has a folder openweathermap that creates the staging view and daily values table.
