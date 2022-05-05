A dbt project, can be run from dbt and with dagster with the dbt_operator.
For some reason I really have to activate all the .env variables before dbt picks
it up.

run dbt like this: dbt docs serve  --profiles-dir . --models tag:daily
