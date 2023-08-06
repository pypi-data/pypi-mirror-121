"""Module containing base exchange classes."""

from __future__ import annotations

import datetime as dtlib

from datetimerange import DateTimeRange
from thefuzz.process import extractOne as fuzzy_match
import ccxt
import pytz

from trading.datasets_core.errors import UnknownSymbolError
from trading.datasets_core.metadata.timeframe import Timeframe
from trading.datasets_core.utils.datetime_utils import to_datetime
from trading.datasets_core.utils.datetime_utils import to_milliseconds
from trading.datasets_core.utils.threading_utils import PropagatingThread


__all__ = [
    # Class exports
    "Exchange",
]


class Exchange(ccxt.Exchange):
    """Improved class implementation of the CCXT Exchange.

    This is used in conjuction with any of the specific exchanges
    in CCXT. So if we want to use this base Exchange class as a parent
    class, we would also need to add the specific exchange from
    CCXT as a parent class.

    For example:
    ```
    # Create a new exchange class. We need to use two
    # classes as parents, one from CCXT and the other
    # one is our base Exchange class.
    class NewBinanceExchange(Exchange, ccxt.binance):
        ...
    ```
    """

    # Must be overriden by subclasses to
    # maximize each individual exchange's limit
    FETCH_OHLCV_LIMIT = 100

    def __init__(self, config: dict | None = None):
        # Make sure config is an empty dictionary if its invalid
        if not config:
            config = {}

        # Force rate limit into the config
        config.update({"enableRateLimit": True})

        super().__init__(config)

        # Make sure markets are already loaded when instance is created
        # but only do it for subclasses of Exchange, not Exchange itself
        if issubclass(type(self), Exchange) and type(self) != Exchange:
            super().load_markets()

    def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe | str,
        start: dtlib.datetime | str | int | None = None,
        end: dtlib.datetime | str | int | None = None,
        include_latest: bool = True,
    ) -> list[list[int | float]]:

        """Fetches the OHLCV data from an exchange.

        Arguments:
            symbol: Ticker symbol of the crypto asset.
            timeframe: Timeframe of the candlestick data to fetch. Some
                examples of valid timeframe strings are `"2h"` for two
                hour, `"1d"` for one day, and `"1w"` for 1 week.
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            include_latest: If the `include_latest` variable is set to
                `True`, the latest OHLCV data is not returned since it
                is not finished yet. If set to `False`, then the
                unfinished data at the time `get_ohlcv()` was called
                will be returned.

        """

        # Validate and standardize the symbol before using it
        symbol = self.get_valid_symbol(symbol)

        # Standardize the timeframe before using it
        timeframe = Timeframe(timeframe)

        # Make sure that the start and end times are valid
        start, end = self.get_valid_start_end(
            start, end, timeframe, include_latest=include_latest)
        end_ms = to_milliseconds(end)

        # Create a datetime range from the initial start and end
        # datetimes and create a limit-based timedelta to generate a
        # list of new start and end timedates for the async OHLCV fetch
        time_range = DateTimeRange(start, end)
        time_range_tf = Timeframe(
            interval=(timeframe.interval * self.FETCH_OHLCV_LIMIT),
            unit=timeframe.unit)

        ohlcvs = []
        threads = []
        for start in time_range.range(time_range_tf.to_timedelta()):
            # Ignore the last start time given if its greater than
            # or equal to our goal end fetch time
            if start >= end:
                break  # pragma: no cover

            threads.append(PropagatingThread(
                target=self._per_thread_fetch_ohlcv,
                args=(
                    symbol,
                    timeframe,
                    start,
                    self.FETCH_OHLCV_LIMIT,
                    ohlcvs,
                )
            ))

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all of them to finish
        for thread in threads:
            thread.join()

        # Remove duplicates in the result, apply a hard-end-time-cap
        # filter, and then sort by timestamp
        ohlcvs = dict.fromkeys(tuple(x) for x in ohlcvs if x[0] <= end_ms)
        ohlcvs = sorted(ohlcvs)

        return ohlcvs

    def _per_thread_fetch_ohlcv(
        self,
        symbol: str,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
        ohlcvs: list[list[int | float]],
    ) -> list[list[int | float]]:

        # Generate parameters for CCXT's original `fetch_ohlcv()` function
        fetch_ohlcv_params = self._generate_fetch_ohlcv_params(
            timeframe, start, limit)

        ohlcv = super().fetch_ohlcv(
            symbol,
            str(timeframe),
            limit=limit,
            params=fetch_ohlcv_params)

        ohlcvs += ohlcv

    def _generate_fetch_ohlcv_params(
        self,
        timeframe: Timeframe,
        start: dtlib.datetime,
        limit: int,
    ) -> dict:

        raise NotImplementedError

    def get_valid_symbol(self, symbol: str) -> str:
        valid_symbol, match_score = fuzzy_match(
            str(symbol), self.markets.keys())

        # Raise an error if the exchange name is unrecognized or invalid
        if not symbol or match_score < 55:
            raise UnknownSymbolError(symbol)

        return valid_symbol

    def get_valid_start_end(
        self,
        start: dtlib.datetime | str | int | None,
        end: dtlib.datetime | str | int | None,
        timeframe: dataset_info.Timeframe,
        include_latest: bool = True,
    ) -> tuple[dtlib.datetime, dtlib.datetime]:

        """Validates and fills up the start and end times.

        Since we want the user to be able to readily use
        the `get_ohlcv()` without thinking much about this small detail,
        we automatically fill up the starting and end timestamps
        based on the parameters provided. Here are the different
        fill up cases:

        * If `start` and `end` are not provided, `end` is assigned the
          latest date and `start` is `end` minus the limit of one fetch
          based on the indicated exchange.
        * If either `start` and `end` are not provided but the other one
          is, we just add or subtract the same fetch limit to compute
          for `end` or `start`.
        * Lastly, if both are provided by the user, we use those without
          any other processing.

        Arguments:
            start: Starting datetime of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            end: Ending timestamp of the data to be fetched.
                The input argument can be a string indicating a
                valid datetime-like string or a number indicating the
                timestamp in milliseconds.
            timeframe: Timeframe of the candlestick data to fetch. Some
                examples of valid timeframe strings are `"2h"` for two
                hour, `"1d"` for one day, and `"1w"` for 1 week.
            include_latest: If the `include_latest` variable is set to
                `True`, the latest OHLCV data is not returned since it
                is not finished yet. If set to `False`, then the
                unfinished data at the time `get_ohlcv()` was called
                will be returned.

        Returns:
            A tuple containing the validated start and ending datetimes.
        """

        start = to_datetime(start)
        end = to_datetime(end)
        now = dtlib.datetime.utcnow().replace(tzinfo=pytz.utc)

        # Create a time adjustment variable to dynamically determine
        # the start or end times if ever one of them or both of them
        # are missing or invalid values.
        time_adjustment = timeframe.to_timedelta() * self.FETCH_OHLCV_LIMIT

        if not start and end:
            start = end - time_adjustment
        elif start and not end:
            end = start + time_adjustment
            if end > now:
                end = now
        elif not start and not end:
            end = now
            start = end - time_adjustment

        # If the end date is not less than the threshold
        # then don't include it, subtract timeframe from end
        if not include_latest:
            if end >= now:
                end -= timeframe.to_timedelta()

        return start, end
