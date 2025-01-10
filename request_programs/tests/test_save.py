# import re

from matplotlib import pyplot as plt
import pandas as pd
import pytest


from save import _validate_figure_args, _validate_dated_data_csv_args

VALID_MATPLOTLIB_FIGURE, _ = plt.subplots(figsize=(8, 6))

# VALID_DATAFRAME_FILE_DATA = pd.read_csv("stellar_hosts_schema.csv")

INVALID_DATA_TYPES = ["a", 1, [], {}, ()]

VALID_FILE_NAME = "File_Name-~"
INVALID_FILE_NAMES = ["fig name", "FIG.name", 
                           "file,", "file>",
                           "file<", "file:",
                           "file;", "file/",
                           "file?", "file*",
                           "file=", "file|",
                           "file'", "file\\",
                           "file\"", "file%"]

VALID_IMG_FILE_TYPES = ["jpg","jpeg","png","JPG","JPEG","PNG",]
INVALID_IMG_FILE_TYPES = [".jpg", "pdf", "csv"]

def test_validate_figure_args_valid_filetypes():
    for file_type in VALID_IMG_FILE_TYPES:
        try:
            _validate_figure_args(VALID_MATPLOTLIB_FIGURE, VALID_FILE_NAME, file_type)
        except ValueError as e:
            assert False, f"_validate_figure_args raised unexpected error: {str(e)}"
        except TypeError as e:
            assert False, f"_validate_figure_args raised unxpected TypeError: {str(e)}"

def test_validate_figure_args_raises_invalid_figure():
    for data_type in INVALID_DATA_TYPES:
        with pytest.raises(TypeError, match=(
            "fig must be matplotlib.figure.Figure "
            "object not {}".format(type(data_type)))
        ):
            _validate_figure_args(data_type, VALID_FILE_NAME, VALID_IMG_FILE_TYPES[0])

def test_validate_figure_args_raises_invalid_filename():
    for file_name in INVALID_FILE_NAMES:
        with pytest.raises(ValueError, match="Invalid file name"):
            _validate_figure_args(VALID_MATPLOTLIB_FIGURE, file_name, VALID_IMG_FILE_TYPES[0])

def test_validate_figure_args_raises_invalid_filetypes():
    for file_type in INVALID_IMG_FILE_TYPES:
        with pytest.raises(ValueError, match="Invalid file type"):
            _validate_figure_args(VALID_MATPLOTLIB_FIGURE, VALID_FILE_NAME, file_type)


# def test_validate_dated_data_csv_args_valid_args():
#     try:
#         _validate_dated_data_csv_args(VALID_DATAFRAME_FILE_DATA, VALID_FILE_NAME)
#     except TypeError as e:
#         assert False, f"_validate_dated_data_csv_args raised unxpected TypeError: {str(e)}"
#     except ValueError as e:
#         assert False, f"_validate_dated_data_csv_args raised unxpected ValueError: {str(e)}"

def test_validate_dated_data_csv_args_raises_invalid_dataframe():
    for data_type in INVALID_DATA_TYPES:
        with pytest.raises(TypeError, match=(
            "data must be pandas.DataFrame "
            "object not {}".format(type(data_type)))
        ):
            _validate_dated_data_csv_args(data_type, VALID_FILE_NAME)

# def test_validate_dated_data_csv_args_raises_invalid_filename():
#     for file_name in INVALID_FILE_NAMES:
#         with pytest.raises(ValueError, match="Invalid file name"):
#              _validate_dated_data_csv_args(VALID_DATAFRAME_FILE_DATA, file_name)
