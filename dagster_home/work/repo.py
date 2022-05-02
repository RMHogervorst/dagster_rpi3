from dagster import repository, AssetGroup
from jobs.create_tables import create_tables
from jobs.load_current_weather import current_weather_during_day, raw_current_weather
from jobs.run_dbt import dbt_tag_daily, dbt_tag_weekly, dbt_assets
from jobs.trigger_website_rebuilds import websites_retrigger_schedule
#from assets import dbt_assets
from jobs.recepten import recept_2_calender, raw_daily_recipes


asset_group = AssetGroup(
    [],#dbt_assets,
    source_assets=[raw_current_weather, raw_daily_recipes]
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
    ]
