#!/usr/bin/env python

"""Tests for `pyecodevices_rt2` package."""
from click.testing import CliRunner

from pyecodevices_rt2 import EcoDevicesRT2, cli

from pyecodevices_rt2.const import (
    PRODUCT_ENTRY,
    PRODUCT_VALUE
)

from pyecodevices_rt2.exceptions import (
    EcoDevicesRT2RequestError,
)

import pytest
import os
from dotenv import load_dotenv
import logging
import time

_LOGGER = logging.getLogger(__name__)
load_dotenv()

ECORT2_HOST = os.environ.get("ECORT2_HOST", "")
ECORT2_PORT = os.environ.get("ECORT2_PORT", 80)
ECORT2_APIKEY = os.environ.get("ECORT2_APIKEY", "")


@pytest.fixture
def test_ping():
    ecodevices = None
    """Sample pytest test function with the pytest fixture as an argument."""
    if (ECORT2_APIKEY != ""):
        ecodevices = EcoDevicesRT2(ECORT2_HOST, ECORT2_PORT, ECORT2_APIKEY)
        _LOGGER.debug("# ping")
        assert ecodevices.ping()
    else:
        _LOGGER.warning("""No host/apikey defined in environement variable for GCE Ecodevices RT2.
Test 'ping' not started.""")
    return ecodevices


def test_ecodevicesrt2(test_ping):
    assert isinstance(test_ping.host, str)
    assert isinstance(test_ping.apikey, str)
    assert isinstance(test_ping.apiurl, str)

    assert test_ping.get("Index", "All", PRODUCT_ENTRY) == PRODUCT_VALUE

    # Test exceptions
    with pytest.raises(EcoDevicesRT2RequestError):
        test_ping.get("Index", "All", "EcoDevicesRT2RequestError")


def test_counter(test_ping):
    from pyecodevices_rt2 import Counter

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'Counter' not started.")
    else:
        wait = 1
        for x in range(1, 13):
            test = Counter(test_ping, x)
            assert isinstance(test.value, int)
            assert isinstance(test.price, (int, float))

        test = Counter(test_ping, 1)
        actual = test.value
        # Test ADD
        current = test.value
        assert test.add(5)
        time.sleep(wait)
        temp = test.value
        assert temp == current + 5
        # Test SUBSTRACT
        current = test.value
        assert test.substrat(10)
        time.sleep(wait)
        temp = test.value
        assert temp == current - 10
        # Test Equal operator and Restore original value
        test.value = actual
        time.sleep(wait)
        temp = test.value
        assert temp == actual


def test_digitalinput(test_ping):
    from pyecodevices_rt2 import DigitalInput

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'DigitalInput' not started.")
    else:
        # Test posts
        for x in range(1, 13):
            test = DigitalInput(test_ping, x)
            assert isinstance(test.status, bool)


def test_enocean(test_ping):
    from pyecodevices_rt2 import EnOceanSensor, EnOceanSwitch

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'EnOcean' not started.")
    else:
        wait = 5
        for x in range(1, 24):
            test = EnOceanSensor(test_ping, x)
            assert isinstance(test.value, (int, float))

        for x in range(1, 24):
            test = EnOceanSwitch(test_ping, x)
            assert isinstance(test.status, bool)

        test = EnOceanSwitch(test_ping, 2)
        actual = test.status
        # Test OFF
        assert test.off() is True
        time.sleep(wait)
        assert test.status is False
        # Test ON
        assert test.on() is True
        time.sleep(wait)
        assert test.status is True
        # Test Toggle
        assert test.toggle() is True
        time.sleep(wait)
        assert test.status is False
        # Test Equal operator
        test.status = True
        time.sleep(wait)
        assert test.status is True
        # Restore original value
        test.status = actual
        time.sleep(wait)
        assert test.status == actual


def test_post(test_ping):
    from pyecodevices_rt2 import Post

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'Post' not started.")
    else:
        # Test posts
        for x in range(1, 9):
            test = Post(test_ping, x)
            assert isinstance(test.index, (int, float))
            assert isinstance(test.index_day, (int, float))
            assert isinstance(test.instant, (int, float))
            assert isinstance(test.price, (int, float))
            assert isinstance(test.price_day, (int, float))

        # Test subposts
        for x in range(1, 9):
            for y in range(1, 9):
                test = Post(test_ping, x, y)
                assert isinstance(test.index, (int, float))
                assert isinstance(test.index_day, (int, float))
                assert isinstance(test.instant, (int, float))
                assert isinstance(test.price, (int, float))
                assert isinstance(test.price_day, (int, float))


def test_relay(test_ping):
    from pyecodevices_rt2 import Relay

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'Relay' not started.")
    else:
        wait = 1
        for x in range(1, 11):
            test = Relay(test_ping, x)
            assert isinstance(test.status, bool)

        test = Relay(test_ping, 1)
        current = test.status
        # Test OFF
        assert test.off() is True
        time.sleep(wait)
        assert test.status is False
        # Test ON
        assert test.on() is True
        time.sleep(wait)
        assert test.status is True
        # Test Toggle
        assert test.toggle() is True
        time.sleep(wait)
        assert test.status is False
        # Test Equal operator
        test.status = True
        time.sleep(wait)
        assert test.status is True
        # Restore original value
        test.status = current
        time.sleep(wait)
        assert test.status == current


def test_supplierindex(test_ping):
    from pyecodevices_rt2 import SupplierIndex

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'SupplierIndex' not started.")
    else:
        for x in range(1, 9):
            test = SupplierIndex(test_ping, x)
            assert isinstance(test.value, (int, float))
            assert isinstance(test.price, (int, float))


def test_toroid(test_ping):
    from pyecodevices_rt2 import Toroid

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'Toroid' not started.")
    else:
        for x in range(1, 5):
            test = Toroid(test_ping, x)
            assert isinstance(test.value, (int, float))
            assert isinstance(test.price, (int, float))
            assert isinstance(test.consumption, (int, float))
            assert isinstance(test.consumption_price, (int, float))
            assert isinstance(test.production, (int, float))
            assert isinstance(test.production_price, (int, float))

        for x in range(5, 17):
            test = Toroid(test_ping, x)
            assert isinstance(test.value, (int, float))
            assert isinstance(test.price, (int, float))

        # Test default is production
        test = Toroid(test_ping, 1, False)
        assert isinstance(test.value, (int, float))
        assert isinstance(test.price, (int, float))

        # Test exceptions
        with pytest.raises(EcoDevicesRT2RequestError):
            test = Toroid(test_ping, 5, False)
            assert isinstance(test.consumption, (int, float))
        with pytest.raises(EcoDevicesRT2RequestError):
            test = Toroid(test_ping, 5, False)
            assert isinstance(test.consumption_price, (int, float))
        with pytest.raises(EcoDevicesRT2RequestError):
            test = Toroid(test_ping, 5, False)
            assert isinstance(test.production, (int, float))
        with pytest.raises(EcoDevicesRT2RequestError):
            test = Toroid(test_ping, 5, False)
            assert isinstance(test.production_price, (int, float))


def test_virtualoutput(test_ping):
    from pyecodevices_rt2 import VirtualOutput

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'VirtualOutput' not started.")
    else:
        for x in range(1, 129):
            test = VirtualOutput(test_ping, x)
            assert isinstance(test.status, bool)


def test_x4fp(test_ping):
    from pyecodevices_rt2 import X4FP

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'X4FP' not started.")
    else:
        wait = 5
        for x in range(1, 3):
            for y in range(1, 5):
                test = X4FP(test_ping, x, y)
                assert test.mode in range(-1, 6)

        test = X4FP(test_ping, 1, 1)
        actual = test.mode
        # Test modes change
        for x in range(1, 6):
            test.mode = x
            time.sleep(wait)
            assert test.mode == x

        # Restore original value
        test.value = actual
        time.sleep(wait)
        temp = test.value
        assert temp == actual


def test_xthl(test_ping):
    from pyecodevices_rt2 import XTHL

    if (test_ping is None):
        _LOGGER.warning("No connexion. Test 'XTHL' not started.")
    else:
        for x in range(1, 3):
            test = XTHL(test_ping, x)
            assert isinstance(test.humidity, (int, float))
            assert isinstance(test.luminosity, (int, float))
            assert isinstance(test.temperature, (int, float))


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'pyecodevices_rt2.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
