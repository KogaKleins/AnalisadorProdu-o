# interface/terminal_panel.py

import tkinter as tk
from tkinter import ttk

def criar_terminal_painel(paned_parent):
    """
    Cria painel de terminal redimensionável estilo VS Code
    """
    frame_terminal = tk.LabelFrame(paned_parent, text="📊 Resultado da Análise", font=("Arial", 10, "bold"))
    
    # Container interno para melhor controle de layout
    container = tk.Frame(frame_terminal)
    container.pack(fill="both", expand=True, padx=2, pady=2)
    
    # Text widget com fonte monospace para melhor legibilidade
    text_resultado = tk.Text(container, 
                           height=12,  # Altura inicial menor
                           font=('Consolas', 9) if tk.font.families().__contains__('Consolas') else ('Courier', 9),
                           bg='#2d2d2d',  # Tema escuro estilo terminal
                           fg='#f0f0f0',
                           insertbackground='#ffffff',
                           selectbackground='#404040')
    
    # Scrollbar vertical
    scrollbar_resultado = ttk.Scrollbar(container, orient="vertical", command=text_resultado.yview)
    text_resultado.configure(yscrollcommand=scrollbar_resultado.set)

    # Layout grid para melhor controle
    text_resultado.grid(row=0, column=0, sticky="nsew")
    scrollbar_resultado.grid(row=0, column=1, sticky="ns")
    
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    return frame_terminal, text_resultado