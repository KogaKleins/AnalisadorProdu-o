"""
Data handler module.
Funções para carregar e gerenciar os dados da interface.
"""

import pandas as pd
from tkinter import messagebox
import tkinter as tk
from src.interface import globals
import os

# Importações específicas (evita importações totais que forçam o __init__.py)
from core.extractor.file_finder import construir_caminho_pdf
from core.extractor.pdf_extractor import extrair_dados_pdf
from core.config.setup_config import get_setup_time
from core.data.data_processor import process_data, validate_data, calculate_setup_times, extrair_media_producao
from core.data.group_manager import GroupManager
from src.core.metrics.utils import limpar_setup_op_sem_acerto

from .table_handler import configurar_colunas_da_tabela, carregar_dados_na_tabela, aplicar_cores_grupos

# Mapeamento de abreviações para nomes completos de máquinas
MACHINE_ALIASES = {
    'b': 'bobst',
    'bobst': 'bobst',
    'k': 'komori',
    'komori': 'komori',
    'f': 'furnax',
    'furnax': 'furnax',
    'cv': 'cv manual',
    'cv manual': 'cv manual',
    'cv guangya': 'cv_guangya',
    'guangya': 'cv_guangya',
    'guan': 'cv_guangya',
    'cvgy': 'cv_guangya',
    'cv guan': 'cv_guangya',
    'gy': 'cv_guangya',
    'h': 'hcd',
    'hcd': 'hcd',
    's': 'samkoon',
    'samkoon': 'samkoon',
    'l': 'laminadora',
    'laminadora': 'laminadora',
    # Aliases para Sakurai
    'verniz uv sakurai': 'sakurai',
    'verniz.uv sakurai': 'sakurai',
    'verniz sakurai': 'sakurai',
    'uv sakurai': 'sakurai',
    'sakurai': 'sakurai',
    'v': 'sakurai',
    # Outros
    'sbl': 'sbl',
    'sbl': 'sbl',
}

def get_maquina_alias(valor):
    valor = str(valor).strip().lower()
    if valor in MACHINE_ALIASES:
        return MACHINE_ALIASES[valor]
    # Matching por prefixo
    for alias in MACHINE_ALIASES:
        if alias.startswith(valor):
            return MACHINE_ALIASES[alias]
    # Matching por substring (fuzzy leve)
    for alias in MACHINE_ALIASES:
        if valor in alias:
            return MACHINE_ALIASES[alias]
    return valor

def carregar_dados_wrapper():
    """Wrapper para carregar dados a partir dos campos da interface"""
    data = globals.entrada_data.get() if getattr(globals, 'entrada_data', None) is not None else ''
    maquina = globals.entrada_maquina.get() if getattr(globals, 'entrada_maquina', None) is not None else ''
    carregar_dados(data, maquina)

def carregar_dados(data, maquina):
    """Carrega os dados do arquivo PDF"""
    if not data or not maquina:
        messagebox.showwarning("Atenção", "Preencha a data e a máquina.")
        return

    try:
        caminho_pdf = construir_caminho_pdf(data, get_maquina_alias(maquina))
        if not os.path.isfile(caminho_pdf):
            messagebox.showerror("Erro", f"PDF da máquina '{maquina}' não encontrado!\nCaminho: {caminho_pdf}")
            # Limpa dados globais e tabela
            globals.df_global = None
            globals.linhas_agrupadas = {}
            if globals.tabela:
                for item in globals.tabela.get_children():
                    globals.tabela.delete(item)
            if globals.text_resultado:
                globals.text_resultado.delete("1.0", tk.END)
            return
        df = extrair_dados_pdf(caminho_pdf)
        df = process_dataframe(df)
        globals.df_global = df.copy()
        globals.linhas_agrupadas = {}
        if hasattr(globals, 'table_component') and globals.table_component:
            globals.table_component.load_data(globals.df_global)
        # Aplica cores de agrupamento automaticamente
        aplicar_cores_grupos(globals.tabela, {})
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

    # Garante que a coluna 'Máquina' existe e está preenchida
    valor_maquina = get_valor_maquina()
    valor_maquina = valor_maquina.lower() if valor_maquina else ''
    if 'Máquina' not in df.columns:
        df.insert(2, 'Máquina', valor_maquina)  # Insere na posição 2 (após 'Término')
    else:
        df['Máquina'] = df['Máquina'].fillna('').replace('', valor_maquina)
        df['Máquina'] = df['Máquina'].apply(lambda x: valor_maquina if not x or (isinstance(x, str) and x.strip() == '') else (x.lower() if isinstance(x, str) else x))

    # Garante que a coluna 'Tempo Setup' existe e está visível
    if 'Tempo Setup' not in df.columns:
        df.insert(3, 'Tempo Setup', '')  # Insere após 'Máquina'

    # Garante que a coluna 'Média Produção' existe e está visível
    if 'Média Produção' not in df.columns:
        df.insert(4, 'Média Produção', '')  # Insere após 'Tempo Setup'

    df = calculate_setup_times(df)

    # Preenche campos especiais para todas as máquinas (generalizado)
    try:
        modulo = f"src.core.metrics.maquinas.{valor_maquina}"
        func_name = f"preencher_campos_{valor_maquina.replace(' ', '_')}"
        import importlib
        mod = importlib.import_module(modulo)
        if hasattr(mod, func_name):
            df = getattr(mod, func_name)(df)
    except Exception:
        pass

    # Limpa tempo de setup de OPs sem acerto (universal para todas as máquinas)
    df = limpar_setup_op_sem_acerto(df)

    # Reorganiza as colunas para garantir que 'Tempo Setup' e 'Média Produção' fiquem sempre visíveis e lado a lado
    cols = df.columns.tolist()
    if 'Tempo Setup' in cols and 'Média Produção' in cols:
        idx_setup = cols.index('Tempo Setup')
        idx_media = cols.index('Média Produção')
        if idx_media != idx_setup + 1:
            # Remove 'Média Produção' e insere logo após 'Tempo Setup'
            cols.pop(idx_media)
            cols.insert(idx_setup + 1, 'Média Produção')
            df = df[cols]

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

def get_valor_maquina():
    em = getattr(globals, 'entrada_maquina', None)
    get_method = getattr(em, 'get', None)
    if callable(get_method):
        try:
            valor = get_method()
            if valor is not None:
                valor = str(valor).strip().lower()
                return get_maquina_alias(valor)
            else:
                return ''
        except Exception:
            return ''
    elif em:
        valor = str(em).strip().lower() if hasattr(em, 'strip') else str(em).lower()
        return get_maquina_alias(valor)
    return ''
