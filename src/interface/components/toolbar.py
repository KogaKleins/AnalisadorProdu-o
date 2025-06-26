"""
Toolbar component module.
Contains the toolbar with input fields and buttons.
"""

import tkinter as tk
from tkinter import ttk
from ..handlers.data_handler import carregar_dados_wrapper
from ..handlers.formatters import (
    ao_digitar_data,
    ao_digitar_hora_inicio,
    ao_digitar_hora_fim
)
from ..handlers.config_handler import abrir_configuracoes

def create_toolbar(parent):
    """Create toolbar with input fields and control buttons"""
    toolbar = ToolbarComponent(parent)
    return toolbar

class ToolbarComponent:
    def __init__(self, parent):
        self.parent = parent
        self.create_data_fields()
        self.create_period_frame()
    
    def create_data_fields(self):
        """Create date and machine input fields"""
        # Date field
        tk.Label(self.parent, text="Data:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5)
        self.entrada_data = tk.Entry(self.parent, width=12)
        self.entrada_data.grid(row=0, column=1, padx=5)
        self.entrada_data.bind("<KeyRelease>", lambda event: ao_digitar_data(self.entrada_data, event))
        self.entrada_data.bind("<Return>", lambda event: carregar_dados_wrapper())
        
        # Machine field
        tk.Label(self.parent, text="Máquina:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5)
        self.entrada_maquina = tk.Entry(self.parent, width=15)
        self.entrada_maquina.grid(row=0, column=3, padx=5)
        self.entrada_maquina.bind("<Return>", lambda event: carregar_dados_wrapper())
        
        # Control buttons
        tk.Button(self.parent, text="📊 Carregar Dados", 
                 command=carregar_dados_wrapper).grid(row=0, column=4, padx=10)
        tk.Button(self.parent, text="⚙ Config Setup",
                 command=abrir_configuracoes).grid(row=0, column=5, padx=5)
    
    def create_period_frame(self):
        """Create work period frame with time inputs"""
        frame_periodo = tk.LabelFrame(self.parent, text="Período de Trabalho", bg='#f5f5f5')
        frame_periodo.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        # Start time
        tk.Label(frame_periodo, text="Início:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entrada_hora_inicio = tk.Entry(frame_periodo, width=8)
        self.entrada_hora_inicio.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_hora_inicio.bind("<KeyRelease>", 
                                    lambda event: ao_digitar_hora_inicio(self.entrada_hora_inicio, event))
        
        # End time
        tk.Label(frame_periodo, text="Fim:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entrada_hora_fim = tk.Entry(frame_periodo, width=8)
        self.entrada_hora_fim.grid(row=0, column=3, padx=5, pady=5)
        self.entrada_hora_fim.bind("<KeyRelease>", 
                                  lambda event: ao_digitar_hora_fim(self.entrada_hora_fim, event))
        
        # Interval
        tk.Label(frame_periodo, text="Intervalo (min):", bg='#f5f5f5').grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.entrada_intervalo = tk.Entry(frame_periodo, width=8)
        self.entrada_intervalo.grid(row=0, column=5, padx=5, pady=5)
        self.entrada_intervalo.insert(0, "60")
