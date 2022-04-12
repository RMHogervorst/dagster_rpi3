from dagster import repository
from jobs.create_tables import create_openweathermap_tables
from jobs.load_current_weather import current_weather_during_day
from jobs.run_dbt import dbt_tag_daily, dbt_tag_weekly
from jobs.trigger_website_rebuilds import websites_retrigger_schedule


@repository
def rpi3work():
    return [
        current_weather_during_day,
        create_openweathermap_tables,
        websites_retrigger_schedule,
        dbt_tag_daily,
        dbt_tag_weekly
    ]
