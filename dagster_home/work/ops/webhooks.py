import os

import requests
from dagster import op
from dotenv import load_dotenv


@op(config_schema={"netlifykey": str})
def trigger_netlify_hook(context):
    """Netlify can be triggered to build with a simple empty post request
    to the right adress"""
    load_dotenv()
    key = context.op_config["netlifykey"]
    value = os.environ[key]
    context.log.info(f"using key {key}")
    url = f"https://api.netlify.com/build_hooks/{value}"
    r = requests.post(url)
    context.log.info(f"request result was {r.status_code}")
