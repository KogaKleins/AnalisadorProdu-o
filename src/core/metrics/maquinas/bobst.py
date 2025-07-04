"""
Lógica de análise e setup para máquina Bobst
"""

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho padrão para Bobst, usando o pipeline de análise geral.
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
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado

def get_tempos_setup():
    # Pode retornar tempos de setup específicos da Bobst
    return {
        'berco': 180,
        'colagem_bandeja': 130,
        'fundo_automatico_primeiro': 130,
        'fundo_automatico_outros': 30,
        'colagem_lateral_primeiro': 130,
        'colagem_lateral_outros': 15,
        'default': 180
    }

from core.config.setup_config import get_setup_time

def extrair_tempo_setup(linha):
    # Para Bobst, usar configuração global conforme o tipo de processo
    processo = linha.get('Processo', '').lower()
    # Tenta identificar o tipo de processo e retorna o tempo pré-determinado
    tempo_min = get_setup_time(processo)
    # Retorna no formato 'HH:MM'
    horas = tempo_min // 60
    minutos = tempo_min % 60
    return f'{horas:02d}:{minutos:02d}'

def extrair_media_producao(linha):
    media = linha.get('Média Produção', '').strip()
    if not media:
        # Fallback: extrair do campo Processo
        processo = linha.get('Processo', '')
        if 'p/h' in processo:
            return processo.split('p/h')[0].strip() + ' p/h'
        return ''
    return media
