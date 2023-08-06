#  Copyright (c) 2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Tests for Sensor Conversion Utils
"""

import pytest

from hvl_ccb.utils.conversion_sensor import (
    LEM4000S,
    LMT70A
)


def test_lem4000s():
    lem = LEM4000S()
    assert lem.shunt == 1.2
    lem.shunt = 2
    assert lem.shunt == 2
    with pytest.raises(ValueError):
        lem.shunt = -1
    with pytest.raises(AttributeError):
        lem.CONVERSION = 1
    with pytest.raises(ValueError):
        lem.calibration_factor = 1.5
    lem.shunt = 1.2
    assert lem.convert(1.2) == 5000


def test_lmt70a():
    lmt = LMT70A()
    with pytest.raises(AttributeError):
        lmt.LUT = 1
    with pytest.raises(ValueError):
        lmt.temperature_unit = 'R'
    with pytest.raises(ValueError):
        lmt.transfer_function_order = 5
    assert lmt.convert(0.943227) == 30
    lmt.transfer_function_order = 1
    assert round(lmt.convert(0.943227), 3) == 29.966
    lmt.transfer_function_order = 2
    assert round(lmt.convert(0.943227), 3) == 29.990
    lmt.transfer_function_order = 3
    assert round(lmt.convert(0.943227), 3) == 30.001
