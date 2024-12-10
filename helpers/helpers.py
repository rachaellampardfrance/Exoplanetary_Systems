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

def make_path(current_path, add_path):
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
