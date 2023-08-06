"""Module containing datetime-related utility functions."""

from __future__ import annotations

import datetime as dtlib

from dateutil import parser
import pytz


__all__ = [
    # Function exports
    "to_iso8601",
    "to_datetime",
    "to_milliseconds",
    "to_seconds",
]


def to_iso8601(value: dtlib.datetime | str | int | None) -> str | None:
    if not value:
        return None

    value_ms = to_milliseconds(value)
    value = to_datetime(value)

    value_iso8601 = value.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-6] + "{:03d}"
    value_iso8601 = value_iso8601.format(int(value_ms) % 1000) + "Z"

    return value_iso8601


def to_milliseconds(value: str | int | None) -> int | None:
    if not value:
        return None

    if isinstance(value, int) and len(str(value)) >= 12:
        return value

    return to_seconds(value) * 1000


def to_seconds(value: str | int | None) -> float | int | None:
    if not value:
        return None

    if isinstance(value, int) and len(str(value)) >= 12:
        return value / 1000

    return to_datetime(value).timestamp()


def to_datetime(value: str | int | None) -> dtlib.datetime | None:
    """Returns the UTC datetime equivalent of the input value.

    Arguments:
        value: The generic input. This can be a string or an integer.
            If its a datetime string, its just parsed automatically.
            If its a number like string or an actual integer,
            we check if its a Unix timestamp and is convert accordingly.

    Return:
        A datetime object.

    """
    if not value:
        return None

    value = str(value)
    if value.isdigit() and len(value) >= 12:
        datetime = dtlib.datetime.utcfromtimestamp(int(value) / 1000.0)
    else:
        datetime = parser.parse(value)

    return datetime.replace(tzinfo=datetime.tzinfo or pytz.utc)
