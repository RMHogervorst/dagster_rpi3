from dagster import job, op
from resources.connectors import postgres_connection, postgres_connection_receptenloader


@op(required_resource_keys={"warehouse_credentials"})
def current_weather(context):
    """Create current_weather table"""
    with open(r"work/sql/create_table_current_weather.sql", "r") as f:
        query = f.read()
        f.close()

    conn = context.resources.warehouse_credentials
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)

@op(required_resource_keys={"warehouse_credentials2"})
def daily_recipes(context):
    """Only need datum and ID but to clear up mess
    later also include link and maaltijdnaam"""

    with open(r"work/sql/create_table_daily_recipes.sql", "r") as f:
        query = f.read()
        f.close()

    conn = context.resources.warehouse_credentials2
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(query)

@job(resource_defs={"warehouse_credentials": postgres_connection, "warehouse_credentials2":postgres_connection_receptenloader})
def create_tables():
    current_weather()
    daily_recipes()
