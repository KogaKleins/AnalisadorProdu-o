"""
Lógica de análise e setup para máquina Verniz.UV Sakurai
"""
from src.core.metrics.utils import preencher_campos_generico

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho para Sakurai, usando o pipeline de análise geral.
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
    df = preencher_campos_sakurai(df)
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado

def preencher_campos_sakurai(df):
    regras_setup = [
        (lambda proc, evt: 'acerto' in evt, '02:50'),
    ]
    regras_media = [
        (lambda proc, evt: 'produção' in evt, '1800 p/h'),
    ]
    return preencher_campos_generico(df, regras_setup, regras_media)
