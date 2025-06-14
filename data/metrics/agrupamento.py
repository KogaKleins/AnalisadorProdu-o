# Arquivo: data/metrics/agrupamento.py

from data.metrics.utils import (
    converter_tempo_para_minutos,
    extrair_velocidade_nominal,
    extrair_op_numero,
    eh_acerto,
    eh_producao,
    extrair_quantidades_melhorada,
    validar_dados_linha
)

def agrupar_dados(df, linhas_agrupadas):
    """Agrupa dados de forma mais precisa, separando corretamente acerto e produção"""
    grupos_para_analise = {}
    ops_analise = {}
    linhas_processadas = set()

    # Processa grupos agrupados pelo usuário
    for nome_grupo, linhas_grupo in linhas_agrupadas.items():
        dados_grupo = inicializar_dados_grupo(linhas_grupo)
        
        # Processa cada linha do grupo
        for linha_idx in linhas_grupo:
            if linha_idx >= len(df):
                continue
                
            row = df.iloc[linha_idx]
            
            # Valida se a linha tem dados consistentes
            if not validar_dados_linha(row, df):
                continue
            
            processar_linha_no_grupo(row, df, dados_grupo)
        
        # Só adiciona o grupo se tiver dados válidos
        if dados_grupo['tem_acerto'] or dados_grupo['tem_producao']:
            grupos_para_analise[nome_grupo] = dados_grupo
            linhas_processadas.update(linhas_grupo)
            
            # Adiciona à análise por OP se tiver - MANTENDO FORMATO ORIGINAL
            if dados_grupo['os_original']:  # Usa versão original
                op_key = f"OP {dados_grupo['os_original']}"
                ops_analise.setdefault(op_key, []).append((nome_grupo, dados_grupo))

    # Processa linhas soltas (não agrupadas)
    processar_linhas_soltas(df, grupos_para_analise, ops_analise, linhas_processadas)

    return grupos_para_analise, ops_analise

def inicializar_dados_grupo(linhas_grupo):
    """Inicializa estrutura de dados do grupo"""
    return {
        'linhas': linhas_grupo,
        'tempo_total_producao': 0,
        'tempo_setup': 0,
        'qtd_produzida': 0,
        'qtd_acerto': 0,
        'velocidade_nominal': 0,
        'os': '',
        'os_original': '',  # NOVO: Mantém formato original (118.951, 119.000)
        'cliente': '',
        'processo': '',
        'eventos': [],
        'tem_acerto': False,
        'tem_producao': False,
        'detalhes_eventos': []  # Para debug
    }

def processar_linha_no_grupo(row, df, dados_grupo):
    """Processa uma linha individual dentro de um grupo"""
    evento = str(row.get('Evento', ''))
    dados_grupo['eventos'].append(evento)
    
    is_acerto = eh_acerto(evento)
    is_producao = eh_producao(evento)
    
    if is_acerto:
        dados_grupo['tem_acerto'] = True
    if is_producao:
        dados_grupo['tem_producao'] = True
    
    # Extrai tempos de forma mais precisa
    tempo_producao = extrair_tempo_producao(row, df)
    tempo_setup = extrair_tempo_setup(row, df, is_acerto)
    
    # Extrai quantidades corretamente
    qtd_produzida, qtd_recebida = extrair_quantidades_melhorada(row, df)
    
    # Atualiza dados do grupo baseado no tipo de evento
    if is_producao:
        dados_grupo['tempo_total_producao'] += tempo_producao
        dados_grupo['qtd_produzida'] += qtd_produzida
    elif is_acerto:
        dados_grupo['tempo_setup'] += tempo_setup
        dados_grupo['qtd_acerto'] += qtd_recebida  # Quantidade de acerto
    
    # Atualiza informações gerais (uma vez por grupo)
    atualizar_info_geral(row, dados_grupo)
    
    # Adiciona detalhes para debug
    dados_grupo['detalhes_eventos'].append({
        'evento': evento,
        'is_acerto': is_acerto,
        'is_producao': is_producao,
        'tempo_producao': tempo_producao,
        'tempo_setup': tempo_setup,
        'qtd_produzida': qtd_produzida,
        'qtd_recebida': qtd_recebida
    })

def extrair_tempo_producao(row, df):
    """Extrai tempo de produção (colunas que não são setup)"""
    for col in df.columns:
        col_lower = str(col).lower()
        if "tempo" in col_lower and "setup" not in col_lower:
            tempo_str = str(row.get(col, "00:00"))
            return converter_tempo_para_minutos(tempo_str)
    return 0

def extrair_tempo_setup(row, df, is_acerto):
    """Extrai tempo de setup apenas se for evento de acerto"""
    if not is_acerto:
        return 0
    
    tempo_setup_str = str(row.get('Tempo Setup', '00:00'))
    return converter_tempo_para_minutos(tempo_setup_str)

def atualizar_info_geral(row, dados_grupo):
    """Atualiza informações gerais do grupo (OS, cliente, processo, etc.)"""
    processo = str(row.get('Processo', ''))
    os_value = str(row.get('OS', ''))
    cliente = str(row.get('Cliente', ''))
    
    # Atualiza velocidade nominal se ainda não tiver
    if not dados_grupo['velocidade_nominal'] and processo:
        dados_grupo['velocidade_nominal'] = extrair_velocidade_nominal(processo)
    
    # MELHORIA: Mantém formato original E versão limpa da OS
    if not dados_grupo['os_original'] and os_value and os_value != '0':
        dados_grupo['os_original'] = os_value  # Formato original (118.951)
        dados_grupo['os'] = extrair_op_numero(os_value)  # Versão limpa (118951)
    
    # Atualiza cliente se ainda não tiver
    if not dados_grupo['cliente'] and cliente:
        dados_grupo['cliente'] = cliente
    
    # Atualiza processo se ainda não tiver
    if not dados_grupo['processo'] and processo:
        dados_grupo['processo'] = processo

def processar_linhas_soltas(df, grupos_para_analise, ops_analise, linhas_processadas):
    """Processa linhas que não foram agrupadas pelo usuário"""
    for idx, row in df.iterrows():
        if idx in linhas_processadas:
            continue
        
        if not validar_dados_linha(row, df):
            continue
        
        evento = str(row.get('Evento', ''))
        nome_grupo = f"Linha_{idx+1}"
        
        # Cria dados individuais para a linha
        dados_individual = inicializar_dados_grupo([idx])
        processar_linha_no_grupo(row, df, dados_individual)
        
        # Só adiciona se tiver dados válidos
        if dados_individual['tem_acerto'] or dados_individual['tem_producao']:
            grupos_para_analise[nome_grupo] = dados_individual
            
            # Adiciona à análise por OP se tiver - MANTENDO FORMATO ORIGINAL
            if dados_individual['os_original']:
                op_key = f"OP {dados_individual['os_original']}"
                ops_analise.setdefault(op_key, []).append((nome_grupo, dados_individual))