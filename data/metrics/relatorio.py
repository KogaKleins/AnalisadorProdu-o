# Arquivo: data/metrics/relatorio.py
from datetime import datetime
import re
from config.setup_config import tempos_setup

def gerar_relatorio(grupos_para_analise, ops_analise, hora_inicio, hora_fim, intervalo):
    """Gera relatório com cálculos corrigidos e estrutura reorganizada"""
    
    # Calcula tempo disponível
    tempo_disponivel = calcular_tempo_disponivel(hora_inicio, hora_fim, intervalo)
    
    # Cabeçalho do relatório
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
    relatorio = f"📊 RELATÓRIO DE DESEMPENHO - {data_atual}\n"
    relatorio += "=" * 80 + "\n\n"
    
    # Seção de período de trabalho
    relatorio += gerar_secao_periodo(hora_inicio, hora_fim, intervalo, tempo_disponivel)
    
    # Calcula métricas gerais
    metricas_gerais = calcular_metricas_gerais(grupos_para_analise, ops_analise, tempo_disponivel)
    
    # Seção de resumo geral - NOVA ESTRUTURA
    relatorio += gerar_secao_resumo_geral_corrigido(metricas_gerais, tempo_disponivel)
    
    # NOVA: Seção de médias gerais simplificada
    if ops_analise:
        relatorio += gerar_secao_medias_gerais_simplificada(ops_analise)
    
    # Seção de análise por OP - CORRIGIDA
    if ops_analise:
        relatorio += gerar_secao_ops_corrigida(ops_analise, grupos_para_analise)
    
    return relatorio

def calcular_tempo_disponivel(hora_inicio, hora_fim, intervalo):
    """Calcula tempo disponível em minutos, aceitando vários formatos de hora/data"""
    import re
    def extrair_hora_minuto(valor):
        valor = valor.strip()
        # Aceita 'HH:MM', 'dd/mm/yyyy HH:MM', 'dd/mm/yyyy - HH:MM', etc.
        match = re.search(r"(\d{2}):(\d{2})$", valor)
        if match:
            h, m = int(match.group(1)), int(match.group(2))
            return h * 60 + m
        raise ValueError(f"Formato de hora inválido: {valor}")
    inicio_min = extrair_hora_minuto(hora_inicio)
    fim_min = extrair_hora_minuto(hora_fim)
    return fim_min - inicio_min - int(intervalo)

def gerar_secao_periodo(hora_inicio, hora_fim, intervalo, tempo_disponivel):
    """Gera seção do período de trabalho"""
    relatorio = "⏰ PERÍODO DE TRABALHO\n"
    relatorio += "─" * 40 + "\n"
    relatorio += f"Início: {hora_inicio}\n"
    relatorio += f"Fim: {hora_fim}\n"
    relatorio += f"Intervalo: {intervalo} min\n"
    relatorio += f"Tempo Disponível: {tempo_disponivel} min ({tempo_disponivel/60:.1f}h)\n\n"
    return relatorio

def calcular_metricas_gerais(grupos_para_analise, ops_analise, tempo_disponivel):
    """Calcula métricas gerais com as novas fórmulas"""
    metricas = {
        'tempo_total_producao': 0,
        'tempo_total_acerto': 0,
        'qtd_total_produzida': 0,
        'tempo_total_perdido_ganho': 0,
        'eficiencia_producao': 0,
        'eficiencia_acerto': 0,
        'eficiencia_tempo_geral': 0,
        'tempo_ocioso': 0
    }
    # Soma tempos diretamente dos detalhes dos eventos
    tempo_total_producao = 0
    tempo_total_acerto = 0
    qtd_total_produzida = 0
    for dados in grupos_para_analise.values():
        for detalhe in dados.get('detalhes_eventos', []):
            if detalhe.get('is_producao'):
                tempo_total_producao += detalhe.get('tempo_producao', 0)
                qtd_total_produzida += detalhe.get('qtd_produzida', 0)
            if detalhe.get('is_acerto'):
                # Corrigido: usar tempo_producao para acerto (coluna Tempo)
                tempo_total_acerto += detalhe.get('tempo_producao', 0)
    metricas['tempo_total_producao'] = tempo_total_producao
    metricas['tempo_total_acerto'] = tempo_total_acerto
    metricas['qtd_total_produzida'] = qtd_total_produzida
    # Tempo ocioso: tempo_disponivel - (tempo_total_producao + tempo_total_acerto)
    metricas['tempo_ocioso'] = tempo_disponivel - (tempo_total_producao + tempo_total_acerto)

    # Calcula atraso/ganho geral das OPs e eficiências
    if ops_analise:
        soma_atraso_ops = 0
        soma_eficiencia_producao = 0
        soma_eficiencia_acerto = 0
        count_ops_producao = 0
        count_ops_acerto = 0
        
        for op_key, grupos_op in ops_analise.items():
            dados_op = consolidar_dados_op(grupos_op)
            
            # Calcula atraso/ganho da produção desta OP
            if dados_op['tempo_producao'] > 0 and dados_op['velocidade_nominal'] > 0:
                tempo_programado_producao = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
                atraso_producao = dados_op['tempo_producao'] - tempo_programado_producao
                
                # Calcula eficiência de produção desta OP (nova fórmula)
                eficiencia_producao_op = ((tempo_programado_producao - dados_op['tempo_producao'] + tempo_programado_producao) / tempo_programado_producao) * 100
                soma_eficiencia_producao += eficiencia_producao_op
                count_ops_producao += 1
                
                # Acumula no atraso geral
                soma_atraso_ops += atraso_producao
            
            # NOVA LÓGICA PARA ACERTO - CORREÇÃO IMPLEMENTADA
            tempo_setup_programado = calcular_tempo_setup_programado(dados_op['processo'])
            if dados_op['tempo_setup'] > 0:
                diferenca_setup = tempo_setup_programado - dados_op['tempo_setup']
                
                # NOVA REGRA: Só conta ganho se tiver produção na mesma OP
                tem_producao_na_op = dados_op['tempo_producao'] > 0
                
                if diferenca_setup > 0:  # Seria ganho
                    if tem_producao_na_op:
                        # Tem produção: conta o ganho real
                        atraso_acerto = -diferenca_setup  # Negativo = ganho
                        eficiencia_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                    else:
                        # Não tem produção: considera 100% (sem ganho nem perda)
                        atraso_acerto = 0  # Zero = sem ganho nem perda
                        eficiencia_acerto_op = 100  # 100% = exato
                else:  # É atraso
                    # Atraso sempre conta, independente de ter produção
                    atraso_acerto = -diferenca_setup  # Positivo = atraso
                    eficiencia_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                
                soma_eficiencia_acerto += eficiencia_acerto_op
                count_ops_acerto += 1
                
                # Acumula no atraso geral
                soma_atraso_ops += atraso_acerto
        
        # Calcula médias das eficiências
        if count_ops_producao > 0:
            metricas['eficiencia_producao'] = soma_eficiencia_producao / count_ops_producao
        
        if count_ops_acerto > 0:
            metricas['eficiencia_acerto'] = soma_eficiencia_acerto / count_ops_acerto
        
        # Tempo total perdido/ganho = soma atrasos OPs + tempo ocioso
        metricas['tempo_total_perdido_ganho'] = soma_atraso_ops + metricas['tempo_ocioso']
        
        # Eficiência de tempo geral (fórmula corrigida)
        if tempo_disponivel > 0:
            tempo_efetivo_final = tempo_disponivel - metricas['tempo_total_perdido_ganho']
            metricas['eficiencia_tempo_geral'] = (tempo_efetivo_final / tempo_disponivel) * 100
    
    return metricas

def gerar_secao_resumo_geral_corrigido(metricas, tempo_disponivel):
    """Gera seção do resumo geral com nova estrutura"""
    relatorio = "📈 RESUMO GERAL\n"
    relatorio += "─" * 40 + "\n"
    relatorio += f"Tempo Total Produção: {metricas['tempo_total_producao']} min ({metricas['tempo_total_producao']/60:.1f}h)\n"
    relatorio += f"Tempo Total de Acerto: {metricas['tempo_total_acerto']} min ({metricas['tempo_total_acerto']/60:.1f}h)\n"
    # CORREÇÃO: Remover o espaço entre vírgula e ponto na formatação
    relatorio += f"Quantidade Total Produzida: {metricas['qtd_total_produzida']:,.0f} unidades\n"
    # Tempo total perdido ou ganho
    if metricas['tempo_total_perdido_ganho'] >= 0:
        relatorio += f"Tempo Total Perdido: {metricas['tempo_total_perdido_ganho']:.0f} min\n"
    else:
        relatorio += f"Tempo Total Ganho: {abs(metricas['tempo_total_perdido_ganho']):.0f} min\n"
    relatorio += f"Eficiência de Produção: {metricas['eficiencia_producao']:.1f}%\n"
    relatorio += f"Eficiência de Acerto: {metricas['eficiencia_acerto']:.1f}%\n"
    relatorio += f"Tempo Ocioso: {metricas['tempo_ocioso']} min ({metricas['tempo_ocioso']/60:.1f}h)\n"
    # Eficiência de tempo geral - DESTACADA
    relatorio += "\n🎯 " + "="*60 + "\n"
    relatorio += f"║        EFICIÊNCIA DE TEMPO GERAL: {metricas['eficiencia_tempo_geral']:.2f}% {obter_classificacao_eficiencia(metricas['eficiencia_tempo_geral'])}        ║\n"
    relatorio += "🎯 " + "="*60 + "\n\n"
    return relatorio

def gerar_secao_medias_gerais_simplificada(ops_analise):
    """Seção simplificada das médias gerais"""
    relatorio = "🎯 MÉDIAS GERAIS DE TODAS AS OPs\n"
    relatorio += "=" * 60 + "\n"
    
    # Calcula apenas a média de acerto COM NOVA LÓGICA
    total_tempo_setup_programado = 0
    total_tempo_setup_utilizado = 0
    total_eficiencia_acerto = 0
    count_ops_acerto = 0
    
    for op_key, grupos_op in ops_analise.items():
        dados_op = consolidar_dados_op(grupos_op)
        
        # Calcula tempo de setup programado para esta OP
        tempo_setup_programado = calcular_tempo_setup_programado(dados_op['processo'])
        
        if dados_op['tempo_setup'] > 0:
            diferenca_setup = tempo_setup_programado - dados_op['tempo_setup']
            tem_producao_na_op = dados_op['tempo_producao'] > 0
            
            if diferenca_setup > 0:  # Seria ganho
                if tem_producao_na_op:
                    # Tem produção: conta o ganho real
                    eficiencia_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                    total_tempo_setup_programado += tempo_setup_programado
                    total_tempo_setup_utilizado += dados_op['tempo_setup']
                else:
                    # Não tem produção: considera 100%
                    eficiencia_acerto_op = 100
                    total_tempo_setup_programado += tempo_setup_programado
                    total_tempo_setup_utilizado += tempo_setup_programado  # Como se fosse exato
            else:  # É atraso
                # Atraso sempre conta
                eficiencia_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                total_tempo_setup_programado += tempo_setup_programado
                total_tempo_setup_utilizado += dados_op['tempo_setup']
            
            total_eficiencia_acerto += eficiencia_acerto_op
            count_ops_acerto += 1
    
    if count_ops_acerto > 0:
        media_acerto_percent = total_eficiencia_acerto / count_ops_acerto
        diferenca_acerto = total_tempo_setup_programado - total_tempo_setup_utilizado
        
        relatorio += "⚙️ MÉDIA DE ACERTO (com nova lógica):\n"
        relatorio += f"  • Média de Acerto: {media_acerto_percent:.1f}%\n"
        
        if diferenca_acerto > 0:
            relatorio += f"  • Tempo economizado: {diferenca_acerto} min\n"
            relatorio += f"  • Observação: Ganhos só contam quando há produção na mesma OP\n\n"
        else:
            relatorio += f"  • Tempo perdido: {abs(diferenca_acerto)} min\n\n"
    
    return relatorio

def gerar_secao_ops_corrigida(ops_analise, grupos_para_analise):
    """Gera seção de análise por OP com fórmulas corrigidas"""
    relatorio = "🎯 ANÁLISE DETALHADA POR ORDEM DE PRODUÇÃO\n"
    relatorio += "=" * 80 + "\n\n"
    
    for op_key, grupos_op in ops_analise.items():
        # Mantém formato original dos números
        op_numero_original = extrair_op_numero_original(grupos_op)
        relatorio += f"📋 OP {op_numero_original}\n"
        relatorio += "─" * 60 + "\n"
        
        # Consolida dados da OP
        dados_op = consolidar_dados_op(grupos_op)
        
        # Informações da OP
        relatorio += f"Cliente: {dados_op['cliente']}\n"  
        relatorio += f"Processo: {dados_op['processo']}\n"
        
        # Calcula tempo de setup programado
        tempo_setup_programado = calcular_tempo_setup_programado(dados_op['processo'])
        
        relatorio += f"Tempo Produção: {dados_op['tempo_producao']} min ({dados_op['tempo_producao']/60:.1f}h)\n"
        relatorio += f"Tempo de Setup Programado: {tempo_setup_programado} min\n"
        relatorio += f"Tempo de Setup Utilizado: {dados_op['tempo_setup']} min\n"
        
        # NOVA LÓGICA PARA MOSTRAR GANHO/PERDA
        diferenca_acerto = tempo_setup_programado - dados_op['tempo_setup']
        tem_producao_na_op = dados_op['tempo_producao'] > 0
        
        if diferenca_acerto > 0:  # Seria ganho
            if tem_producao_na_op:
                relatorio += f"Ganho de Setup: {diferenca_acerto} min (VÁLIDO - há produção)\n"
            else:
                relatorio += f"Setup aparentemente ganho: {diferenca_acerto} min (NÃO VÁLIDO - sem produção, conta como 100%)\n"
        elif diferenca_acerto < 0:
            relatorio += f"Perda de Setup: {abs(diferenca_acerto)} min (VÁLIDO - atraso sempre conta)\n"
        else:
            relatorio += f"Setup no tempo exato.\n"
        
        # CORREÇÃO: Usar formatação correta para quantidade produzida
        relatorio += f"Qtd Produzida: {dados_op['qtd_produzida']:,.0f}\n\n"
        
        # Inicialização para evitar erro de variável não associada
        media_producao_op = 0.0
        minutos_diferenca_producao = 0.0
        # NOVA FÓRMULA DE PRODUÇÃO
        if dados_op['tempo_producao'] > 0 and dados_op['velocidade_nominal'] > 0:
            # Tempo programado de produção
            tempo_programado_producao = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
            
            # Nova fórmula: (tempo programado - tempo utilizado + tempo programado) / tempo programado * 100
            media_producao_op = ((tempo_programado_producao - dados_op['tempo_producao'] + tempo_programado_producao) / tempo_programado_producao) * 100
            minutos_diferenca_producao = tempo_programado_producao - dados_op['tempo_producao']
            
            relatorio += "📊 MÉDIA DE PRODUÇÃO DA OP:\n"
            relatorio += f"  • {media_producao_op:.2f}%\n"
            
            if minutos_diferenca_producao > 0:
                relatorio += f"  • Minutos ganhos: {minutos_diferenca_producao:.0f} min\n\n"
            else:
                relatorio += f"  • Minutos perdidos: {abs(minutos_diferenca_producao):.0f} min\n\n"
        
        # NOVA FÓRMULA DE ACERTO COM LÓGICA CORRIGIDA
        if dados_op['tempo_setup'] > 0:
            if diferenca_acerto > 0:  # Seria ganho
                if tem_producao_na_op:
                    # Tem produção: conta o ganho real
                    media_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                    relatorio += "⚙️ MÉDIA DE ACERTO DA OP:\n"
                    relatorio += f"  • {media_acerto_op:.1f}%\n"
                    relatorio += f"  • Minutos ganhos: {diferenca_acerto} min (VÁLIDO)\n\n"
                else:
                    # Não tem produção: considera 100%
                    media_acerto_op = 100.0
                    relatorio += "⚙️ MÉDIA DE ACERTO DA OP:\n"
                    relatorio += f"  • {media_acerto_op:.1f}% (considerado como exato - sem produção)\n"
                    relatorio += f"  • Observação: Ganho não contabilizado pois não há produção\n\n"
            else:  # É atraso
                # Atraso sempre conta
                media_acerto_op = ((tempo_setup_programado - dados_op['tempo_setup'] + tempo_setup_programado) / tempo_setup_programado) * 100
                relatorio += "⚙️ MÉDIA DE ACERTO DA OP:\n"
                relatorio += f"  • {media_acerto_op:.1f}%\n"
                relatorio += f"  • Minutos perdidos: {abs(diferenca_acerto)} min (VÁLIDO)\n\n"
            
            # MÉDIA FINAL DA OP
            if dados_op['tempo_producao'] > 0:
                media_final_op = (media_producao_op + media_acerto_op) / 2
                
                relatorio += "🎯 MÉDIA FINAL DA OP:\n"
                relatorio += f"  • Média: {media_final_op:.1f}% {obter_classificacao_eficiencia(media_final_op)}\n"
                relatorio += f"  • Fórmula: {media_producao_op:.1f}% + {media_acerto_op:.1f}% / 2 = {media_final_op:.1f}%\n"
                relatorio += f"    - Produção: {minutos_diferenca_producao:.0f} min\n"
                relatorio += f"    - Acerto: {diferenca_acerto} min\n\n"
        else:
            if dados_op['tempo_producao'] > 0:
                relatorio += f"🎯 EFICIÊNCIA DA OP (apenas produção): {media_producao_op:.1f}% {obter_classificacao_eficiencia(media_producao_op)}\n\n"
        
        # Formato simplificado dos grupos
        relatorio += "📁 Grupos desta OP:\n"
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
        
        relatorio += "\n" + "="*60 + "\n\n"
    
    return relatorio

def extrair_op_numero_original(grupos_op):
    """Extrai o número original da OP mantendo formato"""
    for nome_grupo, dados in grupos_op:
        os_original = dados.get('os_original', '') or dados.get('os', '')
        if os_original:
            return os_original
    return "N/A"

def calcular_tempo_setup_programado(processo):
    """Calcula tempo de setup programado baseado no processo e configurações"""
    if not processo:
        return tempos_setup.get('default', 180)
    
    processo_lower = processo.lower()
    
    # Mapeia processos para configurações
    if "berço" in processo_lower or "berco" in processo_lower:
        return tempos_setup.get('berco', 180)
    elif "fundo automá" in processo_lower or "fundo automa" in processo_lower:
        return tempos_setup.get('fundo_automatico_primeiro', 130)
    elif "colagem" in processo_lower:
        if "bandeja" in processo_lower:
            return tempos_setup.get('colagem_bandeja', 130)
        elif "lateral" in processo_lower:
            return tempos_setup.get('colagem_lateral_primeiro', 130)
        else:
            return tempos_setup.get('colagem_bandeja', 130)
    else:
        return tempos_setup.get('default', 180)

def consolidar_dados_op(grupos_op):
    """Consolida dados de todos os grupos de uma OP"""
    dados_op = {
        'tempo_producao': 0,
        'tempo_setup': 0,
        'qtd_produzida': 0,
        'qtd_acerto': 0,
        'velocidade_nominal': 0,
        'cliente': "",
        'processo': ""
    }
    
    for nome_grupo, dados in grupos_op:
        dados_op['tempo_producao'] += dados['tempo_total_producao']
        # CORREÇÃO: Somar o tempo real de setup dos detalhes de eventos
        # em vez de usar o campo tempo_setup que pode estar incorreto
        for detalhe in dados.get('detalhes_eventos', []):
            if detalhe.get('is_acerto'):
                dados_op['tempo_setup'] += detalhe.get('tempo_producao', 0)
        
        dados_op['qtd_produzida'] += dados['qtd_produzida']
        dados_op['qtd_acerto'] += dados['qtd_acerto']
        
        # Pega informações do primeiro grupo que tiver
        if dados['velocidade_nominal'] > 0 and dados_op['velocidade_nominal'] == 0:
            dados_op['velocidade_nominal'] = dados['velocidade_nominal']
        if dados['cliente'] and not dados_op['cliente']:
            dados_op['cliente'] = dados['cliente']
        if dados['processo'] and not dados_op['processo']:
            dados_op['processo'] = dados['processo']
    
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