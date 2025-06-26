"""
Módulo responsável pelos cálculos e métricas do relatório de produção.
"""

from datetime import datetime
from ...config.setup_config import tempos_setup

def calcular_tempo_disponivel(hora_inicio: str, hora_fim: str, intervalo: int) -> int:
    """
    Calcula o tempo disponível em minutos entre um período, descontando o intervalo.
    
    Args:
        hora_inicio (str): Hora de início no formato HH:MM
        hora_fim (str): Hora de fim no formato HH:MM
        intervalo (int): Duração do intervalo em minutos
        
    Returns:
        int: Tempo disponível em minutos
    """
    def minutos(hora: str) -> int:
        h, m = map(int, hora.split(':'))
        return h * 60 + m
    
    inicio_min = minutos(hora_inicio)
    fim_min = minutos(hora_fim)
    return fim_min - inicio_min - intervalo

def calcular_metricas_gerais(grupos_para_analise: dict, ops_analise: dict, tempo_disponivel: int) -> dict:
    """
    Calcula as métricas gerais de produção, incluindo tempos e eficiências.
    
    Args:
        grupos_para_analise (dict): Dicionário com os grupos de análise
        ops_analise (dict): Dicionário com as OPs analisadas
        tempo_disponivel (int): Tempo disponível total em minutos
        
    Returns:
        dict: Dicionário com todas as métricas calculadas
    """
    metricas = {
        'tempo_total_producao': 0,
        'tempo_total_acerto': 0,
        'qtd_total_produzida': 0,
        'tempo_total_perdido_ganho': 0,
        'eficiencia_producao': 0,
        'eficiencia_acerto': 0,
        'eficiencia_tempo_geral': 0,
        'tempo_ocioso': 0
    }
    
    # Calcula totais de produção
    tempo_total_producao = 0
    tempo_total_acerto = 0
    qtd_total_produzida = 0
    
    for dados in grupos_para_analise.values():
        for detalhe in dados.get('detalhes_eventos', []):
            if detalhe.get('is_producao'):
                tempo_total_producao += detalhe.get('tempo_producao', 0)
                qtd_total_produzida += detalhe.get('qtd_produzida', 0)
            if detalhe.get('is_acerto'):
                tempo_total_acerto += detalhe.get('tempo_producao', 0)
    
    metricas['tempo_total_producao'] = tempo_total_producao
    metricas['tempo_total_acerto'] = tempo_total_acerto
    metricas['qtd_total_produzida'] = qtd_total_produzida
    metricas['tempo_ocioso'] = tempo_disponivel - (tempo_total_producao + tempo_total_acerto)
    
    # Calcula eficiências e atrasos/ganhos das OPs
    if ops_analise:
        soma_atrasos = 0
        soma_eficiencia_producao = 0
        soma_eficiencia_acerto = 0
        count_ops_producao = 0
        count_ops_acerto = 0
        
        for dados_op in ops_analise.values():
            for _, info_op in dados_op:
                if info_op.get('velocidade_nominal', 0) > 0:
                    if info_op.get('qtd_produzida', 0) > 0:
                        tempo_programado = (info_op['qtd_produzida'] / info_op['velocidade_nominal']) * 60
                        atraso = info_op.get('tempo_total_producao', 0) - tempo_programado
                        soma_atrasos += atraso
                        count_ops_producao += 1
                        
                    if info_op.get('tem_acerto', False):
                        count_ops_acerto += 1
        
        metricas['tempo_total_perdido_ganho'] = soma_atrasos
        
        # Calcula eficiências médias
        if count_ops_producao > 0:
            metricas['eficiencia_producao'] = (tempo_total_producao / tempo_disponivel) * 100
            
        if count_ops_acerto > 0:
            metricas['eficiencia_acerto'] = (tempo_total_acerto / tempo_disponivel) * 100
            
        metricas['eficiencia_tempo_geral'] = ((tempo_total_producao + tempo_total_acerto) / tempo_disponivel) * 100
    
    return metricas
