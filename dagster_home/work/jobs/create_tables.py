from dagster import job, op
from resources.connectors import postgres_connection


@op(required_resource_keys={"warehouse_credentials"})
def current_weather(context):

    with open(r"work/sql/create_table_current_weather.sql", "r") as f:
        query = f.read()
        f.close()

    conn = context.resources.warehouse_credentials
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)


@job(resource_defs={"warehouse_credentials": postgres_connection})
def create_openweathermap_tables():
    current_weather()
