"""
Lógica de análise e setup para máquina Furnax
"""
import re

def preencher_campos_furnax(df):
    """
    Preenche Tempo Setup e Média Produção conforme regras da Furnax, mas só se o campo estiver vazio.
    """
    for idx, row in df.iterrows():
        processo = str(row.get('Processo', '')).lower()
        evento = str(row.get('Evento', '')).lower()
        # Tempo Setup
        setup_atual = str(row.get('Tempo Setup', '')).strip()
        if 'acerto' in evento and not setup_atual:
            if 'destaque' in processo:
                df.at[idx, 'Tempo Setup'] = '03:00'
            elif 'relevo + corte' in processo or 'hot stamping' in processo:
                df.at[idx, 'Tempo Setup'] = '02:00'
            elif 'nova' in processo:
                df.at[idx, 'Tempo Setup'] = '01:30'
            else:
                df.at[idx, 'Tempo Setup'] = '01:00'
        # Média Produção
        media_atual = str(row.get('Média Produção', '')).strip()
        if not media_atual:
            if 'micro ondulado' in processo:
                df.at[idx, 'Média Produção'] = '2000 p/h'
            else:
                df.at[idx, 'Média Produção'] = '4000 p/h'
    return df

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho padrão para Furnax, usando o pipeline de análise geral.
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
    df = preencher_campos_furnax(df)
    grupos_para_analise, ops_analise = processar_grupos(df, config.get('linhas_agrupadas', {}))
    generator = ReportGenerator()
    resultado = generator.generate_report({'grupos': grupos_para_analise, 'ops': ops_analise, 'df': df}, {
        'hora_inicio': hora_inicio,
        'hora_fim': hora_fim,
        'intervalo': intervalo
    })
    return resultado

VEL_PADRAO_FURNAX = 4000  # p/h

def get_velocidade_padrao():
    """Retorna a velocidade padrão da Furnax (p/h)"""
    return VEL_PADRAO_FURNAX

def calcular_velocidade_real(quantidade, tempo_min, processo=None):
    """Calcula a velocidade real da Furnax dado quantidade e tempo em minutos, considerando micro ondulado"""
    if tempo_min == 0:
        return 0
    if processo and 'micro ondulado' in processo.lower():
        return (quantidade / tempo_min) * 60 if tempo_min else 0
    return (quantidade / tempo_min) * 60

def extrair_tempo_setup(linha):
    processo = linha.get('Processo', '').lower()
    evento = linha.get('Evento', '').lower()
    if 'acerto' in evento:
        if 'nova' in processo:
            return '01:30'
        return '01:00'
    return ''

def extrair_media_producao(linha):
    processo = linha.get('Processo', '').lower()
    if 'micro ondulado' in processo:
        return '2000 p/h'
    return '4000 p/h'
