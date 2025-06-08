from datetime import datetime
import pytz


IST = pytz.timezone('Asia/Kolkata')
UTC = pytz.utc


def ist_to_utc(ist_datetime_str, fmt="%Y-%m-%d %H:%M"):
    val = datetime.strptime(ist_datetime_str, fmt)
    ist_time = IST.localize(val)
    return ist_time.astimezone(UTC)


def utc_to_ist(utc_dt):
    return utc_dt.astimezone(IST)