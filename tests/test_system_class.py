"""System class instance tests"""

import pytest
from helpers.system import System

def test_init_raises():
    """If stellar_body does not find a corresponding
    planet/star/system"""
    with pytest.raises(TypeError):
        system = System("aaa")
