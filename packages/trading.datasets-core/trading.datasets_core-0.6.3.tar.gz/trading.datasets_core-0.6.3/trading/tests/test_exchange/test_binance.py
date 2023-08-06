"""Tests for trading.datasets_core.exchange.binance."""
# pylint: disable=missing-class-docstring,missing-function-docstring

import ccxt
import pytest

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.exchange import BinanceExchange
from trading.datasets_core.exchange import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_datetime


@pytest.fixture(name="exchange", scope="class")
def fixture_exchange():
    return BinanceExchange()


class TestExchangeBinance:

    def test_initialization(self, exchange):
        assert issubclass(type(exchange), Exchange)
        assert isinstance(exchange, BinanceExchange)

    def test_generate_fetch_ohlcv_params(self, exchange):
        expected_output = {'startTime': 1317168000000, 'limit': 1000}
        assert exchange._generate_fetch_ohlcv_params(
            Timeframe('1h'), to_datetime('2011'), 1000) == expected_output

        expected_output = {'startTime': 970099200000, 'limit': 12}
        assert exchange._generate_fetch_ohlcv_params(
            Timeframe('1d'), to_datetime('2000'), 12) == expected_output

    def test_validating_symbol(self, exchange):
        with pytest.raises(UnknownSymbolError):
            exchange.get_valid_symbol('BKAHDBLAJDHunknwonExchange')

    def test_unsuccessful_fetch_ohlcv(self, exchange, mocker):
        """Separate unsuccessful case so it can be mock patched."""
        mocker.patch(
            'ccxt.binance.fetch_ohlcv', side_effect=ccxt.ExchangeError)
        mocker.patch('time.sleep', return_value=None)

        with pytest.raises(ccxt.ExchangeError):
            exchange.fetch_ohlcv(
                symbol='btcusd',
                timeframe='1d',
                start='JAN 1 2021',
                end='JAN 4 2021')

    def test_successful_fetch_ohlcv(self, exchange):
        expected_output = [
            (1609459200000, 28923.63, 28961.66, 28913.12, 28961.66, 27.457032),
            (1609459260000, 28961.67, 29017.5, 28961.01, 29009.91, 58.477501),
            (1609459320000, 29009.54, 29016.71, 28973.58, 28989.3, 42.470329),
        ]
        assert exchange.fetch_ohlcv(
            symbol='btcusd',
            timeframe='1m',
            start='JAN 1 2021 00:00:00+00:00',
            end='JAN 1 2021 00:02:00+00:00') == expected_output

        assert exchange.fetch_ohlcv(
            symbol='btcusd',
            timeframe='1d',
            start='JAN 1 2000',
            end='JAN 4 2000') == []
