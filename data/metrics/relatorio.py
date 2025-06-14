# Arquivo: data/metrics/relatorio.py
from datetime import datetime
import re

def gerar_relatorio(grupos_para_analise, ops_analise, hora_inicio, hora_fim, intervalo):
    """Gera relatório com cálculos mais precisos e melhorias solicitadas"""
    
    # Calcula tempo disponível
    tempo_disponivel = calcular_tempo_disponivel(hora_inicio, hora_fim, intervalo)
    
    # Cabeçalho do relatório
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    relatorio = f"📊 RELATÓRIO DE DESEMPENHO - {data_atual}\n"
    relatorio += "=" * 80 + "\n\n"
    
    # Seção de período de trabalho
    relatorio += gerar_secao_periodo(hora_inicio, hora_fim, intervalo, tempo_disponivel)
    
    # Calcula métricas gerais
    metricas_gerais = calcular_metricas_gerais(grupos_para_analise, tempo_disponivel)
    
    # Seção de resumo geral - COM DESTAQUE NA EFICIÊNCIA
    relatorio += gerar_secao_resumo_geral(metricas_gerais)
    
    # Seção de análise por OP - MELHORADA
    if ops_analise:
        relatorio += gerar_secao_ops_melhorada(ops_analise, grupos_para_analise)
    
    # REMOVIDO: Seção detalhada por grupo (redundante conforme solicitado)
    
    return relatorio

def calcular_tempo_disponivel(hora_inicio, hora_fim, intervalo):
    """Calcula tempo disponível em minutos"""
    def minutos(hora):
        h, m = map(int, hora.split(':'))
        return h * 60 + m
    
    inicio_min = minutos(hora_inicio)
    fim_min = minutos(hora_fim)
    return fim_min - inicio_min - intervalo

def gerar_secao_periodo(hora_inicio, hora_fim, intervalo, tempo_disponivel):
    """Gera seção do período de trabalho"""
    relatorio = "⏰ PERÍODO DE TRABALHO\n"
    relatorio += "─" * 40 + "\n"
    relatorio += f"Início: {hora_inicio}\n"
    relatorio += f"Fim: {hora_fim}\n"
    relatorio += f"Intervalo: {intervalo} min\n"
    relatorio += f"Tempo Disponível: {tempo_disponivel} min ({tempo_disponivel/60:.1f}h)\n\n"
    return relatorio

def calcular_metricas_gerais(grupos_para_analise, tempo_disponivel):
    """Calcula métricas gerais de todos os grupos"""
    metricas = {
        'tempo_total_usado': 0,
        'tempo_total_acerto': 0,  # MUDANÇA: Renomeado de tempo_total_setup
        'qtd_total_produzida': 0,
        'qtd_total_acerto': 0,
        'velocidade_media_ponderada': 0,
        'eficiencia_tempo': 0,
        'velocidade_real': 0,
        'eficiencia_velocidade': 0
    }
    
    peso_total = 0
    velocidade_ponderada = 0
    
    for dados in grupos_para_analise.values():
        # Soma apenas tempos válidos
        if dados['tem_producao']:
            metricas['tempo_total_usado'] += dados['tempo_total_producao']
            metricas['qtd_total_produzida'] += dados['qtd_produzida']
        
        if dados['tem_acerto']:
            metricas['tempo_total_acerto'] += dados['tempo_setup']  # Soma real do tempo de acerto
            metricas['qtd_total_acerto'] += dados['qtd_acerto']
        
        # Calcula velocidade média ponderada
        if dados['velocidade_nominal'] > 0 and dados['tempo_total_producao'] > 0:
            peso_total += dados['tempo_total_producao']
            velocidade_ponderada += dados['velocidade_nominal'] * dados['tempo_total_producao']
    
    # Calcula velocidade média ponderada
    if peso_total > 0:
        metricas['velocidade_media_ponderada'] = velocidade_ponderada / peso_total
    
    # Calcula eficiências
    if tempo_disponivel > 0:
        tempo_total_efetivo = metricas['tempo_total_usado'] + metricas['tempo_total_acerto']
        metricas['eficiencia_tempo'] = (tempo_total_efetivo / tempo_disponivel * 100)
    
    if metricas['tempo_total_usado'] > 0:
        metricas['velocidade_real'] = metricas['qtd_total_produzida'] / (metricas['tempo_total_usado']/60)
    
    if metricas['velocidade_media_ponderada'] > 0:
        metricas['eficiencia_velocidade'] = (metricas['velocidade_real'] / metricas['velocidade_media_ponderada'] * 100)
    
    return metricas

def gerar_secao_resumo_geral(metricas):
    """Gera seção do resumo geral COM DESTAQUE NA EFICIÊNCIA DE TEMPO"""
    relatorio = "📈 RESUMO GERAL\n"
    relatorio += "─" * 40 + "\n"
    relatorio += f"Tempo Total Produção: {metricas['tempo_total_usado']} min ({metricas['tempo_total_usado']/60:.1f}h)\n"
    relatorio += f"Tempo de Acerto: {metricas['tempo_total_acerto']} min ({metricas['tempo_total_acerto']/60:.1f}h)\n"  # MUDANÇA: Renomeado
    relatorio += f"Quantidade Total Produzida: {metricas['qtd_total_produzida']:,.0f} peças\n"
    
    if metricas['qtd_total_acerto'] > 0:
        relatorio += f"Quantidade Total Acerto: {metricas['qtd_total_acerto']:,.0f} peças\n"
    
    # DESTAQUE ESPECIAL PARA EFICIÊNCIA DE TEMPO
    relatorio += "\n" + "🎯 " + "="*50 + "\n"
    relatorio += f"║  EFICIÊNCIA DE TEMPO: {metricas['eficiencia_tempo']:.1f}% {obter_classificacao_eficiencia(metricas['eficiencia_tempo'])} ║\n"
    relatorio += "🎯 " + "="*50 + "\n\n"
    
    relatorio += f"Velocidade Real: {metricas['velocidade_real']:,.0f} p/h\n"
    relatorio += f"Velocidade Nominal Média: {metricas['velocidade_media_ponderada']:,.0f} p/h\n"
    relatorio += f"Eficiência de Velocidade: {metricas['eficiencia_velocidade']:.1f}%\n\n"
    
    return relatorio

def gerar_secao_ops_melhorada(ops_analise, grupos_para_analise):
    """Gera seção de análise por OP com melhorias solicitadas"""
    relatorio = "🎯 ANÁLISE POR ORDEM DE PRODUÇÃO\n"
    relatorio += "=" * 80 + "\n\n"
    
    for op_key, grupos_op in ops_analise.items():
        # CORREÇÃO: Mantém formato original dos números (118.951, 119.000)
        op_numero_original = extrair_op_numero_original(grupos_op)
        relatorio += f"📋 OP {op_numero_original}\n"
        relatorio += "─" * 40 + "\n"
        
        # Consolida dados da OP
        dados_op = consolidar_dados_op(grupos_op)
        
        # Informações da OP
        relatorio += f"Cliente: {dados_op['cliente']}\n"  
        relatorio += f"Processo: {dados_op['processo']}\n"
        relatorio += f"Tempo Produção: {dados_op['tempo_producao']} min ({dados_op['tempo_producao']/60:.1f}h)\n"
        
        # MELHORIA: Mostrar tempo de setup disponível vs utilizado
        tempo_setup_disponivel = calcular_tempo_setup_disponivel(dados_op['processo'])
        if dados_op['tempo_setup'] > 0:
            relatorio += f"Tempo de Setup: {tempo_setup_disponivel} min\n"  # Disponível
            relatorio += f"Tempo de Setup Utilizado: {dados_op['tempo_setup']} min ({dados_op['tempo_setup']/60:.1f}h)\n"  # Real utilizado
        
        relatorio += f"Qtd Produzida: {dados_op['qtd_produzida']:,.0f} peças\n"
        
        if dados_op['qtd_acerto'] > 0:
            relatorio += f"Qtd Acerto: {dados_op['qtd_acerto']:,.0f} peças\n"
        
        if dados_op['tempo_producao'] > 0:
            relatorio += f"Velocidade Real: {dados_op['velocidade_real']:,.0f} p/h\n"
            relatorio += f"Velocidade Nominal: {dados_op['velocidade_nominal']:,.0f} p/h\n"
            relatorio += f"Eficiência: {dados_op['eficiencia']:.1f}% {obter_classificacao_eficiencia(dados_op['eficiencia'])}\n"
        
        # MELHORIA: Formato simplificado dos grupos
        relatorio += "\n📁 Grupos desta OP:\n"
        grupos_acerto = []
        grupos_producao = []
        
        for nome_grupo, dados in grupos_op:
            # Extrai números das linhas do grupo
            linhas_str = ", ".join([str(l+1) for l in dados['linhas']])
            
            if dados['tem_acerto']:
                grupos_acerto.append(linhas_str)
            if dados['tem_producao']:
                grupos_producao.append(linhas_str)
        
        if grupos_acerto:
            relatorio += f"  • Acerto: linha(s) {', '.join(grupos_acerto)}\n"
        if grupos_producao:
            relatorio += f"  • Produção: linha(s) {', '.join(grupos_producao)}\n"
        
        relatorio += "\n"
    
    return relatorio

def extrair_op_numero_original(grupos_op):
    """Extrai o número original da OP mantendo formato (118.951, 119.000)"""
    for nome_grupo, dados in grupos_op:
        os_original = dados.get('os_original', '') or dados.get('os', '')
        if os_original:
            return os_original
    return "N/A"

def calcular_tempo_setup_disponivel(processo):
    """Calcula tempo de setup disponível baseado no processo (placeholder)"""
    # Esta função pode ser expandida com lógica específica
    # Por enquanto, retorna um valor baseado no tipo de processo
    if not processo:
        return 120  # Padrão de 2 horas
    
    # Pode implementar lógica específica baseada no processo
    if "FUNDO AUTOMÁ" in processo:
        return 130
    elif "COLAGEM" in processo:
        return 180
    else:
        return 120

def consolidar_dados_op(grupos_op):
    """Consolida dados de todos os grupos de uma OP"""
    dados_op = {
        'tempo_producao': 0,
        'tempo_setup': 0,
        'qtd_produzida': 0,
        'qtd_acerto': 0,
        'velocidade_nominal': 0,
        'cliente': "",
        'processo': "",
        'velocidade_real': 0,
        'eficiencia': 0
    }
    
    for nome_grupo, dados in grupos_op:
        dados_op['tempo_producao'] += dados['tempo_total_producao']
        dados_op['tempo_setup'] += dados['tempo_setup']
        dados_op['qtd_produzida'] += dados['qtd_produzida']
        dados_op['qtd_acerto'] += dados['qtd_acerto']
        
        # Pega informações do primeiro grupo que tiver
        if dados['velocidade_nominal'] > 0 and dados_op['velocidade_nominal'] == 0:
            dados_op['velocidade_nominal'] = dados['velocidade_nominal']
        if dados['cliente'] and not dados_op['cliente']:
            dados_op['cliente'] = dados['cliente']
        if dados['processo'] and not dados_op['processo']:
            dados_op['processo'] = dados['processo']
    
    # Calcula velocidade real e eficiência
    if dados_op['tempo_producao'] > 0:
        dados_op['velocidade_real'] = dados_op['qtd_produzida'] / (dados_op['tempo_producao']/60)
        if dados_op['velocidade_nominal'] > 0:
            dados_op['eficiencia'] = dados_op['velocidade_real'] / dados_op['velocidade_nominal'] * 100
    
    return dados_op

def obter_classificacao_eficiencia(eficiencia):
    """Retorna classificação visual da eficiência"""
    if eficiencia >= 90:
        return "🟢 EXCELENTE"
    elif eficiencia >= 80:
        return "🔵 BOA"
    elif eficiencia >= 70:
        return "🟡 REGULAR"
    elif eficiencia >= 60:
        return "🟠 BAIXA"
    else:
        return "🔴 CRÍTICA"