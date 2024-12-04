from datetime import datetime
from datetime import date
import os
import re

path = "directory"

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


def get_hour_str():
    """:returns: 'str': HH format"""
    return datetime.now().strftime("%H")

def get_date_str() -> str:
    """:returns: 'str' of current date in YYYYMMDD format"""
    return str(date.today()).replace("-", "")


def path_exists(path_name: str) -> bool:
    return os.path.exists(path_name)


def format_name_for_file(string: str) -> str:
    """Removes new lines, replaces spaces with underscores
    and """
    string = string.replace("\n", " ").strip().lower()

    string = re.sub(r"\s+", " ", string)

    if string:
        return string.replace(" ", "_")
    raise ValueError("No text to format")
