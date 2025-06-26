"""
Terminal component module.
Contains the terminal panel for displaying analysis results.
"""

import tkinter as tk
from tkinter import ttk

def create_terminal_panel(parent):
    """Create resizable terminal panel VS Code style"""
    terminal = TerminalComponent(parent)
    return terminal.frame, terminal.text_widget

class TerminalComponent:
    def __init__(self, parent):
        self.parent = parent
        self.create_panel()
    
    def create_panel(self):
        """Create terminal panel with text widget"""
        # Create main frame
        self.frame = tk.LabelFrame(
            self.parent,
            text="📊 Resultado da Análise",
            font=("Arial", 10, "bold")
        )
        
        # Internal container for better layout control
        self.container = tk.Frame(self.frame)
        self.container.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Text widget with monospace font
        self.text_widget = tk.Text(
            self.container,
            height=12,
            font=('Consolas', 9) if tk.font.families().__contains__('Consolas')
            else ('Courier', 9),
            bg='#2d2d2d',  # Dark theme style
            fg='#f0f0f0',
            insertbackground='#ffffff',
            selectbackground='#404040'
        )
        
        # Vertical scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.container,
            orient="vertical",
            command=self.text_widget.yview
        )
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)
        
        # Grid layout for better control
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
    def clear(self):
        """Clear terminal content"""
        self.text_widget.delete("1.0", tk.END)
    
    def write(self, text):
        """Write text to terminal"""
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)
    
    def write_error(self, text):
        """Write error message to terminal"""
        self.text_widget.insert(tk.END, f"❌ ERRO: {text}\n", "error")
        self.text_widget.see(tk.END)
    
    def write_success(self, text):
        """Write success message to terminal"""
        self.text_widget.insert(tk.END, f"✅ {text}\n", "success")
        self.text_widget.see(tk.END)
