from dagster import ScheduleDefinition, job
from ops.webhooks import trigger_netlify_hook

config = {
    "ops": {
        "blog": {"config": {"netlifykey": "NETLIFYBLOG"}},
        "notes": {"config": {"netlifykey": "NETLIFYNOTES"}},
    }
}


@job(config=config, description="Trigger netlify to rebuild websites daily.")
def trigger_websites():
    jobs = [
    trigger_netlify_hook.alias("blog")(),
    trigger_netlify_hook.alias("notes")()
    ]


websites_retrigger_schedule = ScheduleDefinition(
    job=trigger_websites, cron_schedule="13 8 * * *"  # 0813 everyday
)
