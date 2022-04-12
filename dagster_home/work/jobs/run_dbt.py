from dagster import ScheduleDefinition, job
from dagster_dbt import dbt_cli_resource, dbt_docs_generate_op
from ops.dbt import make_run_test_custom

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
    daily_run()

## Weekly
weekly_run = make_run_test_custom("tag:weekly")

@job(resource_defs={"dbt": my_dbt_resource})
def dbt_job_weekly_daily():
    weekly_run()

# schedules
dbt_tag_daily = ScheduleDefinition(job=dbt_job_tag_daily, cron_schedule="3 23 * * *")
dbt_tag_weekly = ScheduleDefinition(
    job=dbt_job_tag_weekly,
    cron_schedule="45 23 * * 0"
    # sunday (0) 23:45
    )
