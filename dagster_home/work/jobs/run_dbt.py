from dagster import ScheduleDefinition, job
from dagster_dbt import dbt_cli_resource, dbt_docs_generate_op
from ops.dbt import make_run_test_custom

my_dbt_resource = dbt_cli_resource.configured(
    {
        "project_dir": "work_dbt/",
        "profiles_dir": "work_dbt/",
    }
)

daily_run = make_run_test_custom("tag:daily")


@job(resource_defs={"dbt": my_dbt_resource})
def dbt_job_tag_daily():
    daily_run()


# graph of run, test, document
dbt_tag_daily = ScheduleDefinition(job=dbt_job_tag_daily, cron_schedule="3 23 * * *")
