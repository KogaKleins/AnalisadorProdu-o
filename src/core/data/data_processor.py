"""
Módulo responsável pelo processamento e análise dos dados de produção.
"""

from typing import Dict, List, Tuple, Set
import pandas as pd

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
    df_processed = df_processed[df_processed.apply(lambda row: validar_dados_linha(row, df_processed), axis=1)]
    
    # Ordena por data/hora se existirem essas colunas
    if 'Data' in df_processed.columns and 'Hora' in df_processed.columns:
        df_processed = df_processed.sort_values(['Data', 'Hora'])
        
    return df_processed

def validar_dados_linha(row: pd.Series, df: pd.DataFrame) -> bool:
    """
    Valida se uma linha tem dados consistentes para processamento.
    
    Args:
        row (pd.Series): Linha do DataFrame a ser validada
        df (pd.DataFrame): DataFrame completo para contexto
        
    Returns:
        bool: True se a linha é válida, False caso contrário
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
    valid_rows = df.apply(lambda row: validar_dados_linha(row, df), axis=1)
    return valid_rows.any()

def eh_acerto(evento: str) -> bool:
    """
    Verifica se um evento é do tipo acerto.
    
    Args:
        evento (str): Nome do evento
        
    Returns:
        bool: True se o evento é de acerto, False caso contrário
    """
    return "ACERTO" in str(evento).upper()

def eh_producao(evento: str) -> bool:
    """
    Verifica se um evento é do tipo produção.
    
    Args:
        evento (str): Nome do evento
        
    Returns:
        bool: True se o evento é de produção, False caso contrário
    """
    return "PRODUCAO" in str(evento).upper()

def extrair_velocidade_nominal(row: pd.Series) -> float:
    """
    Extrai a velocidade nominal de uma linha.
    
    Args:
        row (pd.Series): Linha do DataFrame
        
    Returns:
        float: Velocidade nominal extraída ou 0 se não encontrada
    """
    try:
        return float(row.get('Velocidade', 0))
    except (ValueError, TypeError):
        return 0

def extrair_quantidades(row: pd.Series) -> Tuple[int, int]:
    """
    Extrai as quantidades produzidas e recebidas de uma linha.
    
    Args:
        row (pd.Series): Linha do DataFrame
        
    Returns:
        Tuple[int, int]: Tupla com (quantidade_produzida, quantidade_recebida)
    """
    qtd_produzida = 0
    qtd_recebida = 0
    
    try:
        qtd_produzida = int(row.get('Qtd_Produzida', 0))
    except (ValueError, TypeError):
        pass
        
    try:
        qtd_recebida = int(row.get('Qtd_Recebida', 0))
    except (ValueError, TypeError):
        pass
        
    return qtd_produzida, qtd_recebida

def extrair_tempo_producao(row: pd.Series) -> float:
    """
    Extrai o tempo de produção de uma linha.
    
    Args:
        row (pd.Series): Linha do DataFrame
        
    Returns:
        float: Tempo de produção em minutos
    """
    try:
        return float(row.get('Tempo', 0))
    except (ValueError, TypeError):
        return 0

def processar_grupos(df: pd.DataFrame, linhas_agrupadas: Dict[str, List[int]]) -> Tuple[dict, dict]:
    """
    Processa e agrupa os dados de produção para análise.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados brutos
        linhas_agrupadas (Dict[str, List[int]]): Dicionário com as linhas agrupadas por nome
        
    Returns:
        Tuple[dict, dict]: Tupla com (grupos_para_analise, ops_analise)
    """
    grupos_para_analise = {}
    ops_analise = {}
    linhas_processadas = set()
    
    # Processa grupos agrupados pelo usuário
    for nome_grupo, linhas_grupo in linhas_agrupadas.items():
        dados_grupo = {
            'linhas': linhas_grupo,
            'tempo_total_producao': 0,
            'tempo_setup': 0,
            'qtd_produzida': 0,
            'qtd_acerto': 0,
            'velocidade_nominal': 0,
            'os': '',
            'os_original': '',
            'cliente': '',
            'processo': '',
            'eventos': [],
            'tem_acerto': False,
            'tem_producao': False,
            'detalhes_eventos': []
        }
        
        for linha_idx in linhas_grupo:
            if linha_idx >= len(df):
                continue
                
            row = df.iloc[linha_idx]
            if not validar_dados_linha(row, df):
                continue
                
            evento = str(row.get('Evento', ''))
            dados_grupo['eventos'].append(evento)
            
            is_acerto = eh_acerto(evento)
            is_producao = eh_producao(evento)
            
            if is_acerto:
                dados_grupo['tem_acerto'] = True
            if is_producao:
                dados_grupo['tem_producao'] = True
                
            tempo = extrair_tempo_producao(row)
            qtd_produzida, qtd_recebida = extrair_quantidades(row)
            
            if is_producao:
                dados_grupo['tempo_total_producao'] += tempo
                dados_grupo['qtd_produzida'] += qtd_produzida
                dados_grupo['velocidade_nominal'] = extrair_velocidade_nominal(row)
            elif is_acerto:
                dados_grupo['tempo_setup'] += tempo
                dados_grupo['qtd_acerto'] += qtd_recebida
                
            # Atualiza informações gerais
            if not dados_grupo['os_original']:
                dados_grupo['os_original'] = str(row.get('OS', ''))
                dados_grupo['os'] = dados_grupo['os_original']
                dados_grupo['cliente'] = str(row.get('Cliente', ''))
                dados_grupo['processo'] = str(row.get('Processo', ''))
            
            # Adiciona detalhes do evento para debug
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
            linhas_processadas.update(linhas_grupo)
            
            if dados_grupo['os_original']:
                op_key = f"OP {dados_grupo['os_original']}"
                ops_analise.setdefault(op_key, []).append((nome_grupo, dados_grupo))
                
    return grupos_para_analise, ops_analise
