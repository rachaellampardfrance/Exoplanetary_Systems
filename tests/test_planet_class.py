"""Collection of tests for the planet class"""

import pytest
import random
import sqlite3

from helpers.planet import Planet

DB = 'database.db'
DEFAULT = "Unknown"
TEST_NAME = "GJ 667 C b" 
# host = GJ 667 C | cb = "No" | pub = 2013-01
EMPTY = ""


# TESTS: Planet.__init__()
# **********************
def test_init():
    """Class initialises correctly with expected inputs"""
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)

        assert planet.name == "GJ 667 C b"
        assert planet.hostname == "GJ 667 C"
        assert planet.cb_flag == "No"
        assert planet.disc_pubdate == "2013-01"
# **********************


# TESTS: Planet._set_disc_pubdate()
# **********************
def test_set_disc_pubdate():
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_disc_pubdate("2013-04")
        assert planet.disc_pubdate == "2013-04"

def test_set_disc_pubdate_default():
    """function sets class var to Planet.DEFAULT
    if empty"""
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_disc_pubdate(EMPTY)
        assert planet.disc_pubdate == Planet.DEFAULT
# **********************


# TESTS: Planet._set_hostname()
# **********************
def test_set_hostname():
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_hostname("Earth")
        assert planet.hostname == "Earth"

def test_set_hostname_default():
    """function sets class var to Planet.DEFAULT
    if empty"""
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_hostname(EMPTY)
        assert planet.hostname == Planet.DEFAULT
# **********************


# TESTS: Planet._set_cb_flag()
# **********************
def test_set_cb_flag():
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_cb_flag(1)
        assert planet.cb_flag == "Yes"

    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_cb_flag(0)
        assert planet.cb_flag == "No"

def test_set_cb_flag_default():
    """function sets class var to Planet.DEFAULT
    if empty"""
    with sqlite3.connect(DB) as conn:
        planet = Planet(TEST_NAME, conn)
        planet._set_cb_flag(EMPTY)
        assert planet.cb_flag == Planet.DEFAULT
# **********************


# TESTS: Planet.()
# **********************
    # tests
# **********************