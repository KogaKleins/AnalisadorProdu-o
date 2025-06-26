"""
Report generation package.
"""

from .generator import ReportGenerator
from . import sections
from . import utils

__all__ = [
    'ReportGenerator',
    'sections',
    'utils'
]
