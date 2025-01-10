"""Collection of tests for the star class"""

import pytest
import random
import sqlite3

from helpers.star import Star

DB = 'database.db'
DEFAULT = "Unknown"
STAR_CLASSES = {
    'O': ['Blue', '> 30,000'],
    'B': ['Blue-white', '9,700 - 30,000'],
    'A': ['White', '7,200 - 9,700'],
    'F': ['Yellow-white', '5,700 - 7,200'],
    'G': ['Yellow', '4,900 - 5,700'],
    'K': ['Orange', '3,400 - 4,900'],
    'M': ['Red', '2,100 - 3,400'],
    'L': ['Brown dwarf', '1,300 - 2,400'],
    'T': ['Brown dwarf', '< 1,600'],
    'Y': ['Brown dwarf', '< 700']
}
SUBCLASS_HEAT_RANGES = {
    "0": "Hottest",
    "1": "Hotter",
    "2": "Hot",
    "3": "High average",
    "4": "Average",
    "5": "Average",
    "6": "Low average",
    "7": "Cool",
    "8": "Cooler",
    "9": "Coolest"
}
LUMINOSITY = {
    'IA-O': 'Extremely Luminous Hypergiant',
    'IA': 'Hypergiant',
    'IAB': 'Intermediate Luminous Hypergiant',
    'IB': 'Lesser Hypergiant',
    'II': 'Bright Giant',
    'III': 'Giant',
    'IV': 'Subgiant',
    'V': 'Main Sequence Dwarf',
    'VI': 'Subdwarf',
    'VII': 'White Dwarf'
}
# add random prefix and sufix to str
PREFIX_SUFIX = [".", "", "/", "N", "P"]
TEST_NAME = "K2-136" # K5 V


# TESTS: Star.__init__()
# **********************
def test_Star():
    """Assert star class initialises correctly"""
    with sqlite3.connect(DB) as conn:

        star = Star(TEST_NAME, conn)

        assert star.name == "K2-136"
        assert star.full_class_id == "K5 V"
        assert star.class_id == "K"
        assert star.st_class == "Orange"
        assert star.heat == "3,400 - 4,900"
        assert star.sub_class == "Average K type star"
        assert star.lumin == "Main Sequence Dwarf"

def test_Star_no_spec():
    """Assert star class initialises correctly"""
    with sqlite3.connect(DB) as conn:
        name = "KMT-2022-BLG-0303L"

        star = Star(name, conn)

        assert star.name == "KMT-2022-BLG-0303L"
        assert star.full_class_id == "Unknown"
        assert star.class_id == ""
        assert star.st_class == ""
        assert star.heat == ""
        assert star.sub_class == ""
        assert star.lumin == ""
# **********************


# TESTS: Star._set_class_id()
# **********************
def test_set_class_id():
    """function sets corresponding star class key
    back if found in star._full_class_id"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)

    for key in STAR_CLASSES:
        star._full_class_id = random.choice(PREFIX_SUFIX) + key + random.choice(PREFIX_SUFIX)
        star._set_class_id()
        assert star.class_id == key


def test_set_class_id_default():
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)

    for invalid in PREFIX_SUFIX:
        star._full_class_id = invalid
        star._set_class_id()
        assert star.class_id == DEFAULT
# **********************


# TESTS: Star._set_st_class()
# **********************
def test_set_st_class():
    """function sets class e.g 'Orange' from star._st_class"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)
    
    for key in STAR_CLASSES:
        star._class_id = key
        star._set_st_class()
        assert star.st_class == STAR_CLASSES[key][0]

def test_set_st_class_default():
    """function sets class st_class to star.DEFAULT
    when star.class_id is Star.DEFAULT"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)

    star._class_id = Star.DEFAULT
    star._set_st_class()
    assert star.st_class == Star.DEFAULT
# **********************


# TESTS: Star._set_heat()
# **********************
def test_set_heat():
    """function sets class heat e.g star.DEFAULT
    from star._st_class"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)
    
    for key in STAR_CLASSES:
        star._class_id = key
        star._set_heat()
        assert star.heat == STAR_CLASSES[key][1]

def test_set_heat_default():
    """function sets class heat to star.DEFAULT
    when star.class_id is Star.DEFAULT"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)

    star._class_id = Star.DEFAULT
    star._set_heat()
    assert star.heat == Star.DEFAULT
# **********************


# TESTS: Star._set_sub_class()
# **********************
def test_set_sub_class():
    """function sets class sub_class text e.g
    'Hot G type star' by star.full_class_id and
    star.class_id"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)

    # 0-9
    for key in SUBCLASS_HEAT_RANGES:
        st_class = random.choice(list(STAR_CLASSES.keys())) # O, A, B...
        lumin = random.choice(list(LUMINOSITY.keys())) # II, IV...

        star._full_class_id = st_class + key + lumin
        star._class_id = st_class
        star._set_sub_class()
        text = f" {st_class} type star"
        assert star.sub_class == SUBCLASS_HEAT_RANGES[key] + text

def test_set_sub_class_default():
    """function sets class sub_class to star.DEFAULT
    when star.full_class_id is Star.DEFAULT"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)
    
    for invalid in PREFIX_SUFIX:
        star._full_class_id = invalid
        star._set_sub_class()
        assert star.sub_class == Star.DEFAULT
# **********************


# TESTS: Star._set_lumin()
# **********************
def test_set_lumin():
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)
    
    for key in LUMINOSITY:
        st_class = random.choice(list(STAR_CLASSES.keys())) # O, A, B...
        sub_class = random.choice(list(SUBCLASS_HEAT_RANGES.keys())) # 0-9

        star._full_class_id = st_class + sub_class + key
        star._set_lumin()
        assert star.lumin == LUMINOSITY[key]

def test_set_lumin_default():
    """function sets class lumin to star.DEFAULT
    when lumin identifier is not found"""
    star = Star
    with sqlite3.connect(DB) as conn:
        star = Star(TEST_NAME, conn)
    
    for invaild in PREFIX_SUFIX:
        star._full_class_id = invaild
        star._set_lumin()
        assert star.lumin == Star.DEFAULT
# **********************


# TESTS: Star.()
# **********************
    # tests
# **********************