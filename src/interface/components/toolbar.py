"""
Toolbar component module.
Contains the toolbar with input fields and buttons.
"""

import tkinter as tk
from tkinter import ttk
from ..handlers.data_handler import carregar_dados_wrapper, MACHINE_ALIASES
from ..handlers.formatters import (
    ao_digitar_data,
    ao_digitar_hora_inicio,
    ao_digitar_hora_fim,
    ao_sair_hora
)
from ..handlers.config_handler import abrir_configuracoes

def create_toolbar(parent):
    """Create toolbar with input fields and control buttons"""
    toolbar = ToolbarComponent(parent)
    return toolbar

class ToolbarComponent:
    def __init__(self, parent):
        self.parent = parent
        self.entrada_maquina = None
        self.btn_config_setup = None
        self.machine_placeholder = None
        self.create_data_fields()
        self.create_period_frame()
        self.toggle_config_setup()
        self.update_machine_placeholder()
    
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
        self.entrada_maquina.bind("<KeyRelease>", self.update_machine_placeholder)
        self.entrada_maquina.bind("<Right>", self.autocomplete_machine)
        self.entrada_maquina.bind("<Tab>", self.autocomplete_machine)
        # Control buttons
        tk.Button(self.parent, text="📊 Carregar Dados", 
                 command=carregar_dados_wrapper).grid(row=0, column=4, padx=10)
        self.btn_config_setup = tk.Button(self.parent, text="⚙ Config Setup",
                 command=abrir_configuracoes)
        self.btn_config_setup.grid(row=0, column=5, padx=5)
        # Placeholder inteligente (autocomplete) - só crie após o botão
        self.machine_placeholder = tk.Label(self.parent, text="", fg="#bbbbbb", bg="#fff", font=("Arial", 9, "italic"))
        self.machine_placeholder.place(in_=self.entrada_maquina, relx=0, rely=0, x=2, y=1, anchor="nw")
    
    def create_period_frame(self):
        """Create work period frame with time inputs"""
        frame_periodo = tk.LabelFrame(self.parent, text="Período de Trabalho", bg='#f5f5f5')
        frame_periodo.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=5)
        
        # Start time
        tk.Label(frame_periodo, text="Início:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entrada_hora_inicio = tk.Entry(frame_periodo, width=20)
        self.entrada_hora_inicio.grid(row=0, column=1, padx=5, pady=5)
        self.entrada_hora_inicio.bind("<FocusOut>", lambda event: ao_sair_hora(self.entrada_hora_inicio, event))
        
        # End time
        tk.Label(frame_periodo, text="Fim:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entrada_hora_fim = tk.Entry(frame_periodo, width=20)
        self.entrada_hora_fim.grid(row=0, column=3, padx=5, pady=5)
        self.entrada_hora_fim.bind("<FocusOut>", lambda event: ao_sair_hora(self.entrada_hora_fim, event))
        
        # Interval
        tk.Label(frame_periodo, text="Intervalo (min):", bg='#f5f5f5').grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.entrada_intervalo = tk.Entry(frame_periodo, width=8)
        self.entrada_intervalo.grid(row=0, column=5, padx=5, pady=5)
        self.entrada_intervalo.insert(0, "60")

    def toggle_config_setup(self, event=None):
        if not self.entrada_maquina or not self.btn_config_setup:
            return
        valor = self.entrada_maquina.get().strip().lower()
        if valor in ["bobst", "b"]:
            self.btn_config_setup.grid(row=0, column=5, padx=5)
        else:
            self.btn_config_setup.grid_remove()

    def update_machine_placeholder(self, event=None):
        if not self.entrada_maquina or not self.machine_placeholder:
            return
        # Novo autocomplete inteligente: usa todos os aliases
        valor = self.entrada_maquina.get().strip()
        valor_lower = valor.lower()
        sugestao = ""
        # Busca por prefixo em qualquer alias
        for alias, nome_interno in MACHINE_ALIASES.items():
            nome_exibicao = nome_interno.replace('_', ' ').title() if 'cv' in nome_interno else nome_interno.title()
            if alias.startswith(valor_lower) and valor:
                sugestao = nome_exibicao
                break
            if nome_exibicao.lower().startswith(valor_lower) and valor:
                sugestao = nome_exibicao
                break
        if sugestao and valor and sugestao.lower() != valor_lower:
            complemento = sugestao[len(valor):]
            self.machine_placeholder.config(text=valor + complemento, fg="#bbbbbb")
            self.machine_placeholder.place(in_=self.entrada_maquina, relx=0, rely=0, x=2, y=1, anchor="nw")
            self.machine_placeholder.lift()
            self.machine_placeholder.config(text=valor + complemento)
        elif not valor and not self.entrada_maquina.focus_get():
            self.machine_placeholder.config(text="Digite a máquina...", fg="#bbbbbb")
            self.machine_placeholder.lift()
        else:
            self.machine_placeholder.config(text="")
            self.machine_placeholder.lower()
        self.toggle_config_setup()

    def autocomplete_machine(self, event=None):
        if not self.entrada_maquina:
            return
        valor = self.entrada_maquina.get().strip()
        valor_lower = valor.lower()
        sugestao = ""
        for alias, nome_interno in MACHINE_ALIASES.items():
            nome_exibicao = nome_interno.replace('_', ' ').title() if 'cv' in nome_interno else nome_interno.title()
            if alias.startswith(valor_lower) and valor:
                sugestao = nome_exibicao
                break
            if nome_exibicao.lower().startswith(valor_lower) and valor:
                sugestao = nome_exibicao
                break
        if sugestao and valor and sugestao.lower() != valor_lower:
            self.entrada_maquina.delete(0, tk.END)
            self.entrada_maquina.insert(0, sugestao)
            self.update_machine_placeholder()
            self.toggle_config_setup()
            return "break"  # Impede o comportamento padrão da tecla
        self.toggle_config_setup()
        return None
