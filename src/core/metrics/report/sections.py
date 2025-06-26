"""
Módulo responsável por gerar as seções do relatório de produção.
"""

from datetime import datetime

def gerar_secao_periodo(hora_inicio: str, hora_fim: str, intervalo: int, tempo_disponivel: int) -> str:
    """
    Gera a seção do relatório que descreve o período de trabalho.
    
    Args:
        hora_inicio (str): Hora de início no formato HH:MM
        hora_fim (str): Hora de fim no formato HH:MM
        intervalo (int): Duração do intervalo em minutos
        tempo_disponivel (int): Tempo disponível total em minutos
        
    Returns:
        str: Texto formatado da seção do período
    """
    relatorio = "⏰ PERÍODO DE TRABALHO\n"
    relatorio += "─" * 40 + "\n"
    relatorio += f"Início: {hora_inicio}\n"
    relatorio += f"Fim: {hora_fim}\n"
    relatorio += f"Intervalo: {intervalo} min\n"
    relatorio += f"Tempo Disponível: {tempo_disponivel} min ({tempo_disponivel/60:.1f}h)\n\n"
    return relatorio

def gerar_secao_resumo_geral(metricas: dict, tempo_disponivel: int) -> str:
    """
    Gera a seção de resumo geral do relatório.
    
    Args:
        metricas (dict): Dicionário com as métricas calculadas
        tempo_disponivel (int): Tempo disponível total em minutos
        
    Returns:
        str: Texto formatado da seção de resumo
    """
    relatorio = "📈 RESUMO GERAL\n"
    relatorio += "─" * 40 + "\n"
    
    # Tempos
    relatorio += f"Tempo Total de Produção: {metricas['tempo_total_producao']} min\n"
    relatorio += f"Tempo Total de Acerto: {metricas['tempo_total_acerto']} min\n"
    relatorio += f"Tempo Ocioso: {metricas['tempo_ocioso']} min\n\n"
    
    # Eficiências
    relatorio += f"Eficiência Geral: {metricas['eficiencia_tempo_geral']:.1f}%\n"
    relatorio += f"Eficiência de Produção: {metricas['eficiencia_producao']:.1f}%\n"
    relatorio += f"Eficiência de Acerto: {metricas['eficiencia_acerto']:.1f}%\n\n"
    
    # Produção
    relatorio += f"Quantidade Total Produzida: {metricas['qtd_total_produzida']:,}\n"
    if metricas['tempo_total_perdido_ganho'] != 0:
        tempo_perdido = f"{'PERDIDO' if metricas['tempo_total_perdido_ganho'] > 0 else 'GANHO'}"
        relatorio += f"Tempo Total {tempo_perdido}: {abs(metricas['tempo_total_perdido_ganho']):.1f} min\n"
    
    return relatorio

def gerar_secao_ops(ops_analise: dict, grupos_para_analise: dict) -> str:
    """
    Gera a seção de análise por OP do relatório.
    
    Args:
        ops_analise (dict): Dicionário com as OPs analisadas
        grupos_para_analise (dict): Dicionário com os grupos de análise
        
    Returns:
        str: Texto formatado da seção de OPs
    """
    if not ops_analise:
        return ""
        
    relatorio = "\n📋 ANÁLISE POR OP\n"
    relatorio += "─" * 40 + "\n\n"
    
    for op_key, grupos_op in ops_analise.items():
        relatorio += f"🔹 {op_key}\n"
        
        tempo_total = 0
        qtd_total = 0
        tem_acerto = False
        velocidade_nominal = 0
        
        for nome_grupo, dados in grupos_op:
            if dados.get('tem_producao'):
                tempo_total += dados.get('tempo_total_producao', 0)
                qtd_total += dados.get('qtd_produzida', 0)
                velocidade_nominal = dados.get('velocidade_nominal', 0)
            if dados.get('tem_acerto'):
                tem_acerto = True
        
        relatorio += f"   Quantidade Total: {qtd_total:,}\n"
        relatorio += f"   Tempo Total: {tempo_total} min\n"
        
        if velocidade_nominal > 0:
            tempo_programado = (qtd_total / velocidade_nominal) * 60
            atraso = tempo_total - tempo_programado
            status = "ATRASO" if atraso > 0 else "GANHO"
            relatorio += f"   {status}: {abs(atraso):.1f} min\n"
            
        if tem_acerto:
            relatorio += "   ⚠️ Contém acerto(s)\n"
            
        relatorio += "\n"
    
    return relatorio
