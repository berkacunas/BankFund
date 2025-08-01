from datetime import datetime
import julian

from globals.globals import DEFAULT_DATETIME_FORMAT, DEFAULT_JULIAN_FORMAT

def is_valid_dt_format(datetime_str, format=DEFAULT_DATETIME_FORMAT) -> bool:
    
    valid = True
    try:
        valid = bool(datetime.datetime.strptime(datetime_str, format))
    except ValueError:
        valid = False
        
    return valid

def to_julian(dt) -> float:
    
    return julian.to_jd(dt, fmt=DEFAULT_JULIAN_FORMAT)

def from_julian(jul, format=DEFAULT_JULIAN_FORMAT) -> datetime:
    '''Format jd or mjd'''
    return julian.from_jd(jul, fmt=format)

def is_julian(jul, format=DEFAULT_JULIAN_FORMAT) -> bool:

    try:
        dt = from_julian(jul, format)
    except:
        return False
    
    return isinstance(dt, datetime.datetime)

def is_weekday(dt: datetime) -> bool:
    
    return dt.weekday() < 5

def is_weekend(dt: datetime) -> bool:
    
    return not is_weekday(dt)
