"""
Table handling module.
Contains functions for managing table data and display.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from ..utils.header_generator import gerar_headers_colunas
from src.interface import globals
import unidecode
import re
from src.core.metrics.utils import formatar_quantidade, parse_quantidade, formatar_tempo, parse_tempo

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
        values = [row.get(col, '') for col in treeview['columns']]
        treeview.insert('', tk.END, values=values)
    aplicar_cores_por_processo(treeview)

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
        "Observações": 200,
        "Média Produção": 120
    }
    
    alinhamentos = {
        "Data": tk.CENTER,
        "Hora": tk.CENTER,
        "Máquina": tk.CENTER,
        "Evento": tk.W,
        "Quantidade": tk.RIGHT,
        "Status": tk.CENTER,
        "Grupo": tk.CENTER,
        "Observações": tk.W,
        "Média Produção": tk.CENTER
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

def formatar_tempo(valor):
    # Aceita formatos como 100, 0100, 59, 1:00, 01:00 e converte para HH:MM
    valor = str(valor).strip()
    if ':' in valor:
        partes = valor.split(':')
        if len(partes) == 2:
            h, m = partes
            try:
                h = int(h)
                m = int(m)
                # Ajusta minutos para nunca passar de 59
                h += m // 60
                m = m % 60
                return f"{h:02d}:{m:02d}"
            except Exception:
                return valor
    valor_num = re.sub(r'\D', '', valor)
    if valor_num == '':
        return '00:00'
    if len(valor_num) <= 2:
        return f"00:{int(valor_num):02d}"
    if len(valor_num) == 3:
        h = int(valor_num[0])
        m = int(valor_num[1:])
        h += m // 60
        m = m % 60
        return f"0{h}:{m:02d}"
    if len(valor_num) >= 4:
        h = int(valor_num[:-2])
        m = int(valor_num[-2:])
        h += m // 60
        m = m % 60
        return f"{h:02d}:{m:02d}"
    return valor

def formatar_tempo_para_minutos(valor):
    # Converte HH:MM ou formatos burros para minutos inteiros
    valor = str(valor).strip()
    if ':' in valor:
        partes = valor.split(':')
        if len(partes) == 2:
            try:
                h = int(partes[0])
                m = int(partes[1])
                return h * 60 + m
            except Exception:
                return 0
    valor_num = re.sub(r'\D', '', valor)
    if valor_num == '':
        return 0
    if len(valor_num) <= 2:
        return int(valor_num)
    if len(valor_num) == 3:
        return int(valor_num[0]) * 60 + int(valor_num[1:])
    if len(valor_num) >= 4:
        return int(valor_num[:-2]) * 60 + int(valor_num[-2:])
    return 0

def editar_celula(event, treeview):
    """
    Habilita a edição de uma célula após duplo clique
    """
    try:
        if not treeview or not treeview.winfo_exists():
            return
        item = treeview.identify('item', event.x, event.y)
        column = treeview.identify('column', event.x, event.y)
        if not item or not column:
            return
        try:
            column_index = int(column.replace('#', '')) - 1
        except Exception:
            column_index = 0
        bbox = treeview.bbox(item, column)
        if not bbox:
            return
        valores_item = treeview.item(item)['values']
        if column_index < 0 or column_index >= len(valores_item):
            valor_atual = ''
        else:
            valor_atual = valores_item[column_index]
        entry = tk.Entry(treeview)
        entry.insert(0, valor_atual)
        entry.select_range(0, tk.END)
        def salvar_edicao(event=None):
            novo_valor = entry.get()
            colunas = list(map(str, treeview['columns']))
            col_nome = colunas[column_index] if column_index < len(colunas) else ''
            col_norm = unidecode.unidecode(col_nome).lower()
            # Se for coluna de tempo, normaliza e atualiza campo auxiliar em minutos
            if 'tempo' in col_norm:
                # Normaliza entradas de tempo para HH:MM
                temp = novo_valor.strip()
                temp_num = re.sub(r'\D', '', temp)
                
                if len(temp_num) == 3:
                    # 3 dígitos: interpretar como HMM (ex: 200 = 2:00, 180 = 1:80 -> 2:20)
                    h = int(temp_num[0])
                    m = int(temp_num[1:])
                    # Ajusta se minutos > 59
                    h += m // 60
                    m = m % 60
                    temp = f"0{h}:{m:02d}"
                elif len(temp_num) == 4:
                    # 4 dígitos: interpretar como HHMM (ex: 0200 = 02:00, 1430 = 14:30)
                    h = int(temp_num[:2])
                    m = int(temp_num[2:])
                    # Ajusta se minutos > 59
                    h += m // 60
                    m = m % 60
                    temp = f"{h:02d}:{m:02d}"
                elif len(temp_num) <= 2 and temp_num:
                    # 1 ou 2 dígitos: interpretar como minutos (ex: 40 = 00:40, 80 = 01:20)
                    minutos = int(temp_num)
                    h = minutos // 60
                    m = minutos % 60
                    temp = f"{h:02d}:{m:02d}"
                elif ':' in temp:
                    # Já está no formato HH:MM, apenas valida
                    partes = temp.split(':')
                    if len(partes) == 2:
                        try:
                            h = int(partes[0])
                            m = int(partes[1])
                            # Ajusta se minutos > 59
                            h += m // 60
                            m = m % 60
                            temp = f"{h:02d}:{m:02d}"
                        except:
                            pass
                
                novo_valor = temp
                # Atualiza campo auxiliar 'Tempo (min)' se existir
                try:
                    tempo_min = formatar_tempo_para_minutos(novo_valor)
                    idx_tempo_min = None
                    for idx, c in enumerate(colunas):
                        if 'tempo (min' in unidecode.unidecode(c).lower():
                            idx_tempo_min = idx
                            break
                    valores = list(treeview.item(item)['values'])
                    if idx_tempo_min is not None and idx_tempo_min < len(valores):
                        valores[idx_tempo_min] = tempo_min
                        treeview.item(item, values=valores)
                except Exception:
                    pass
            # Se for coluna de quantidade, formata para milhar
            if 'qtd' in col_norm:
                novo_valor = formatar_quantidade(novo_valor)
            # Só salva se mudou
            if str(novo_valor) != str(valor_atual):
                valores = list(treeview.item(item)['values'])
                colunas = list(map(str, treeview['columns']))
                if column_index >= 0 and column_index < len(valores):
                    # Quantidade: salva como número no DataFrame, exibe formatado na tabela
                    if 'qtd' in col_norm:
                        try:
                            num_val = parse_quantidade(novo_valor)
                            valores[column_index] = formatar_quantidade(num_val)
                            if globals.df_global is not None:
                                globals.df_global.at[treeview.index(item), colunas[column_index]] = num_val
                        except Exception:
                            valores[column_index] = novo_valor
                    # Tempo: salva como minutos no DataFrame, exibe HH:MM na tabela
                    elif 'tempo' in col_norm:
                        try:
                            minutos = parse_tempo(novo_valor)
                            valores[column_index] = formatar_tempo(minutos)
                            if globals.df_global is not None:
                                globals.df_global.at[treeview.index(item), colunas[column_index]] = minutos
                        except Exception:
                            valores[column_index] = novo_valor
                    else:
                        valores[column_index] = novo_valor
                        if globals.df_global is not None:
                            globals.df_global.at[treeview.index(item), colunas[column_index]] = novo_valor
                    treeview.item(item, values=valores)
                atualizar_dataframe_global()
            entry.destroy()
        def cancelar_edicao(event=None):
            entry.destroy()
        entry.bind('<Return>', salvar_edicao)
        entry.bind('<Escape>', cancelar_edicao)
        entry.bind('<FocusOut>', salvar_edicao)
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
    selecionadas = tabela.selection()
    if selecionadas:
        idx = tabela.index(selecionadas[0])
    else:
        idx = 0
    colunas = list(map(str, tabela['columns']))
    nova_linha = ['' for _ in colunas]
    tabela.insert('', idx, values=nova_linha)
    df = globals.df_global.copy() if globals.df_global is not None else pd.DataFrame(columns=colunas)
    nova_df = pd.DataFrame([['' for _ in colunas]], columns=colunas)
    df1 = df.iloc[:idx] if idx > 0 else pd.DataFrame(columns=colunas)
    df2 = df.iloc[idx:] if idx < len(df) else pd.DataFrame(columns=colunas)
    globals.df_global = pd.concat([df1, nova_df, df2], ignore_index=True)
    for item in tabela.get_children():
        tabela.delete(item)
    if isinstance(globals.df_global, pd.DataFrame):
        for i, row in globals.df_global.iterrows():
            tabela.insert('', 'end', values=list(row))

def deletar_linha(tabela):
    selecionadas = tabela.selection()
    if not selecionadas:
        return
    indices = [tabela.index(item) for item in selecionadas]
    if globals.df_global is not None and isinstance(globals.df_global, pd.DataFrame):
        globals.df_global = globals.df_global.drop(indices).reset_index(drop=True)
    for item in selecionadas:
        tabela.delete(item)
    # Corrigir: garantir que get_children retorna lista
    all_items = list(tabela.get_children())
    tabela.delete(*all_items)
    if globals.df_global is not None and isinstance(globals.df_global, pd.DataFrame):
        for i, row in globals.df_global.iterrows():
            tabela.insert('', 'end', values=list(row))

def atualizar_dataframe_global():
    """
    Sincroniza o DataFrame global com os dados atuais da tabela.
    Converte e valida valores numéricos nas colunas de quantidade e tempo.
    """
    tabela = globals.tabela
    if tabela is None or not tabela.winfo_exists():
        return
    try:
        raw_cols = list(map(str, tabela['columns']))
        colunas = [str(c) for c in raw_cols if isinstance(c, str) or isinstance(c, int)]
    except Exception:
        colunas = []
    dados = []
    for item in tabela.get_children():
        valores = list(tabela.item(item)['values'])
        for i, col in enumerate(colunas):
            col_norm = unidecode.unidecode(col).lower()
            if 'qtd' in col_norm:
                valores[i] = parse_quantidade(valores[i])
            elif 'tempo' in col_norm:
                valores[i] = parse_tempo(valores[i])
        if len(valores) == len(colunas):
            dados.append(valores)
    # Garante que a coluna 'Tempo (min)' existe
    if not any('tempo (min' in unidecode.unidecode(c).lower() for c in colunas):
        colunas.append('Tempo (min)')
        for row in dados:
            row.append('')
    # Atualiza o campo 'Tempo (min)' para cada linha
    idx_tempo = None
    idx_tempo_min = None
    for i, c in enumerate(colunas):
        if 'tempo' in unidecode.unidecode(c).lower() and '(min' not in unidecode.unidecode(c).lower():
            idx_tempo = i
        if 'tempo (min' in unidecode.unidecode(c).lower():
            idx_tempo_min = i
    if idx_tempo is not None and idx_tempo_min is not None:
        for row in dados:
            tempo_str = row[idx_tempo] if idx_tempo < len(row) else ''
            row[idx_tempo_min] = parse_tempo(tempo_str)
    # Adiciona linha de totais ao final (somente para linhas de produção/OPs válidas)
    if dados and colunas:
        totais = ['' for _ in colunas]
        # Identifica índices das colunas de quantidade
        idxs_qtd = [i for i, col in enumerate(colunas) if 'qtd' in unidecode.unidecode(col).lower()]
        # Filtra apenas linhas de produção (Evento contém 'produção')
        linhas_validas = []
        idx_evento = None
        for i, col in enumerate(colunas):
            if unidecode.unidecode(col).lower().startswith('evento'):
                idx_evento = i
                break
        for row in dados:
            if idx_evento is not None and idx_evento < len(row):
                evento = str(row[idx_evento]).lower()
                if 'producao' in unidecode.unidecode(evento):
                    linhas_validas.append(row)
        for i in idxs_qtd:
            try:
                total_num = sum(row[i] for row in linhas_validas if isinstance(row[i], (int, float)))
                totais[i] = formatar_quantidade(total_num)
            except Exception:
                totais[i] = ''
        if len(totais) > 0:
            totais[0] = 'TOTAL'
        if dados and str(dados[-1][0]).strip().upper() == 'TOTAL':
            dados = dados[:-1]
        dados.append(totais)
    # Padroniza colunas para lista de strings simples
    if hasattr(colunas, 'get'):
        colunas = list(colunas.get())
    else:
        colunas = list(colunas)
    colunas = [str(c) for c in colunas]
    if dados and isinstance(colunas, list) and all(isinstance(c, str) for c in colunas):
        import pandas as pd
        try:
            df = pd.DataFrame(data=dados, columns=colunas)
            if not df.empty:
                globals.df_global = df
        except Exception:
            df = pd.DataFrame(data=dados)
            if not df.empty:
                globals.df_global = df

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

def aplicar_cores_por_processo(tabela):
    cores = ['#FFFACD', '#E0FFFF', '#FFDAB9', '#E6E6FA', '#F0E68C', '#D8BFD8', '#B0E0E6', '#FFB6C1', '#98FB98', '#F5DEB3']
    padrao_entrada = re.compile(r'(\b\d*\s*[ªa]?\s*entrada\b|acerto)', re.IGNORECASE)
    idx_cor = 0
    cor_atual = None
    bloco_tag = None
    op_anterior = None
    bloco_idx = 0
    # Identifica índices das colunas OP/OS e Processo
    colunas = list(map(str, tabela['columns']))
    idx_op = None
    idx_proc = None
    for i, c in enumerate(colunas):
        c_norm = unidecode.unidecode(str(c)).lower().replace(' ', '')
        if any(x in c_norm for x in ['op', 'os', 'ordem']):
            idx_op = i
        if 'processo' in c_norm:
            idx_proc = i
    if idx_op is None or idx_proc is None:
        return  # Não encontrou colunas necessárias
    # Limpa tags antigas
    for item in tabela.get_children():
        tabela.item(item, tags=())
    for idx, item in enumerate(tabela.get_children()):
        valores = list(tabela.item(item)['values'])
        if idx_op is None or idx_proc is None or idx_op >= len(valores) or idx_proc >= len(valores):
            continue
        op = str(valores[idx_op]).strip()
        proc = unidecode.unidecode(str(valores[idx_proc])).lower().strip()
        # Se mudou a OP, reseta cor/bloco
        if op != op_anterior:
            cor_atual = None
            bloco_tag = None
            op_anterior = op
        # Se encontrou nova entrada/acerto, inicia novo bloco de cor
        if padrao_entrada.search(proc):
            cor_atual = cores[bloco_idx % len(cores)]
            bloco_tag = f'entrada_bloco_{bloco_idx}'
            tabela.tag_configure(bloco_tag, background=cor_atual)
            bloco_idx += 1
        # Aplica cor se estiver em bloco de entrada
        if cor_atual and bloco_tag:
            tabela.item(item, tags=(str(bloco_tag),))
        else:
            tabela.item(item, tags=())
