from dagster import AssetGroup, repository

from jobs.create_tables import create_tables
from jobs.gps_to_db import scan_for_new_gpx_files
from jobs.load_current_weather import current_weather_during_day, raw_current_weather

# from assets import dbt_assets
from jobs.recepten import raw_daily_recipes, recept_2_calender
from jobs.run_dbt import dbt_assets, dbt_tag_daily, dbt_tag_weekly
from jobs.trigger_website_rebuilds import websites_retrigger_schedule

asset_group = AssetGroup(
    [], source_assets=[raw_current_weather, raw_daily_recipes]  # dbt_assets,
)


@repository
def rpi3work():
    return [
        current_weather_during_day,
        create_tables,
        websites_retrigger_schedule,
        dbt_tag_daily,
        dbt_tag_weekly,
        asset_group,
        recept_2_calender,
        scan_for_new_gpx_files,
    ]
