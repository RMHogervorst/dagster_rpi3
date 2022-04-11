{% docs __overview__ %}
# Overview
This is the dbt project that runs all the transformations in my 'warehouse'.
Currently it has a schema openweathermap. not more



## Schemas

### openweathermap
Contains all the work for local weather.
Data comes in with the [load_current_weather_job](http://rpi3.local:3000/workspace/rpi3work@repo.py/jobs/load_current_weather).

That fills the raw_current_weather table. We never select out of the raw data,
but use the staging table stg_current_weather for further work.

{% enddocs %}
