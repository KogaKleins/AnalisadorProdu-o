"""
Lógica de análise e setup para máquina SBL (igual Furnax)
"""

from src.core.metrics.utils import preencher_campos_generico

def preencher_campos_sbl(df):
    """
    Preenche Tempo Setup e Média Produção conforme regras da SBL, mas só se o campo estiver vazio.
    """
    regras_setup = [
        (lambda proc, evt: 'destaque' in proc, '03:00'),
        (lambda proc, evt: 'relevo + corte' in proc or 'hot stamping' in proc, '02:00'),
        (lambda proc, evt: 'nova' in proc, '01:30'),
        (lambda proc, evt: True, '01:00'),
    ]
    regras_media = [
        (lambda proc, evt: 'produção' in evt and 'micro ondulado' in proc, '2000 p/h'),
        (lambda proc, evt: 'produção' in evt, '4000 p/h'),
    ]
    return preencher_campos_generico(df, regras_setup, regras_media)

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho padrão para SBL, usando o pipeline de análise geral.
    """
    hora_inicio = config.get('hora_inicio')
    hora_fim = config.get('hora_fim')
    intervalo_str = config.get('intervalo', '60')
    if not hora_inicio or not hora_fim:
        return "❌ ERRO: Preencha os horários de início e fim."
    intervalo = int(intervalo_str) if intervalo_str else 60
    from src.core.data.data_processor import processar_grupos
    from src.core.metrics.report.generator import ReportGenerator
    df = df_global.copy()
    df = preencher_campos_sbl(df)
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado

VEL_PADRAO_SBL = 4000  # p/h

def get_velocidade_padrao():
    """Retorna a velocidade padrão da SBL (p/h)"""
    return VEL_PADRAO_SBL

def calcular_velocidade_real(quantidade, tempo_min, processo=None):
    """Calcula a velocidade real da SBL dado quantidade e tempo em minutos, considerando micro ondulado"""
    if tempo_min == 0:
        return 0
    if processo and 'micro ondulado' in processo.lower():
        return (quantidade / tempo_min) * 60 if tempo_min else 0
    return (quantidade / tempo_min) * 60
