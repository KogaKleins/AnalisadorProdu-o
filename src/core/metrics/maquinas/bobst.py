"""
Lógica de análise e setup para máquina Bobst
"""

def calcular_desempenho(df_global, config):
    """
    Lógica de desempenho padrão (original) para Bobst
    """
    hora_inicio = config.get('hora_inicio')
    hora_fim = config.get('hora_fim')
    intervalo_str = config.get('intervalo', '60')
    if not hora_inicio or not hora_fim:
        return "❌ ERRO: Preencha os horários de início e fim."
    intervalo = int(intervalo_str) if intervalo_str else 60
    from data.metrics.agrupamento import agrupar_dados
    from data.metrics.relatorio import gerar_relatorio
    df = df_global.copy()
    grupos_para_analise, ops_analise = agrupar_dados(df, config.get('linhas_agrupadas', {}))
    resultado = gerar_relatorio(grupos_para_analise, ops_analise, hora_inicio, hora_fim, intervalo)
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
