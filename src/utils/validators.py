"""
General validation utilities.
"""

from datetime import datetime
import re

def validate_date(date_str):
    """Validate date string format"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """Validate time string format (HH:MM)"""
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def validate_number(value):
    """Validate if string can be converted to number"""
    try:
        float(value)
        return True
    except ValueError:
        return False

def validate_path(path):
    """Validate if path is valid"""
    import os
    try:
        return os.path.exists(os.path.dirname(path))
    except:
        return False
