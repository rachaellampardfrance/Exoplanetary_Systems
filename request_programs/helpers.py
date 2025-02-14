"""helper fucntions for data gathering/saving"""
from io import StringIO
import re
from database_helpers import get_last_updated
from pyfiglet import Figlet

from astroquery.utils.tap.core import TapPlus
import pandas as pd

# PATH = "directory"
FG = Figlet(font='standard')
# FG = Figlet(font='cybermedium')


def render_figlet(message: str) -> None:
    print(FG.renderText(message))


def get_user_confirm(message: str) -> bool:
    """take in message for user input and confirmation
    
    :returns: True on confirm, False on not confirm
    """
    answer = input(message).lower()

    while True:
        if answer in ["y", "yes"]:
            return True
        if answer in ["n", "no"]:
            return False


def format_name_for_file(string: str) -> str:
    """Removes new lines, replaces spaces with underscores
    and """
    string = string.replace("\n", " ").strip().lower()

    string = re.sub(r"\s+", " ", string)

    if string:
        return string.replace(" ", "_")
    raise ValueError("No text to format")


def tap_request(service_url: str, query: str, sync_type: str) -> pd.DataFrame:
    """get TapPlus query data back as pandas DataFrame"""
    if not sync_type in ["async", "sync"]:
        raise ValueError("sync_type must be 'async' or 'sync'")

    tap_service = TapPlus(url=service_url)

    if sync_type == "async":
        job = tap_service.launch_job_async(query)
    else:
        job = tap_service.launch_job(query)

    result_csv = job.get_results().to_pandas().to_csv(index=False)
    print()
    return pd.read_csv(StringIO(result_csv))

# Data Cleaning
# ***********************
def clean_data(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """organise data alphabetaically and drop duplicates
    
    :param column_name: column name to sort data by"""
    print("cleaning...\n")
    data = _organise_data(data, column_name)
    data = _drop_duplicate_data(data)

    return data

def _organise_data(data, column_name):
    return data.sort_values(by=[column_name])

def _drop_duplicate_data(data):
    return data.drop_duplicates()
# ***********************


def show_cleaning(data: pd.DataFrame, data_colum: pd.DataFrame, column_name: str) -> None:
    """
    :param data_column: Dataframe.column to reference data by
    :param column_name: column name to reference data by
    """
    print(f"Rows in data: {data_colum.count().sum()}")
    duplicates = data.duplicated(subset=[column_name], keep='first')
    print(f"Number of non-duplicate data: {data_colum.count().sum() - duplicates.sum()}")
    print(f"Number of duplicate data: {duplicates.sum()}")
    print(f"Columns with null values:\n{data.isnull().sum()}\n")


def print_last_updated(table):
    date = get_last_updated(table)[0]

    print("Last updated on {}".format(date))
    