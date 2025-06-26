"""
Interface package.
Contains all interface-related components and functionality.
"""

from .components.main_window import MainWindow
from .components.toolbar import create_toolbar
from .components.table import create_table_view
from .components.terminal import create_terminal_panel
from .handlers.data_handler import carregar_dados_wrapper
from .handlers.event_handler import handle_event
from .handlers.group_handler import handle_group_action
from .utils.formatters import format_date, format_number, format_time
