from dagster import build_op_context

from work.ops.webhooks import trigger_netlify_hook

def test_trigger_netlify_hook():
    context = build_op_context(config = {"netlifykey":"blabla"}
        )
    trigger_netlify_hook(context) is None
