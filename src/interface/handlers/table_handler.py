"""
Table handling module.
Contains functions for managing table data and display.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from ..utils.header_generator import gerar_headers_colunas
from src.interface import globals

def configurar_tabela(treeview, colunas):
    """Configure table columns and headers"""
    # Remove existing columns
    for col in treeview['columns']:
        treeview.delete(col)
        
    # Configure new columns
    treeview['columns'] = colunas
    treeview.column('#0', width=0, stretch=tk.NO)
    
    for col in colunas:
        treeview.column(col, anchor=tk.CENTER, width=100)
        treeview.heading(col, text=col, anchor=tk.CENTER)

def carregar_dados_na_tabela(treeview, dados):
    """Load data into table"""
    # Clear existing items
    for item in treeview.get_children():
        treeview.delete(item)
        
    # Insert new data
    for idx, row in dados.iterrows():
        values = [row[col] for col in treeview['columns']]
        treeview.insert('', tk.END, values=values)

def atualizar_selecao(treeview, indices_selecionados):
    """Update table selection"""
    treeview.selection_set(indices_selecionados)

def configurar_colunas_da_tabela(tabela, df=None):
    """
    Configura as colunas da tabela baseado no DataFrame ou em headers padrão.
    
    Args:
        tabela (ttk.Treeview): A tabela para configurar
        df (pd.DataFrame, optional): DataFrame com os dados. Se None, usa headers padrão.
    """
    # Remove colunas existentes
    tabela.delete(*tabela.get_children())
    
    # Configura coluna #0 (índice) para não aparecer
    tabela.column("#0", width=0, stretch=tk.NO)
    tabela.heading("#0", text="", anchor=tk.W)
    
    # Gera headers para as colunas
    if df is not None:
        colunas = list(df.columns)
    else:
        colunas = gerar_headers_colunas()
    
    # Configura as colunas
    tabela["columns"] = colunas
    
    # Configurações específicas para cada coluna
    larguras = {
        "Data": 100,
        "Hora": 80,
        "Máquina": 100,
        "Evento": 200,
        "Quantidade": 100,
        "Status": 100,
        "Grupo": 100,
        "Observações": 200
    }
    
    alinhamentos = {
        "Data": tk.CENTER,
        "Hora": tk.CENTER,
        "Máquina": tk.CENTER,
        "Evento": tk.W,
        "Quantidade": tk.RIGHT,
        "Status": tk.CENTER,
        "Grupo": tk.CENTER,
        "Observações": tk.W
    }
    
    # Aplica as configurações
    for coluna in colunas:
        largura = larguras.get(coluna, 100)  # Largura padrão de 100 se não especificado
        alinhamento = alinhamentos.get(coluna, tk.CENTER)  # Alinhamento central como padrão
        
        tabela.column(coluna, width=largura, anchor=alinhamento)
        tabela.heading(coluna, text=coluna, anchor=tk.CENTER)

def aplicar_cores_grupos(tabela, grupos):
    """
    Aplica cores diferentes para cada grupo na tabela.
    
    Args:
        tabela (ttk.Treeview): A tabela para aplicar as cores
        grupos (dict): Dicionário com os grupos e seus índices
    """
    cores = ['#FFD700', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C',
             '#E6E6FA', '#FFA07A', '#20B2AA', '#FF69B4', '#BDB76B']
    
    # Aplica novas cores
    for i, (grupo, indices) in enumerate(grupos.items()):
        cor = cores[i % len(cores)]  # Cicla pelas cores se houver mais grupos que cores
        tag = f'grupo_{i}'
        tabela.tag_configure(tag, background=cor)
        
        # Aplica a cor às linhas do grupo
        for idx in indices:
            item_id = tabela.get_children()[idx]
            tabela.item(item_id, tags=(tag,))

def ao_selecionar_linha(event):
    """
    Manipula o evento de seleção de linha na tabela.
    
    Args:
        event: Evento de seleção da tabela
    """
    tabela = event.widget
    selecionadas = tabela.selection()
    
    if not selecionadas:
        return
        
    # Atualiza linhas selecionadas nos globals
    globals.linhas_selecionadas = [tabela.index(item) for item in selecionadas]

def editar_celula(event, treeview):
    """
    Habilita a edição de uma célula após duplo clique
    """
    try:
        # Identifica o item e coluna clicados
        item = treeview.identify('item', event.x, event.y)
        column = treeview.identify('column', event.x, event.y)
        
        if not item or not column:  # clique fora de item/coluna válido
            return
            
        # Pega o índice da coluna (remove o #)
        column_index = treeview['columns'].index(treeview['columns'][int(column[1]) - 1])
        
        # Cria uma entry para edição
        bbox = treeview.bbox(item, column)
        if not bbox:  # célula não visível
            return
            
        # Recupera o valor atual
        valor_atual = treeview.item(item)['values'][column_index]
        
        # Cria e posiciona o entry
        entry = tk.Entry(treeview)
        entry.insert(0, valor_atual)
        entry.select_range(0, tk.END)
        
        def salvar_edicao(event=None):
            """Salva o valor editado na tabela"""
            novo_valor = entry.get()
            valores = list(treeview.item(item)['values'])
            valores[column_index] = novo_valor
            treeview.item(item, values=valores)
            entry.destroy()
            atualizar_dataframe_global()
            
        def cancelar_edicao(event=None):
            """Cancela a edição"""
            entry.destroy()
            
        entry.bind('<Return>', salvar_edicao)
        entry.bind('<Escape>', cancelar_edicao)
        entry.bind('<FocusOut>', salvar_edicao)
        
        # Posiciona o entry sobre a célula
        x, y, width, height = bbox
        entry.place(x=x, y=y, width=width, height=height)
        entry.focus_set()
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao editar célula: {str(e)}")
        if 'entry' in locals():
            entry.destroy()

# --- AVISO: Funções de sincronização, inserção e edição de setup/velocidade desabilitadas para evitar conflito ---
# Utilize apenas a lógica de interface/table_manager.py para manipulação de Tempo Setup e Velocidade.

def inserir_linha(tabela):
    pass
def deletar_linha(tabela):
    pass
def atualizar_dataframe_global():
    pass
def importar_dados():
    pass

def exportar_dados():
    """Exporta os dados para CSV ou Excel"""
    df_global = globals.df_global
    if df_global is None or df_global.empty:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return
    
    try:
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*")]
        )
        
        if not arquivo:
            return  # Usuário cancelou a operação
        
        # Pergunta ao usuário qual formato deseja salvar
        resposta = messagebox.askquestion(
            "Escolher formato",
            "Deseja salvar como CSV (sim) ou Excel (não)?",
            icon='question'
        )
        
        if resposta == 'yes':
            # Salvar como CSV
            df_global.to_csv(arquivo, index=False, sep=';')
            messagebox.showinfo("Sucesso", "Dados exportados para CSV com sucesso.")
        else:
            # Salvar como Excel
            df_global.to_excel(arquivo, index=False)
            messagebox.showinfo("Sucesso", "Dados exportados para Excel com sucesso.")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")
