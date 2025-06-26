"""
Utility functions for report generation and data processing.
"""

def format_time(minutes):
    """Format minutes to HH:MM format"""
    if minutes <= 0:
        return "00:00"
    
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours:02d}:{mins:02d}"

def extract_numeric_value(text):
    """Extract numeric value from text, preserving decimal points"""
    if not text:
        return 0
    
    try:
        # Remove everything except digits, decimal points and minus sign
        clean_text = ''.join(c for c in str(text) if c.isdigit() or c in '.-')
        return float(clean_text)
    except (ValueError, TypeError):
        return 0

def format_number(number, decimal_places=0):
    """Format number with thousands separator and optional decimal places"""
    try:
        return f"{float(number):,.{decimal_places}f}"
    except (ValueError, TypeError):
        return "0"

def calculate_percentage(part, total):
    """Calculate percentage safely"""
    try:
        if total == 0:
            return 0
        return (part / total) * 100
    except (ZeroDivisionError, TypeError):
        return 0

def is_valid_time(time_str):
    """Validate time string in HH:MM format"""
    if not time_str:
        return False
    
    try:
        parts = time_str.split(':')
        if len(parts) != 2:
            return False
            
        hours, minutes = map(int, parts)
        return 0 <= hours <= 23 and 0 <= minutes <= 59
    except (ValueError, TypeError):
        return False
