"""
General utility functions module.
"""

import re
from datetime import datetime, timedelta

def format_time(minutes):
    """Format minutes to HH:MM format"""
    if not minutes or minutes <= 0:
        return "00:00"
    
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"

def parse_time(time_str):
    """Parse time string to minutes"""
    if not time_str:
        return 0
        
    try:
        # Handle HH:MM format
        if ':' in time_str:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        
        # Handle numeric minutes
        return int(float(time_str))
    except (ValueError, TypeError):
        return 0

def calculate_time_difference(start_time, end_time):
    """Calculate time difference in minutes"""
    if not start_time or not end_time:
        return 0
        
    try:
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")
        
        diff = end - start
        if diff.days < 0:  # Handle overnight times
            end += timedelta(days=1)
            diff = end - start
            
        return diff.seconds // 60
    except ValueError:
        return 0

def format_large_number(number):
    """Format large numbers with thousands separator"""
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        return "0"

def extract_numeric(text):
    """Extract numeric value from text"""
    if not text:
        return 0
        
    try:
        # Remove everything except digits, decimal point and minus sign
        clean = ''.join(c for c in str(text) if c.isdigit() or c in '.-')
        return float(clean)
    except (ValueError, TypeError):
        return 0

def calculate_percentage(part, total):
    """Calculate percentage safely"""
    try:
        if not total:
            return 0
        return (part / total) * 100
    except (ZeroDivisionError, TypeError):
        return 0

def format_percentage(value, decimal_places=1):
    """Format percentage value"""
    try:
        return f"{float(value):.{decimal_places}f}%"
    except (ValueError, TypeError):
        return "0.0%"

def is_valid_date(date_str):
    """Validate date string in DD/MM/YYYY format"""
    if not date_str:
        return False
        
    try:
        day, month, year = map(int, date_str.split('/'))
        datetime(year, month, day)
        return True
    except (ValueError, TypeError):
        return False

def normalize_text(text):
    """Normalize text removing accents and special characters"""
    if not text:
        return ""
        
    # Remove accents and special characters
    normalized = text.lower()
    normalized = re.sub(r'[àáâãä]', 'a', normalized)
    normalized = re.sub(r'[èéêë]', 'e', normalized)
    normalized = re.sub(r'[ìíîï]', 'i', normalized)
    normalized = re.sub(r'[òóôõö]', 'o', normalized)
    normalized = re.sub(r'[ùúûü]', 'u', normalized)
    normalized = re.sub(r'[ýÿ]', 'y', normalized)
    normalized = re.sub(r'[ñ]', 'n', normalized)
    normalized = re.sub(r'[çc]', 'c', normalized)
    
    # Remove other special characters
    normalized = re.sub(r'[^a-z0-9\s]', '', normalized)
    
    return normalized.strip()
