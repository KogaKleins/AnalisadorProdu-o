"""
Event handler module.
Contains functions for handling various GUI events.
"""

import tkinter as tk
from .data_handler import carregar_dados_wrapper
from .group_handler import (
    agrupar_selecionadas_melhorado,
    desagrupar_selecionadas_melhorado
)
from src.interface import globals

def importar_e_chamar_calcular_desempenho():
    from data.performance_calculator import calcular_desempenho
    return calcular_desempenho()

def handle_event(event_type, **kwargs):
    """
    Generic event handler that dispatches events to appropriate handlers.
    
    Args:
        event_type (str): Type of event to handle
        **kwargs: Additional keyword arguments specific to the event
    """
    handlers = {
        'table_select': handle_table_selection,
        'agrupar': lambda: agrupar_selecionadas_melhorado(),
        'desagrupar': lambda: desagrupar_selecionadas_melhorado(),
        'carregar': lambda: carregar_dados_wrapper(),
        'calcular': lambda: importar_e_chamar_calcular_desempenho()
    }
    
    if event_type in handlers:
        return handlers[event_type](**kwargs)
    else:
        raise ValueError(f"Evento desconhecido: {event_type}")

def register_events(window):
    """Register event handlers for the main window"""
    # Table selection event
    window.table.bind("<<TreeviewSelect>>", handle_table_selection)
    
    # Key bindings
    window.window.bind("<Control-a>", lambda e: agrupar_selecionadas_melhorado())
    window.window.bind("<Control-d>", lambda e: desagrupar_selecionadas_melhorado())
    window.window.bind("<F5>", lambda e: carregar_dados_wrapper())
    window.window.bind("<F8>", lambda e: importar_e_chamar_calcular_desempenho())

def handle_table_selection(event=None):
    """Handle table row selection"""
    if globals.tabela is not None:
        item = globals.tabela.selection()
        globals.linhas_selecionadas.clear()
        globals.linhas_selecionadas.extend(globals.tabela.index(i) for i in item)
        
        if globals.label_selecao:
            if globals.linhas_selecionadas:
                text = f"{len(globals.linhas_selecionadas)} linha(s) selecionada(s)"
            else:
                text = "Nenhuma linha selecionada"
            globals.label_selecao.config(text=text)

def handle_data_load():
    """Handle data loading from file"""
    if globals.df_global is None or globals.df_global.empty:
        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, "❌ ERRO: Nenhum dado carregado.")
        return False
    return True

def handle_error(error_message):
    """Handle and display error messages"""
    if globals.text_resultado:
        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, f"❌ ERRO: {error_message}")

def handle_success(success_message):
    """Handle and display success messages"""
    if globals.text_resultado:
        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, f"✅ {success_message}")

def handle_data_validation():
    """Validate required data before processing"""
    hora_inicio = globals.entrada_hora_inicio.get()
    hora_fim = globals.entrada_hora_fim.get()
    
    if not hora_inicio or not hora_fim:
        handle_error("Preencha os horários de início e fim.")
        return False
    
    return True
