# Copyright 2021 drewCo Software, All Rights Reserved
# Some code to help deal with datetimes, in particular, UTC.

from datetime import datetime, timezone

# ----------------------------------------------------------------------------------------------------------------------------
def getAlignedUTCTime():
    """Gets a datetime representing the current day starting at UTC 00:00:00"""
    nowTime = datetime.utcnow()
    res = datetime(nowTime.year, nowTime.month, nowTime.day, 0, 0, 0, 0, tzinfo=timezone.utc)
    return res

# ----------------------------------------------------------------------------------------------------------------------------
def getUTCMin():
    """Get the minimum UTC time."""
    dtMin = datetime.min
    res = datetime(dtMin.year, dtMin.month, dtMin.day, 0, 0, 0, 0, tzinfo=timezone.utc)
    return res

# ----------------------------------------------------------------------------------------------------------------------------
def getUTCTimeFromString(timestamp: str):

    parts = timestamp.split("+")
    offset = "00:00"
    tz = timezone.utc

    if len(parts) > 1:
        offset = parts[1]
        if offset != "00:00":
            raise Exception("This is a nonzero offset.  Since python is a lil' bitch and want to make working with timezones as hard as possible, I am currently not supporting anything that isn't UTC+0!!")        

    dtMin = datetime.fromisoformat(parts[0])
    
    res = datetime(dtMin.year, dtMin.month, dtMin.day, dtMin.hour, dtMin.minute, dtMin.second, dtMin.microsecond, tz)
    return res