"""
date_utils.py

Utility for generating ISO 8601 timestamps (with colon-separated timezone
offset) for the Auckland timezone, including relative dates via a flexible
y/m/d token syntax (e.g. {date_minus_3m}, {date_plus_1y2m}, {date_minus_10d}).

Designed to plug into payload_resolver.py's {placeholder} substitution pattern.
"""

import re
from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil.relativedelta import relativedelta  # pip install python-dateutil

from utils.helpers.dynamic_tokens import register_token

DEFAULT_TZ = "Pacific/Auckland"

# Matches tokens like: date_now, date_minus_3m, date_plus_1y2m10d,
# date_only_minus_6m, date_only_now
TOKEN_PATTERN = re.compile(
    r"^date(?P<only>_only)?_(?:now|(?P<sign>plus|minus)_(?P<spec>(?:\d+[ymd])+))$"
)

# Matches individual y/m/d components within a spec string, e.g. "1y2m10d"
COMPONENT_PATTERN = re.compile(r"(\d+)([ymd])")


def _apply_offset(dt: datetime, sign: str, spec: str) -> datetime:
    """
    Apply a combination of year/month/day offsets to a datetime.
    spec examples: "3m", "1y", "1y2m10d", "10d"
    """
    years = months = days = 0
    for amount, unit in COMPONENT_PATTERN.findall(spec):
        amount = int(amount)
        if unit == "y":
            years += amount
        elif unit == "m":
            months += amount
        elif unit == "d":
            days += amount

    if sign == "minus":
        years, months, days = -years, -months, -days

    return dt + relativedelta(years=years, months=months, days=days)


def get_iso_datetime(sign: str = None, spec: str = None, tz: str = DEFAULT_TZ) -> str:
    """
    Return current (or offset) datetime as ISO 8601 string with colon-separated
    UTC offset, e.g. 2026-08-24T14:35:02+12:00

    Args:
        sign: "plus" or "minus" (None/omitted means no offset, i.e. now)
        spec: combination string like "3m", "1y2m", "10d" (required if sign given)
        tz: IANA timezone name (default: Pacific/Auckland)
    """
    dt = datetime.now(ZoneInfo(tz))

    if sign and spec:
        dt = _apply_offset(dt, sign, spec)

    formatted = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Insert colon into offset: +1200 -> +12:00
    return formatted[:-2] + ":" + formatted[-2:]


def get_date_only(sign: str = None, spec: str = None, tz: str = DEFAULT_TZ) -> str:
    """
    Return just the date portion (no time/offset), e.g. 2026-08-24
    """
    dt = datetime.now(ZoneInfo(tz))
    if sign and spec:
        dt = _apply_offset(dt, sign, spec)
    return dt.strftime("%Y-%m-%d")

@register_token("resolve_date_token")
def resolve_date_token(token: str="date_now") -> str | None:
    """
    Given a token name (without braces), return its resolved date string,
    or None if it's not a recognised date token.

    Supported forms:
        date_now                  -> current timestamp
        date_minus_3m             -> 3 months ago
        date_plus_1y              -> 1 year from now
        date_minus_1y2m10d        -> 1 year, 2 months, 10 days ago (combinable)
        date_only_now             -> current date, no time/offset
        date_only_minus_6m        -> date only, 6 months ago
    """
    match = TOKEN_PATTERN.match(token)
    if not match:
        return None

    only = bool(match.group("only"))
    sign = match.group("sign")
    spec = match.group("spec")

    if only:
        return get_date_only(sign, spec)
    return get_iso_datetime(sign, spec)


if __name__ == "__main__":
    # Quick manual check
    for t in [
        "date_now",
        "date_minus_3m",
        "date_minus_6m",
        "date_plus_1y",
        "date_minus_1y2m10d",
        "date_only_now",
        "date_only_minus_6m",
        "date_not_a_token",
    ]:
        print(f"{t:25s} -> {resolve_date_token(t)}")
