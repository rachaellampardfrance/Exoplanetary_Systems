import os

import matplotlib.figure
import pandas as pd

from helpers.helpers import (
    get_user_confirm,
    is_png_jpg_jpeg,
    is_valid_file_name,
    get_date_str,
    path_exists
    )


def save_dated_figure(fig: object, fig_name: str, file_type: str) -> None:
    """
    :param figure: matplotlib fig 'object'
    :param figure_name: 'str'
    :param file_type: 'str' of png|jpeg|jpg
    """
    base_path = "static"

    try:
        _validate_figure_args(fig, fig_name, file_type)
    except (ValueError, TypeError) as e:
        print_faliure_msg(e)
        return
    
    todays_date = get_date_str()
    dir_path = _make_path(base_path, todays_date)
    file_name = _format_file_name(fig_name, todays_date, file_type)
    file_path = _make_path(dir_path, file_name)

    try:
        _create_todays_dir(dir_path)
    except OSError as e:
        print_faliure_msg(e)
        return
    
    try:
        _save_figure(fig, file_path)
    except OSError as e:
        print_faliure_msg(e)
        return


def _validate_figure_args(fig, fig_name, file_type):
    """Raises errors if validation not met"""
    if not isinstance(fig, matplotlib.figure.Figure):
        raise TypeError(
            "fig must be matplotlib.figure.Figure "
            "object not {}".format(type(fig))
        )

    if not is_valid_file_name(fig_name):
        raise ValueError("Invalid file name")

    if not is_png_jpg_jpeg(file_type):
        raise ValueError("Invalid file type")


def _make_path(current_path, add_path):
    return current_path+"/"+add_path


def _format_file_name(file_name, date, file_type):
    return file_name + "_" + date + "." + file_type
    # return file_name + get_hour_str() + "." + file_type


def _create_todays_dir(dir_name: str):
    if path_exists(dir_name):
        return
    os.makedirs(dir_name)
    print("new directory created {}".format(dir_name))


def _save_figure(figure, file_path):
    if path_exists(file_path):
        if not _overwrite_file_request():
            print("overwrite file aborted.")
            return
    # figure.savefig(file_path, transparent=True)
    figure.savefig(file_path)


def _overwrite_file_request() -> bool:
    """If figure file already exists request overwite"""
    query_overwrite_msg = (
        "File already exists would you "
        "like to over write the file Y/N?"
    )
    confirm_overwrite_msg = (
        "This action cannot be undone,"
        "confirm overwrite Y/N?"
    )
    if get_user_confirm(query_overwrite_msg):
        if get_user_confirm(confirm_overwrite_msg):
            return True
    return False

def print_faliure_msg(e):
    print(e)
    print("Failed to save file")


def save_dated_data_csv(file_data: pd.DataFrame, file_name: str):
    """try to save data to dated location with data stamp"""
    base_path = "static"

    try:
        _validate_dated_data_csv_args(file_data, file_name)
    except (ValueError, TypeError) as e:
        print_faliure_msg(e)
        return

    todays_date = get_date_str()
    dir_path = _make_path(base_path, todays_date)
    file_name = file_name + todays_date + ".csv"
    file_path = _make_path(dir_path, file_name)

    try:
        _create_todays_dir(dir_path)
    except OSError as e:
        print_faliure_msg(e)
        return
    
    try:
        file_data.to_csv(file_path, index=False)
    except OSError as e:
        print_faliure_msg(e)
        return

def _validate_dated_data_csv_args(file_data: pd.DataFrame, file_name: str) -> None:
    """raises errors if not of valid args"""

    if not isinstance(file_data, pd.DataFrame):
        raise TypeError(
            "data must be pandas.DataFrame "
            "object not {}".format(type(file_data))
        )
    
    if not is_valid_file_name(file_name):
        raise ValueError("Invalid file name")
