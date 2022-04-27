"""Operators for reading and writing to google sheets.
Sheets are not databases but they are remarkably easy to use!"""

import os

import gspread
import pandas as pd
from dagster import op
from dotenv import load_dotenv

@op(config_schema={"sheetid": str, "sheetnumber": int})
def get_sheet_data(context) -> pd.DataFrame:
    """download all rows from a sheet
    filelocation is defined with an env variable
    return a dataframe with results"""
    load_dotenv()
    keylocation = os.environ["gcp_key_loc"]
    gc = auth_gdrive_service_account(filename=keylocation)
    sheetid = context.op_config["sheetid"]
    sheetnumber = context.op_config["sheetnumber"]
    values = get_all_values_from_sheet(gc, sheetid, sheetnumber)
    # TODO: use schema validation here with pandera or something?
    # TODO: define as asset?
    return pd.DataFrame(values)


def auth_gdrive_service_account(filename):
    gc = gspread.service_account(filename=filename)
    return gc


def get_all_values_from_sheet(account, sheetid, sheetnumber):
    sh = account.open_by_key(sheetid)
    worksheet = sh.get_worksheet(sheetnumber)
    return worksheet.get_all_values()
