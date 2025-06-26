"""
Data formatting utilities.
"""

from datetime import datetime

def format_date(date_str):
    """Format date string to standard format"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date.strftime("%d/%m/%Y")
    except:
        return date_str

def format_number(number, decimal_places=0):
    """Format number with thousand separator"""
    try:
        return f"{float(number):,.{decimal_places}f}"
    except:
        return str(number)

def format_time(minutes):
    """Format minutes to hours and minutes"""
    try:
        hours = int(minutes) // 60
        mins = int(minutes) % 60
        return f"{hours}h {mins}min"
    except:
        return str(minutes)
