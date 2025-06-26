"""
Efficiency calculations and metrics module.
Contains functions for calculating and analyzing efficiency metrics.
"""

from core.config.setup_config import TEMPOS_SETUP as tempos_setup

def calculate_general_metrics(grupos_para_analise, ops_analise, tempo_disponivel):
    """Calculate general metrics with new formulas"""
    metrics = {
        'tempo_total_producao': 0,
        'tempo_total_acerto': 0,
        'qtd_total_produzida': 0,
        'tempo_total_perdido_ganho': 0,
        'eficiencia_producao': 0,
        'eficiencia_acerto': 0,
        'eficiencia_tempo_geral': 0,
        'tempo_ocioso': 0
    }
    
    # Sum times directly from event details
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
    
    metrics['tempo_total_producao'] = tempo_total_producao
    metrics['tempo_total_acerto'] = tempo_total_acerto
    metrics['qtd_total_produzida'] = qtd_total_produzida
    metrics['tempo_ocioso'] = tempo_disponivel - (tempo_total_producao + tempo_total_acerto)
    
    # Calculate OPs delay/gain and efficiencies
    if ops_analise:
        metrics.update(_calculate_ops_metrics(ops_analise, tempo_disponivel))
        
        # Calculate general efficiencies
        if tempo_disponivel > 0:
            metrics['eficiencia_producao'] = (tempo_total_producao / tempo_disponivel) * 100
            metrics['eficiencia_acerto'] = (tempo_total_acerto / tempo_disponivel) * 100
            metrics['eficiencia_tempo_geral'] = ((tempo_total_producao + tempo_total_acerto) / tempo_disponivel) * 100
    
    return metrics

def _calculate_ops_metrics(ops_analise, tempo_disponivel):
    """Calculate metrics related to OPs"""
    metrics = {}
    soma_atraso_ops = 0
    count_ops = 0
    
    for grupos_op in ops_analise.values():
        dados_op = consolidar_dados_op(grupos_op)
        
        if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
            tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
            atraso = dados_op['tempo_total_producao'] - tempo_programado
            soma_atraso_ops += atraso
            count_ops += 1
    
    metrics['tempo_total_perdido_ganho'] = soma_atraso_ops
    return metrics

def consolidar_dados_op(grupos_op):
    """Consolidate data from multiple groups of the same OP"""
    dados_consolidados = {
        'tempo_total_producao': 0,
        'tempo_setup': 0,
        'qtd_produzida': 0,
        'velocidade_nominal': 0,
        'os': '',
        'cliente': '',
        'processo': '',
        'tem_acerto': False
    }
    
    for _, dados in grupos_op:
        dados_consolidados['tempo_total_producao'] += dados.get('tempo_total_producao', 0)
        dados_consolidados['tempo_setup'] += dados.get('tempo_setup', 0)
        dados_consolidados['qtd_produzida'] += dados.get('qtd_produzida', 0)
        
        if not dados_consolidados['velocidade_nominal'] and dados.get('velocidade_nominal'):
            dados_consolidados['velocidade_nominal'] = dados['velocidade_nominal']
            
        if not dados_consolidados['os'] and dados.get('os'):
            dados_consolidados['os'] = dados['os']
            dados_consolidados['cliente'] = dados.get('cliente', '')
            dados_consolidados['processo'] = dados.get('processo', '')
            
        if dados.get('tem_acerto'):
            dados_consolidados['tem_acerto'] = True
    
    return dados_consolidados

def calculate_setup_time(processo):
    """Calculate programmed setup time based on process type"""
    return tempos_setup.get(processo.upper(), 45)  # Default 45 minutes if not found

def get_efficiency_classification(eficiencia):
    """Get emoji classification based on efficiency percentage"""
    if eficiencia >= 95:
        return "🌟 EXCELENTE"
    elif eficiencia >= 85:
        return "✨ ÓTIMO"
    elif eficiencia >= 75:
        return "👍 BOM"
    elif eficiencia >= 65:
        return "⚠️ REGULAR"
    else:
        return "❌ INSATISFATÓRIO"

def calculate_op_metrics(dados_op):
    """Calculate specific metrics for an OP"""
    metrics = {
        'atraso': 0,
        'eficiencia_producao': 0,
        'eficiencia_setup': 0
    }
    
    if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
        tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
        metrics['atraso'] = dados_op['tempo_total_producao'] - tempo_programado
        
        if tempo_programado > 0:
            metrics['eficiencia_producao'] = (tempo_programado / dados_op['tempo_total_producao']) * 100
            
        if dados_op['tem_acerto']:
            tempo_setup_programado = calculate_setup_time(dados_op['processo'])
            if tempo_setup_programado > 0:
                metrics['eficiencia_setup'] = (tempo_setup_programado / dados_op['tempo_setup']) * 100
    
    return metrics
