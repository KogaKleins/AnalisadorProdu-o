"""
Lógica de análise e setup para máquina HCD
"""
import re
from src.core.metrics.utils import preencher_campos_generico

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho padrão para HCD, usando o pipeline de análise geral.
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
    df = preencher_campos_hcd(df)
    return resultado

def extrair_tempo_setup(linha):
    processo = linha.get('Processo', '').lower()
    maquina = linha.get('Máquina', '')
    # Aceita: '1h 30 min', '1h30min', '1h', '2 horas', '45 min', '45min', etc.
    match_hora_min = re.search(r'(\d{1,2})\s*h(?:ora)?(?:s)?\s*(\d{1,2})?\s*min', processo)
    match_hora_min_junto = re.search(r'(\d{1,2})h(\d{1,2})min', processo)
    match_hora = re.search(r'(\d{1,2})\s*h(?:ora)?(?:s)?', processo)
    match_min = re.search(r'(\d{1,2})\s*min', processo)
    match_min_junto = re.search(r'(\d{1,2})min', processo)
    tempo = ''
    if match_hora_min:
        horas = int(match_hora_min.group(1))
        minutos = int(match_hora_min.group(2)) if match_hora_min.group(2) else 0
        tempo = f'{horas:02d}:{minutos:02d}'
    elif match_hora_min_junto:
        horas = int(match_hora_min_junto.group(1))
        minutos = int(match_hora_min_junto.group(2))
        tempo = f'{horas:02d}:{minutos:02d}'
    elif match_hora:
        horas = int(match_hora.group(1))
        tempo = f'{horas:02d}:00'
    elif match_min:
        minutos = int(match_min.group(1))
        tempo = f'00:{minutos:02d}'
    elif match_min_junto:
        minutos = int(match_min_junto.group(1))
        tempo = f'00:{minutos:02d}'
    return tempo

def extrair_media_producao(linha):
    media = linha.get('Média Produção', '').strip()
    if not media:
        return '5000 p/h'
    return media

def preencher_campos_hcd(df):
    regras_setup = [
        (lambda proc, evt: 'nova' in proc, '01:30'),
        (lambda proc, evt: True, '01:00'),
    ]
    regras_media = [
        (lambda proc, evt: 'produção' in evt, '5000 p/h'),
    ]
    return preencher_campos_generico(df, regras_setup, regras_media)
