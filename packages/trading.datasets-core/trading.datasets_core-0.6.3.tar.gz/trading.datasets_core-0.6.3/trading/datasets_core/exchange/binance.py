"""Module containing the Binance Exchange class."""

from __future__ import annotations

import datetime as dtlib
import ccxt

from trading.datasets_core.exchange.base import Exchange
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_milliseconds


__all__ = [
    # Class exports
    "BinanceExchange",
]


class BinanceExchange(Exchange, ccxt.binance):
    """Improved class implementation of the CCXT Binance Exchange."""

    FETCH_OHLCV_LIMIT = 999

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        return {
            "startTime": int(to_milliseconds(start)),
            "limit": limit,
        }
