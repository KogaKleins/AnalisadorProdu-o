"""
Lógica de análise e setup para máquina Laminadora
"""
VEL_PADRAO_LAMINADORA = 4000  # p/h

def get_velocidade_padrao():
    """Retorna a velocidade nominal padrão da Laminadora em p/h"""
    return VEL_PADRAO_LAMINADORA

from src.core.metrics.utils import preencher_campos_generico

def preencher_campos_laminadora(df):
    regras_setup = [
        (lambda proc, evt: 'acerto' in evt, '00:45'),
    ]
    regras_media = [
        (lambda proc, evt: 'produção' in evt, '4000 p/h'),
    ]
    return preencher_campos_generico(df, regras_setup, regras_media)

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho para Laminadora, usando o pipeline de análise geral.
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
    df = preencher_campos_laminadora(df)
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado
