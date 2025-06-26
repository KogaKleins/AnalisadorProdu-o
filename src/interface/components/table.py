"""
Table component module.
Contains the table view and related components.
"""

import tkinter as tk
from tkinter import ttk
from ..handlers.table_handler import (
    configurar_colunas_da_tabela,
    aplicar_cores_grupos,
    ao_selecionar_linha
)
from ..utils.header_generator import (
    gerar_headers_colunas,
    criar_headers_alfabeticos
)

def create_table_view(parent):
    """Create table view with headers and scrollbars"""
    table = TableComponent(parent)
    return table.frame, table.table

class TableComponent:
    def __init__(self, parent):
        self.parent = parent
        self.create_table_frame()
        self.create_table()
        self.configure_scrollbars()
    
    def create_table_frame(self):
        """Create frames for table structure"""
        # Main frame
        self.frame = tk.Frame(self.parent, bg='#ffffff', relief='sunken', bd=2)
        
        # Container frame
        self.container = tk.Frame(self.frame, bg='#ffffff')
        self.container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Tree frame
        self.frame_tree = tk.Frame(self.container, bg='#ffffff')
        self.frame_tree.pack(fill="both", expand=True, pady=(30, 0))
    
    def create_table(self):
        """Create table with treeview"""
        self.scrollbar_y = ttk.Scrollbar(self.frame_tree, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")
        
        self.scrollbar_x = ttk.Scrollbar(self.frame_tree, orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")
        
        self.table = ttk.Treeview(
            self.frame_tree,
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
            selectmode="extended",
            height=20
        )
        self.table.pack(fill="both", expand=True)
        
        # Configure selection event
        self.table.bind("<<TreeviewSelect>>", ao_selecionar_linha)
    
    def configure_scrollbars(self):
        """Configure scrollbar commands"""
        self.scrollbar_y.config(command=self.table.yview)
        self.scrollbar_x.config(command=self.table.xview)
    
    def update_headers(self, df):
        """Update table headers based on dataframe"""
        if df is not None and not df.empty:
            num_colunas = len(df.columns)
            headers_alfabeticos = gerar_headers_colunas(num_colunas)
            
            # Update alphabetic headers
            if hasattr(self, 'frame_headers'):
                self.frame_headers.destroy()
            self.frame_headers = criar_headers_alfabeticos(
                self.container, headers_alfabeticos, df.columns
            )
            
            # Configure table columns
            configurar_colunas_da_tabela(self.table, headers_alfabeticos, df.columns)
    
    def load_data(self, df):
        """Load data into table"""
        if df is not None and not df.empty:
            # Clear existing items
            for item in self.table.get_children():
                self.table.delete(item)
            
            # Update headers
            self.update_headers(df)
            
            # Insert data
            for index, row in df.iterrows():
                valores = list(row)
                self.table.insert("", "end", values=[index + 1] + valores)
    
    def update_groups(self, linhas_agrupadas):
        """Update group colors"""
        aplicar_cores_grupos(self.table, linhas_agrupadas)
