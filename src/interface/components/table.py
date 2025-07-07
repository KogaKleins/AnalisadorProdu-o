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
        # Estilo visual tipo planilha clássica
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="black",
            bordercolor="black",
            borderwidth=1,
            rowheight=25
        )
        style.configure("Treeview.Heading",
            background="#e0e0e0",
            foreground="black",
            bordercolor="black",
            borderwidth=1,
            font=('Arial', 10, 'bold')
        )
        style.map("Treeview", background=[('selected', '#cce6ff')])
        self.parent = parent
        self.letter_labels = []
        self.df_atual = None
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
        
        # Frame para letras (acima da tabela)
        self.frame_letters = tk.Frame(self.container, bg='#f0f0f0', height=25)
        self.frame_letters.pack(fill="x", pady=(0, 2))
        self.frame_letters.pack_propagate(False)
        
        # Frame da tabela
        self.frame_tree = tk.Frame(self.container, bg='#ffffff')
        self.frame_tree.pack(fill="both", expand=True)
    
    def create_table(self):
        """Create table with treeview"""
        # Scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.frame_tree, orient="vertical")
        self.scrollbar_y.pack(side="right", fill="y")
        
        self.scrollbar_x = ttk.Scrollbar(self.frame_tree, orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")
        
        # Treeview
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
        
        # Configure scrollbars
        self.scrollbar_y.config(command=self.table.yview)
        self.scrollbar_x.config(command=self.table.xview)
    
    def configure_scrollbars(self):
        """Configure scrollbar commands"""
        pass  # Já configurado em create_table
    
    def create_letter_headers(self, num_colunas):
        """Cria os headers alfabéticos"""
        # Limpa headers antigos
        for lbl in self.letter_labels:
            lbl.destroy()
        self.letter_labels = []
        
        # Cria headers alfabéticos
        headers_alfabeticos = criar_headers_alfabeticos(num_colunas)
        
        # Label para coluna '#'
        lbl_hash = tk.Label(
            self.frame_letters, 
            text='#', 
            bg='#e0e0e0', 
            font=('Arial', 9, 'bold'), 
            relief='raised',
            bd=1,
            anchor='center'
        )
        self.letter_labels.append(lbl_hash)
        
        # Labels para as letras das colunas
        for letra in headers_alfabeticos:
            lbl = tk.Label(
                self.frame_letters, 
                text=letra, 
                bg='#e0e0e0', 
                font=('Arial', 9, 'bold'), 
                relief='raised',
                bd=1,
                anchor='center'
            )
            self.letter_labels.append(lbl)
    
    def update_letter_positions(self):
        """Atualiza posições dos labels para alinhar com colunas da tabela"""
        if not self.letter_labels:
            return
        try:
            self.table.update_idletasks()
            self.frame_letters.update_idletasks()
            x_pos = 0
            if len(self.letter_labels) > 0:
                hash_width = self.table.column('#0', option='width')
                self.letter_labels[0].place(x=x_pos, y=0, width=hash_width, height=25)
                x_pos += hash_width
            for i, col in enumerate(self.table['columns']):
                if i + 1 < len(self.letter_labels):
                    col_width = self.table.column(col, option='width')
                    self.letter_labels[i + 1].place(x=x_pos, y=0, width=col_width, height=25)
                    x_pos += col_width
        except Exception:
            self.frame_letters.after(100, self.update_letter_positions)
    
    def update_headers(self, df):
        """Update table headers based on dataframe"""
        self.df_atual = df
        if df is not None and not df.empty:
            colunas = list(df.columns)
            self.table['columns'] = colunas
            self.table.heading('#0', text='#')
            self.table.column('#0', width=50, anchor='center')
            for col in colunas:
                self.table.heading(col, text=col)
                self.table.column(col, width=120, anchor='center')
            self.create_letter_headers(len(colunas))
            self.frame_letters.after(10, self.update_letter_positions)
            self.frame_letters.after(100, self.update_letter_positions)
    
    def load_data(self, df):
        """Load data into table"""
        if df is not None and not df.empty:
            for item in self.table.get_children():
                self.table.delete(item)
            self.update_headers(df)
            for index, row in df.iterrows():
                valores = list(row)
                self.table.insert("", "end", text=str(index + 1), values=valores)
            self.frame_letters.after(50, self.update_letter_positions)
            self.frame_letters.after(200, self.update_letter_positions)
            self.frame_letters.after(500, self.update_letter_positions)
    
    def update_groups(self, linhas_agrupadas):
        """Update group colors"""
        # Em vez de aplicar cores de grupo, deixe todas as linhas com fundo claro
        for item in self.table.get_children():
            self.table.item(item, tags=())
        self.table.tag_configure('clear', background='#f9f9f9')
        for item in self.table.get_children():
            self.table.item(item, tags=('clear',))