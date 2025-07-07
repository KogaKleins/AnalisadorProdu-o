"""
Módulo responsável pelo processamento e análise dos dados de produção.
"""

from typing import Dict, List, Tuple, Set
import pandas as pd
import unicodedata
import re
from src.core.metrics.maquinas import komori, bobst

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa os dados brutos do DataFrame aplicando as transformações necessárias.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados brutos
        
    Returns:
        pd.DataFrame: DataFrame processado e limpo
    """
    if df is None or df.empty:
        return pd.DataFrame()
        
    # Faz uma cópia para não modificar o original
    df_processed = df.copy()
    
    # Aplica validações nas linhas
    valid_mask = df_processed.apply(validar_dados_linha, axis=1)
    df_processed = df_processed[valid_mask]
    
    # Ordena por data/hora se existirem essas colunas
    if 'Data' in df_processed.columns and 'Hora' in df_processed.columns:
        if isinstance(df_processed, pd.DataFrame):
            df_processed = df_processed.sort_values(by=['Data', 'Hora'])
    if not isinstance(df_processed, pd.DataFrame):
        df_processed = pd.DataFrame(df_processed)
        
    return df_processed

def validar_dados_linha(row: pd.Series) -> bool:
    """
    Valida se uma linha tem dados consistentes para processamento.
    """
    evento = str(row.get('Evento', ''))
    if not evento or pd.isna(evento):
        return False
    # Validações adicionais podem ser adicionadas aqui
    return True

def validate_data(df: pd.DataFrame) -> bool:
    """
    Valida se o DataFrame tem a estrutura e dados necessários para processamento.
    
    Args:
        df (pd.DataFrame): DataFrame a ser validado
        
    Returns:
        bool: True se os dados são válidos, False caso contrário
    """
    if df is None or df.empty:
        return False
        
    # Verifica colunas obrigatórias
    required_columns = {'Data', 'Hora', 'Evento'}
    if not required_columns.issubset(df.columns):
        return False
        
    # Verifica se tem pelo menos uma linha válida
    valid_rows = df.apply(validar_dados_linha, axis=1)
    return bool(valid_rows.any())

def normalizar_texto(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').upper()

def eh_acerto(evento: str) -> bool:
    """
    Verifica se um evento é do tipo acerto.
    
    Args:
        evento (str): Nome do evento
        
    Returns:
        bool: True se o evento é de acerto, False caso contrário
    """
    evento_norm = normalizar_texto(evento)
    return "ACERTO" in evento_norm

def eh_producao(evento: str) -> bool:
    """
    Verifica se um evento é do tipo produção.
    
    Args:
        evento (str): Nome do evento
        
    Returns:
        bool: True se o evento é de produção, False caso contrário
    """
    evento_norm = normalizar_texto(evento)
    return "PRODUCAO" in evento_norm

def to_float(val):
    if val is None or val == '':
        return 0.0
    if isinstance(val, str):
        val = val.replace('.', '').replace(',', '.')
    try:
        return float(val)
    except Exception:
        return 0.0

def to_int(val):
    if val is None or val == '':
        return 0
    if isinstance(val, str):
        val = val.replace('.', '').replace(',', '.')
    try:
        return int(float(val))
    except Exception:
        return 0

def tempo_para_minutos(tempo_str):
    if not tempo_str or tempo_str == '':
        return 0
    if isinstance(tempo_str, (int, float)):
        return int(tempo_str)
    try:
        partes = tempo_str.split(':')
        if len(partes) == 2:
            h, m = map(int, partes)
            return h * 60 + m
        return int(float(tempo_str))
    except Exception:
        return 0

def extrair_velocidade_nominal(row: pd.Series) -> float:
    return to_float(row.get('Velocidade', 0))

def extrair_quantidades(row: pd.Series) -> Tuple[int, int]:
    qtd_produzida = to_int(row.get('Qtd. Produzida', 0))
    qtd_recebida = to_int(row.get('Qtd. Recebida', 0))
    return qtd_produzida, qtd_recebida

def extrair_tempo_producao(row: pd.Series) -> float:
    # Prioriza campo auxiliar em minutos, se existir
    if 'Tempo (min)' in row and row['Tempo (min)'] not in [None, '', 0]:
        try:
            return float(row['Tempo (min)'])
        except Exception:
            pass
    return tempo_para_minutos(row.get('Tempo', 0))

def extrair_tempo_setup(row: pd.Series) -> float:
    # Para acerto, o tempo utilizado é o campo 'Tempo' (real)
    return tempo_para_minutos(row.get('Tempo', 0))

def processar_grupos(df: pd.DataFrame, linhas_agrupadas: Dict[str, List[int]]) -> Tuple[dict, dict]:
    """
    Processa e agrupa os dados de produção para análise.
    Sempre processa todas as OPs do DataFrame, mesmo que haja agrupamento manual.
    """
    print('DF shape:', df.shape)
    print('Linhas agrupadas:', linhas_agrupadas)
    grupos_para_analise = {}
    ops_analise = {}
    linhas_processadas = set()

    # AGRUPAMENTO AUTOMÁTICO POR OP (sempre processa todas as OPs)
    op_to_indices = {}
    if 'OS' in df.columns:
        for idx, row in df.iterrows():
            op = str(row.get('OS', ''))
            if op:
                op_to_indices.setdefault(op, []).append(idx)

    # Processa grupos agrupados pelo usuário
    for nome_grupo, linhas_grupo in linhas_agrupadas.items():
        print(f'Grupo: {nome_grupo}, linhas: {linhas_grupo}')
        op_principal = None
        for idx in linhas_grupo:
            if idx < len(df):
                op_val = str(df.iloc[idx].get('OS', ''))
                if op_val:
                    op_principal = op_val
                    break
        if not op_principal:
            continue
        indices_op = op_to_indices.get(op_principal, [])
        dados_grupo = {
            'linhas': indices_op,
            'tempo_total_producao': 0,
            'tempo_setup': 0,
            'qtd_produzida': 0,
            'qtd_acerto': 0,
            'velocidade_nominal': 0,
            'os': op_principal,
            'os_original': op_principal,
            'cliente': '',
            'processo': '',
            'eventos': [],
            'tem_acerto': False,
            'tem_producao': False,
            'detalhes_eventos': []
        }
        for linha_idx in indices_op:
            if linha_idx >= len(df):
                print(f'Linha {linha_idx} fora do DataFrame!')
                continue
            row = df.iloc[linha_idx]
            print(f'Linha {linha_idx}:', row.to_dict())
            if not validar_dados_linha(row):
                print(f'Linha {linha_idx} inválida!')
                continue
            evento = str(row.get('Evento', ''))
            dados_grupo['eventos'].append(evento)
            is_acerto = eh_acerto(evento)
            is_producao = eh_producao(evento)
            print(f'Evento: {evento} | Acerto: {is_acerto} | Producao: {is_producao}')
            if is_acerto:
                dados_grupo['tem_acerto'] = True
            if is_producao:
                dados_grupo['tem_producao'] = True
            tempo = extrair_tempo_producao(row) if is_producao else extrair_tempo_setup(row)
            qtd_produzida, qtd_recebida = extrair_quantidades(row)
            if is_producao:
                dados_grupo['tempo_total_producao'] += tempo
                dados_grupo['qtd_produzida'] += qtd_produzida
                dados_grupo['velocidade_nominal'] = extrair_velocidade_nominal(row)
            elif is_acerto:
                dados_grupo['tempo_setup'] += tempo
                dados_grupo['qtd_acerto'] += qtd_recebida
            if not dados_grupo['cliente']:
                dados_grupo['cliente'] = str(row.get('Cliente', ''))
            if not dados_grupo['processo']:
                # Prioriza 'Média Produção' se existir e não for vazio
                media_producao = str(row.get('Média Produção', '')).strip()
                if media_producao:
                    dados_grupo['processo'] = media_producao
                else:
                    dados_grupo['processo'] = str(row.get('Processo', ''))
            dados_grupo['detalhes_eventos'].append({
                'evento': evento,
                'is_producao': is_producao,
                'is_acerto': is_acerto,
                'tempo_producao': tempo,
                'qtd_produzida': qtd_produzida,
                'qtd_recebida': qtd_recebida
            })
        if dados_grupo['tem_acerto'] or dados_grupo['tem_producao']:
            grupos_para_analise[nome_grupo] = dados_grupo
            linhas_processadas.update(indices_op)
            if dados_grupo['os_original']:
                op_key = f"OP {dados_grupo['os_original']}"
                ops_analise.setdefault(op_key, []).append((nome_grupo, dados_grupo))

    # Garante que todas as OPs do DataFrame estejam em ops_analise (mesmo sem agrupamento manual)
    for op, indices_op in op_to_indices.items():
        op_key = f"OP {op}"
        # Se já existe no agrupamento manual, não adiciona duplicado
        if op_key in ops_analise:
            continue
        dados_grupo = {
            'linhas': indices_op,
            'tempo_total_producao': 0,
            'tempo_setup': 0,
            'qtd_produzida': 0,
            'qtd_acerto': 0,
            'velocidade_nominal': 0,
            'os': op,
            'os_original': op,
            'cliente': '',
            'processo': '',
            'eventos': [],
            'tem_acerto': False,
            'tem_producao': False,
            'detalhes_eventos': []
        }
        for linha_idx in indices_op:
            if linha_idx >= len(df):
                continue
            row = df.iloc[linha_idx]
            if not validar_dados_linha(row):
                continue
            evento = str(row.get('Evento', ''))
            dados_grupo['eventos'].append(evento)
            is_acerto = eh_acerto(evento)
            is_producao = eh_producao(evento)
            if is_acerto:
                dados_grupo['tem_acerto'] = True
            if is_producao:
                dados_grupo['tem_producao'] = True
            tempo = extrair_tempo_producao(row) if is_producao else extrair_tempo_setup(row)
            qtd_produzida, qtd_recebida = extrair_quantidades(row)
            if is_producao:
                dados_grupo['tempo_total_producao'] += tempo
                dados_grupo['qtd_produzida'] += qtd_produzida
                dados_grupo['velocidade_nominal'] = extrair_velocidade_nominal(row)
            elif is_acerto:
                dados_grupo['tempo_setup'] += tempo
                dados_grupo['qtd_acerto'] += qtd_recebida
            if not dados_grupo['cliente']:
                dados_grupo['cliente'] = str(row.get('Cliente', ''))
            if not dados_grupo['processo']:
                # Prioriza 'Média Produção' se existir e não for vazio
                media_producao = str(row.get('Média Produção', '')).strip()
                if media_producao:
                    dados_grupo['processo'] = media_producao
                else:
                    dados_grupo['processo'] = str(row.get('Processo', ''))
            dados_grupo['detalhes_eventos'].append({
                'evento': evento,
                'is_producao': is_producao,
                'is_acerto': is_acerto,
                'tempo_producao': tempo,
                'qtd_produzida': qtd_produzida,
                'qtd_recebida': qtd_recebida
            })
        if dados_grupo['tem_acerto'] or dados_grupo['tem_producao']:
            nome_grupo = f'OP_{op}'
            grupos_para_analise[nome_grupo] = dados_grupo
            ops_analise.setdefault(op_key, []).append((nome_grupo, dados_grupo))
    return grupos_para_analise, ops_analise

def calculate_setup_times(df):
    for idx, row in df.iterrows():
        maquina = str(row.get('Máquina', '')).lower()
        evento = str(row.get('Evento', '')).lower()
        row_dict = row.to_dict()  # Garante dicionário para as funções de extração
        if 'acerto' in evento:
            if 'komori' in maquina:
                df.at[idx, 'Tempo Setup'] = komori.extrair_tempo_setup(row_dict)
            elif 'hcd' in maquina:
                from src.core.metrics.maquinas import hcd
                df.at[idx, 'Tempo Setup'] = hcd.extrair_tempo_setup(row_dict)
            elif 'bobst' in maquina:
                df.at[idx, 'Tempo Setup'] = bobst.extrair_tempo_setup(row_dict)
            else:
                df.at[idx, 'Tempo Setup'] = ''
        else:
            df.at[idx, 'Tempo Setup'] = ''
    return df

# Função para extrair média de produção por máquina

def extrair_media_producao(row):
    maquina = str(row.get('Máquina', '')).lower()
    row_dict = row.to_dict()  # Garante dicionário para as funções de extração
    if 'komori' in maquina:
        return komori.extrair_media_producao(row_dict)
    elif 'hcd' in maquina:
        from src.core.metrics.maquinas import hcd
        return hcd.extrair_media_producao(row_dict)
    elif 'bobst' in maquina:
        return bobst.extrair_media_producao(row_dict)
    else:
        return row.get('Média Produção', '').strip()
