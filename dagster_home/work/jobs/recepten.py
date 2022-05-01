import pandas as pd
from dagster import op, job, Out, AssetMaterialization
from ops.gsheets import get_sheet_data
from ops.gcalendar import insert_event, create_event_dict, read_calendar
from dagster_pandera import pandera_schema_to_dagster_type
import pandera as pa
from pandera.typing import Series
import zoneinfo

import datetime


class Recipes(pa.SchemaModel):
    """Recipes retrieved from google sheet, modified by this operator."""

    weekdag: Series[str] = pa.Field(description="day of the week, in dutch")
    datum: Series[str] = pa.Field(description="Date in isoformat %Y-%m-%d")
    ID: Series[str] = pa.Field(description="ID that refers back to masterlist")
    maaltijdnaam: Series[str] = pa.Field(
        description="ID that refers back to masterlist", nullable=True
    )
    omschrijving: Series[str] = pa.Field(
        description="Derived field from masterlist: summary of meal", nullable=True
    )
    energie: Series[str] = pa.Field(
        description="Derived field from masterlist: energy in kilocalories",
        nullable=True,
    )
    eiwitten: Series[str] = pa.Field(
        description="Derived field from masterlist: protein", nullable=True
    )
    vet: Series[str] = pa.Field(
        description="Derived field from masterlist: fat", nullable=True
    )
    koolhydraten: Series[str] = pa.Field(
        description="Derived field from masterlist: carbohydrates", nullable=True
    )
    link: Series[str] = pa.Field(
        description="Derived field from masterlist: URL to recipe", nullable=True
    )
    type: Series[str] = pa.Field(
        description="Derived field from masterlist: category of meal (pasta, soup, rice, etc.)",
        nullable=True,
    )


@op(out=Out(dagster_type=pandera_schema_to_dagster_type(Recipes)))
def cleanup_recipes(df: pd.DataFrame) -> pd.DataFrame:
    """A helper operator to clean up this sheet.
    The get_sheet_data operator is generic and doesn't care
    about what it gets. But I know the design of this sheet and so
    I can do some cleaning.
    Because google sheets can change I think it is wise to validate
    the schema after modification with pandera."""
    # first row in this case is names.
    df.columns = df.iloc[0]
    # drop the first row (is already the header).
    df = df.iloc[1:, :]
    # drop rows without a date filled in (it is not NA (missing) but empty)
    df = df[df.datum != ""]
    # drop rows without ID
    df = df[df.ID != ""]
    # set the datum row to dates -type?
    # TODO: guard against changes in the past
    # TODO: guard against changes more than 14 days in the future
    return df


@op(config_schema={"calendar_id": str})
def remove_days_already_filled(context, df: pd.DataFrame) -> pd.DataFrame:
    """Filter days that are already in the calendar"""
    # get events
    tz = zoneinfo.ZoneInfo("Europe/Amsterdam")
    df["date_parsed"] = pd.to_datetime(df["datum"])

    max = datetime.datetime.combine(
        df["date_parsed"].max(),
        datetime.time(22, 30, tzinfo=tz)
        )
    min = datetime.datetime.combine(
        df["date_parsed"].min(),
        datetime.time(8, 30, tzinfo=tz)
        )
    events = read_calendar(calendar_id=context.op_config["calendar_id"],
        from_date=min, to_date=max)
    # filter out rows that already have a result.
    datums = [event["start"][0:10] for event in events]
    df = df[~df.datum.isin(datums)]
    return df


@op(config_schema={"calendar_id": str})
def insert_recipes_into_gcal(context, df: pd.DataFrame) -> None:
    """Parse dataframe and send every recipe as event to google calendar"""
    # take 'datum' and make that into start and end datetime
    # fix time at 18:30-19:30
    tz = zoneinfo.ZoneInfo("Europe/Amsterdam")
    #
    for row in df.itertuples(index=False):
        context.log.info(f"writing {row.datum}")
        date_ = datetime.date.fromisoformat(row.datum)
        startdatetime = datetime.datetime.combine(
            date_,
            datetime.time(18, 30, tzinfo=tz),
        )
        enddatetime = datetime.datetime.combine(
            date_,
            datetime.time(19, 30, tzinfo=tz),
        )
        dict = create_event_dict(
            startdatetime=startdatetime,
            enddatetime=enddatetime,
            title=row.maaltijdnaam,
            description=f"{row.omschrijving}, type: {row.type}, link {row.link} ",
        )
        insert_event(calendar_id=context.op_config["calendar_id"], event_dict=dict)


@job(
    config={
        "ops": {
            "get_sheet_data": {
                "config": {
                    "sheetid": "1bTFbQTY6869y52kyr48DlcHsN7FnUWyxBfuL5XLVRWI",
                    "sheetnumber": 0,
                }
            },
            "remove_days_already_filled": {
                "config": {
                    "calendar_id": "447883an888q1ldagsqe9pj7ts@group.calendar.google.com"
                }
            },
            "insert_recipes_into_gcal": {
                "config": {
                    "calendar_id": "447883an888q1ldagsqe9pj7ts@group.calendar.google.com"
                }
            },
        }
    }
)
def recept_2_calender():
    """Read recepten from google sheet and write to calender"""
    future_recipes_df = get_sheet_data()
    cleaned_recipes = cleanup_recipes(future_recipes_df)
    filtered_recipes = remove_days_already_filled(cleaned_recipes)
    insert_recipes_into_gcal(filtered_recipes)
    # or get the ones for a week
    # check if these dates have recipes already?
    # filter dates
    # write to calender
    # send notification on failure?
    # remove from sheet 0?
