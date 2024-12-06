import pytest
from matplotlib import pyplot as plt

from helpers.helpers import is_png_jpg_jpeg, is_valid_file_name

DATAFRAME_FIGURE, ax = plt.subplots(figsize=(8, 6))
valid_fig_name = "fig_name"

def test_is_png_jpg_jpeg_true():
    valid_img_types = ["jpg","jpeg","png","JPG","JPEG","PNG",]

    for img_type in valid_img_types:
        assert is_png_jpg_jpeg(img_type) == True


def test_is_png_jpg_jpeg_false():
    invalid_img_types = [".jpg", "pdf", "txt"]

    for img_type in invalid_img_types:
        assert is_png_jpg_jpeg(img_type) == False


def test_is_valid_file_name_true():
    valid_file_names = ["fig_name", "FIG_name", "file$"]
    for file_name in valid_file_names:
        assert is_valid_file_name(file_name) == True

def test_is_valid_file_name_false():
    in_valid_file_names = ["fig name", "FIG.name", 
                           "file,", "file>",
                           "file<", "file:",
                           "file;", "file/",
                           "file?", "file*",
                           "file=", "file|",
                           "file'", "file\\",
                           "file\"", "file%"]
    for file_name in in_valid_file_names:
        assert is_valid_file_name(file_name) == False
