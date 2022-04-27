import os
import requests
from dagster import HookContext, failure_hook, success_hook
from dotenv import load_dotenv

@success_hook()
def pushover_message_on_success(context: HookContext):
    message = f"Op {context.op.name} in job {context.job_name} finished successfully"
    send_pushover_message(message=message, priority=-1, title="dagster success")


@failure_hook()
def pushover_message_on_failure(context: HookContext):
    message = f"Op {context.op.name} failed in job {context.job_name} "
    send_pushover_message(message=message, priority=0, title="dagster failure")

def send_pushover_message(message:str, priority: int = 0, title=None):
    """
    (https://pushover.net/api)
    POST an HTTPS request to https://api.pushover.net/1/messages.json with the following parameters:

        token - your application's API token (required)
        user - your user/group key (or that of your target user), viewable when logged into our dashboard; often referred to as USER_KEY in our documentation and code examples (required)
        message - your message (required)

    Some optional parameters may also be included:

        attachment - an image attachment to send with the message (documentation)
        device - the name of one of your devices to send just to that device instead of all devices (documentation)
        html - set to 1 to enable HTML parsing (documentation)
        priority - a value of -2, -1, 0 (default), 1, or 2 (documentation)
        sound - the name of a supported sound to override your default sound choice (documentation)
        timestamp - a Unix timestamp of a time to display instead of when our API received it (documentation)
        title - your message's title, otherwise your app's name is used
        url - a supplementary URL to show with your message (documentation)
        url_title - a title for the URL specified as the url parameter, otherwise just the URL is shown (documentation)
    """
    load_dotenv()
    APP_TOKEN = os.environ["PUSHOVER_APP_TOKEN"]
    USER_KEY = os.environ["PUSHOVER_USER_KEY"]
    if priority not in [-2,-1,0,1,2]:
        raise ValueError('priority must be in -2,-1,0,1,2')
    data = {
      "token": APP_TOKEN,
      "user": USER_KEY,
      "message": message,
    }

    if title is not None:
        data["title"]= title

    r = requests.post("https://api.pushover.net/1/messages.json", data =data)
    return r.text
