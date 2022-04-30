from dagster import ScheduleDefinition, job
from dagster_dbt import dbt_cli_resource, dbt_docs_generate_op
from ops.dbt import make_run_test_custom
from dagster_dbt.asset_defs import load_assets_from_dbt_manifest
from hooks.pushover import pushover_message_on_failure
import os
import json

DBT_PROJECT_DIR="/Users/roelhogervorst/Documents/projecten/dagster_rpi3/dagster_home/work_dbt"

dbt_assets = load_assets_from_dbt_manifest(
    manifest_json=json.load(open(os.path.join(DBT_PROJECT_DIR,"target","manifest.json")))
)

my_dbt_resource = dbt_cli_resource.configured(
    {
        "project_dir": "work_dbt/",
        "profiles_dir": "work_dbt/",
    }
)




## Daily
daily_run = make_run_test_custom("tag:daily")

@job(resource_defs={"dbt": my_dbt_resource})
def dbt_job_tag_daily():
    daily_run.with_hooks({pushover_message_on_failure})()

## Weekly
weekly_run = make_run_test_custom("tag:weekly")

@job(resource_defs={"dbt": my_dbt_resource})
def dbt_job_tag_weekly():
    weekly_run.with_hooks({pushover_message_on_failure})()

# schedules
dbt_tag_daily = ScheduleDefinition(job=dbt_job_tag_daily, cron_schedule="3 23 * * *")
dbt_tag_weekly = ScheduleDefinition(
    job=dbt_job_tag_weekly,
    cron_schedule="45 23 * * 0"
    # sunday (0) 23:45
    )
