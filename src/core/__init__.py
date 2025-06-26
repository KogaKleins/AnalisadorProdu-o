"""Core functionality package."""

__version__ = "1.0.0"

from .config.setup_config import get_setup_time
from .data.group_manager import GroupManager
from .data.data_processor import process_data, validate_data
