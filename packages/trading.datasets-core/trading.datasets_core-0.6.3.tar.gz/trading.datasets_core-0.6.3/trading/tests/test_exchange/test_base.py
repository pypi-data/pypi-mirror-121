"""Tests for trading.datasets_core.exchange.base."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import datetime as dtlib

import ccxt
import pytest
import pytz

from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.utils.datetime_utils import to_datetime


@pytest.fixture(name='exchange', scope="class")
def fixture_exchange():
    return Exchange()


class TestExchangeBase:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), ccxt.Exchange)
        assert isinstance(exchange, Exchange)

    def test_unimplemented_generate_fetch_ohlcv_params(self, exchange):
        with pytest.raises(NotImplementedError):
            exchange._generate_fetch_ohlcv_params(None, None, None)

    def test_validating_start_and_end_datetimes(self, exchange):
        timeframe = Timeframe(interval=1, unit='d')
        expected_start = to_datetime('2020-09-23')
        expected_end = to_datetime('2021-01-01')

        assert exchange.get_valid_start_end(
            None, '2021-01-01', timeframe) == (expected_start, expected_end)
        assert exchange.get_valid_start_end(
            '2020-09-23', None, timeframe) == (expected_start, expected_end)

        now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)
        result_start, result_end = exchange.get_valid_start_end(
            None, None, timeframe)

        assert result_end.year == now.year
        assert result_end.month == now.month
        assert result_end.day == now.day
        assert result_start < now

        test_start = now - dtlib.timedelta(days=1)
        result_start, result_end = exchange.get_valid_start_end(
            test_start, None, timeframe)

        assert result_end.year == now.year
        assert result_end.month == now.month
        assert result_end.day == now.day
        assert result_start == test_start

    def test_validating_start_and_end_excluding_latest(self, exchange):
        timeframe = Timeframe(interval=1, unit='d')
        now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)
        result_start, result_end = exchange.get_valid_start_end(
            None, None, timeframe, include_latest=False)

        assert result_end.year == now.year
        assert result_end.month == now.month
        assert result_end.day != now.day
