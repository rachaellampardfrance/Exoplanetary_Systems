import pytest
import random

from main import (
    get_class, get_spectral_class_id,
    get_class_details, get_sub_class_heat,
    get_spec_type, get_luminosity
)

DEFAULT = "Unknown"
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
# add random prefix and sufix to str
PREFIX_SUFIX = [".", "", "/", "N", "P"]


# TESTS: get_spectral_class_id
# **********************
def test_get_spectral_class_id():
    """function returns correspondingh star class key
    back if found in str"""
    for key in STAR_CLASSES:
        string = random.choice(PREFIX_SUFIX) + key + random.choice(PREFIX_SUFIX)
        assert get_spectral_class_id(string) == key


def test_get_spectral_class_id_none():
    # returns None
    for invaild in PREFIX_SUFIX:
        assert get_spectral_class_id(invaild) == None
# **********************


# TESTS: get_class_details
# **********************
def test_get_class_details():
    """function returns corresponding dict values in a tuple if
    key is present in str
    """
    for key in STAR_CLASSES:
        assert get_class_details(key) == (STAR_CLASSES[key][0], STAR_CLASSES[key][1])
# **********************


# TESTS: get_sub_class_heat
# **********************
def test_get_sub_class_heat_returns():
    """function returns correct corresponding dict str
    to dict key.
    """

    # Manual: returns correct sub heat
    iii_sub_class = "ZK1VI"
    assert get_sub_class_heat(iii_sub_class) == "Hotter"

    # Automated: check index values return expected strings
    for i in range(len(SUBCLASS_HEAT_RANGES)):
        index = str(i)
        assert get_sub_class_heat(index) == SUBCLASS_HEAT_RANGES[index]


def test_get_sub_class_heat_returns_none():
    """function returns None when there are no heat identifiers in str."""
    invailds = ["HM", "", "!", "M IV"]

    for i in range(len(invailds)):
        assert get_sub_class_heat(invailds[i]) == None
# **********************


# TESTS: get_class
# **********************
def test_get_class():
    """returns correct dict with class"""
    valid_class = "M2 III"

    assert get_class(valid_class, DEFAULT) == {
        'class': 'Red',
        'heat': '2,100 - 3,400',
        'sub_heat': 'Hot M type star'
    }
# create fully automated tests
# **********************


# TESTS: get_spec_type
# **********************
def test_get_spec_type():
    """function returns dictionary with star details 
    from identifiers in string
    """
    # Manual default tests
    partial_classes = ["M III", "K9"]

    assert get_spec_type(partial_classes[0]) == {   
        'class': 'Red',
        'heat': '2,100 - 3,400',
        'sub_heat': DEFAULT,
        "luminosity": 'Giant',
    }
    assert get_spec_type(partial_classes[1]) == {
        'class': 'Orange',
        'heat': '3,400 - 4,900',
        'sub_heat': "Coolest K type star",
        "luminosity": DEFAULT,
    }

    # Automated
    for key in STAR_CLASSES:
        # sub_class_pair = random.choice(SUBCLASS_HEAT_RANGES.keys())
        # lumin_pair = random.choice(LUMINOSITY.keys())

        sub_class = random.choice(list(SUBCLASS_HEAT_RANGES.keys()))
        lumin = random.choice(list(LUMINOSITY.keys()))

        star = key + sub_class + " " + lumin
        sub_heat = SUBCLASS_HEAT_RANGES[sub_class]
        sub_heat_str = sub_heat + " " + key + " " + "type star"

        assert get_spec_type(star) == {
            'class': STAR_CLASSES[key][0],
            'heat': STAR_CLASSES[key][1],
            'sub_heat': sub_heat_str,
            "luminosity": LUMINOSITY[lumin],
        }
# **********************



# TESTS: get_luminosity(spec: str, default: str) -> str
# **********************
def test_get_luminosity():
    """returns corrospoding value when key is found in str"""

    # add prefix and sufix to str  
    add = [".", "", "A", "P", "1", "12"]

    for key in LUMINOSITY:
        string = random.choice(PREFIX_SUFIX) + key + random.choice(PREFIX_SUFIX)
        assert get_luminosity(string, DEFAULT) == LUMINOSITY[key]

def test_get_luminosity_default():
    """returns default value if no key match"""
    invalids = ["O", "M2", "IX", ".", ""]

    for invaild in invalids:
        assert get_luminosity(invaild, DEFAULT) == DEFAULT
# **********************


# TESTS: function_name
# **********************
    # tests
# **********************