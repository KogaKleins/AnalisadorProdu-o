"""
Data handler module.
Funções para carregar e gerenciar os dados da interface.
"""

import pandas as pd
from tkinter import messagebox
import tkinter as tk
from src.interface import globals

# Importações específicas (evita importações totais que forçam o __init__.py)
from core.extractor.file_finder import construir_caminho_pdf
from core.extractor.pdf_extractor import extrair_dados_pdf
from core.config.setup_config import get_setup_time
from core.data.data_processor import process_data, validate_data
from core.data.group_manager import GroupManager

from .table_handler import configurar_colunas_da_tabela, carregar_dados_na_tabela

def carregar_dados_wrapper():
    """Wrapper para carregar dados a partir dos campos da interface"""
    data = globals.entrada_data.get()
    maquina = globals.entrada_maquina.get()
    carregar_dados(data, maquina)

def carregar_dados(data, maquina):
    """Carrega os dados do arquivo PDF"""
    
    if not data or not maquina:
        messagebox.showwarning("Atenção", "Preencha a data e a máquina.")
        return

    try:
        caminho_pdf = construir_caminho_pdf(data, maquina)
        df = extrair_dados_pdf(caminho_pdf)
        
        df = process_dataframe(df)
        
        globals.df_global = df.copy()
        globals.linhas_agrupadas = {}
        
        # Corrigido: passar argumentos corretos
        configurar_colunas_da_tabela(globals.tabela, globals.df_global)
        carregar_dados_na_tabela(globals.tabela, globals.df_global)
        
        if globals.text_resultado:
            globals.text_resultado.delete("1.0", tk.END)
            globals.text_resultado.insert(tk.END, 
                "Dados carregados! Selecione linhas e clique em 'Agrupar' ou 'Calcular Desempenho'")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def process_dataframe(df):
    """Processa o DataFrame após a leitura do PDF"""
    if df.empty:
        return df

    header = list(df.iloc[0])
    df = df[1:].reset_index(drop=True)
    df.columns = header

    if len(df.columns) >= 3:
        df = insert_setup_column(df)

    df = calculate_setup_times(df)
    return df

def insert_setup_column(df):
    """Insere coluna de 'Tempo Setup'"""
    colunas_antigas = df.columns.tolist()
    novas_colunas = colunas_antigas[:2] + ['Tempo Setup'] + colunas_antigas[2:]

    df_novo = pd.DataFrame(index=df.index)
    df_novo[novas_colunas[0]] = df[colunas_antigas[0]]
    df_novo[novas_colunas[1]] = df[colunas_antigas[1]]
    df_novo['Tempo Setup'] = ''

    for i, col_antiga in enumerate(colunas_antigas[2:], start=3):
        df_novo[novas_colunas[i]] = df[col_antiga]

    return df_novo

def calculate_setup_times(df):
    """Calcula os tempos de setup para cada linha"""
    os_anteriores_por_processo = {}

    for idx, row in df.iterrows():
        processo = ""
        for col in df.columns:
            if "processo" in str(col).lower():
                processo = str(row.get(col, ""))
                break

        os_value = ""
        for col in df.columns:
            if col.upper() == "OS" or "os" in str(col).lower():
                os_value = str(row.get(col, ""))
                break

        evento = ""
        for col in df.columns:
            if "evento" in str(col).lower():
                evento = str(row.get(col, "")).strip().lower()
                break

        if processo and evento and evento != "produção":
            eventos_setup = ["acerto", "setup", "ajuste", "troca", "preparação"]
            is_evento_setup = any(termo in evento for termo in eventos_setup)

            if is_evento_setup:
                tipo_processo = processo.lower()
                is_first = tipo_processo not in os_anteriores_por_processo

                tempo_setup = get_setup_time(processo, is_first)
                df.at[idx, 'Tempo Setup'] = f"{tempo_setup//60}:{tempo_setup%60:02d}"
            else:
                df.at[idx, 'Tempo Setup'] = ""
        else:
            df.at[idx, 'Tempo Setup'] = ""

        if processo and os_value and os_value != "0" and os_value.strip():
            tipo_processo = processo.lower()
            os_anteriores_por_processo[tipo_processo] = os_value

    return df
