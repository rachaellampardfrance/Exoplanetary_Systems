"""helper fucntions for data gathering/saving"""
from datetime import datetime
from datetime import date
from io import StringIO
import os
import re

from astroquery.utils.tap.core import TapPlus
import pandas as pd

# PATH = "directory"

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


def is_png_jpg_jpeg(string: str) -> bool:
    pattern = r"^(jpg|jpeg|png|JPG|JPEG|PNG)$"
    if re.search(pattern, string):
        return True
    return False

def is_valid_file_name(string: str) -> bool:
    pattern = r"^[^/\\:*?<>;=%|.,\"' ]+$"
    if re.search(pattern, string):
        return True
    return False

def get_date_str() -> str:
    """:returns: 'str' of current date in YYYYMMDD format"""
    return str(date.today()).replace("-", "")

def path_exists(path_name: str) -> bool:
    return os.path.exists(path_name)

def make_path(current_path: str, add_path: str) -> str:
    return current_path+"/"+add_path

def get_dirs(directory: str) -> list|None:
    """:returns: all directories within a directory"""
    pattern = r"[0-9]{8}$"
    return [x for x in os.listdir(directory) if not "." in x and re.search(pattern, x)]

def find_last_date_dir(directory: str) -> str:
    """find most recent dated directory within a directory
    
    :returns: 'str' directory name"""
    pattern = r"/$"
    if not re.search(pattern, directory):
        raise ValueError("path must end with /")

    if not path_exists(directory):
        raise FileNotFoundError("directory not found")

    folders = get_dirs(directory)
    if not folders:
        raise FileNotFoundError()

    # orders folders by most recent date name
    folders = sorted(folders, key=lambda x: datetime.strptime(x[-8:], '%Y%m%d'), reverse=True)

    return folders[0]

def get_last_csv(file_name: str, directory: str) -> str|None:
    """
    :param file_name: file_name to match
    :param directory: dir to search
    :returns: 'str' path of latest csv file with
    filename args match from a given dir
    """
    path: str = directory + find_last_date_dir(directory)
    files: list = [x for x in os.listdir(path) if ".csv" in x]
    for file in files:
        if file_name in file:
            return make_path(path, file)
    return None
    # raise FileNotFoundError("{} file not found in {}".format(file_name, directory))


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
    return pd.read_csv(StringIO(result_csv))


def clean_data(data: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """organise data alphabetaically and drop duplicates
    
    :param column_name: column name to sort data by"""
    data = _organise_data(data, column_name)
    data = _drop_duplicate_data(data)

    return data

def _organise_data(data, column_name):
    return data.sort_values(by=[column_name])

def _drop_duplicate_data(data):
    return data.drop_duplicates()


def show_cleaning(data: pd.DataFrame, data_colum: pd.DataFrame, column_name: str) -> None:
    """
    :param data_column: Dataframe.column to reference data by
    :param column_name: column name to reference data by
    """
    print(f"Rows in data: {data_colum.count().sum()}\n")
    duplicates = data.duplicated(subset=[column_name], keep='first')
    print(f"Number of non-duplicate systems: {data_colum.count().sum() - duplicates.sum()}")
    print(f"Number of duplicate systems: {duplicates.sum()}")
    print(f"Columns with null values:\n{data.isnull().sum()}")
