from src.core.metrics.utils import preencher_campos_generico

def preencher_campos_cv_guangya(df):
    regras_setup = [
        (lambda proc, evt: 'hot stamping' in proc, '02:00'),
        (lambda proc, evt: 'faca nova' in proc, '01:30'),
        (lambda proc, evt: 'faca' in proc, '01:00'),
        (lambda proc, evt: True, '00:30'),
    ]
    regras_media = [
        (lambda proc, evt: 'produção' in evt, '900 p/h'),
    ]
    return preencher_campos_generico(df, regras_setup, regras_media)

def calcular_desempenho(df_global, config):
    hora_inicio = config.get('hora_inicio')
    hora_fim = config.get('hora_fim')
    intervalo_str = config.get('intervalo', '60')
    if not hora_inicio or not hora_fim:
        return "❌ ERRO: Preencha os horários de início e fim."
    intervalo = int(intervalo_str) if intervalo_str else 60
    from src.core.data.data_processor import processar_grupos
    from src.core.metrics.report.generator import ReportGenerator
    df = df_global.copy()
    df = preencher_campos_cv_guangya(df)
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado 