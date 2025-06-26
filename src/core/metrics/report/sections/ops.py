"""
OP analysis module.
Contains functions for generating the OP analysis section of the report.
"""

from .efficiency import (
    calculate_op_metrics,
    get_efficiency_classification,
    calculate_setup_time,
    consolidar_dados_op
)

def generate_ops_section(ops_analise, grupos_para_analise):
    """Generate OPs analysis section with corrected formulas"""
    section = "🎯 ANÁLISE DETALHADA POR ORDEM DE PRODUÇÃO\n"
    section += "=" * 80 + "\n\n"
    
    for op_key, grupos_op in ops_analise.items():
        # Keep original number format
        op_numero_original = extract_op_number_original(grupos_op)
        section += f"📋 OP {op_numero_original}\n"
        section += "─" * 60 + "\n"
        
        # Consolidate OP data
        dados_op = consolidar_dados_op(grupos_op)
        section += generate_op_info(dados_op)
        
        # Calculate programmed setup time
        tempo_setup_programado = calculate_setup_time(dados_op['processo'])
        section += generate_setup_analysis(dados_op, tempo_setup_programado)
        
        # Add production info
        section += generate_production_info(dados_op)
        
        # Add groups summary
        section += generate_groups_summary(grupos_op)
        section += "\n" + "="*60 + "\n\n"
    
    return section

def extract_op_number_original(grupos_op):
    """Extract original OP number keeping format"""
    for nome_grupo, dados in grupos_op:
        os_original = dados.get('os_original', '') or dados.get('os', '')
        if os_original:
            return os_original
    return "N/A"

def generate_op_info(dados_op):
    """Generate basic OP information"""
    info = f"Cliente: {dados_op['cliente']}\n"
    info += f"Processo: {dados_op['processo']}\n"
    if dados_op['velocidade_nominal'] > 0:
        info += f"Velocidade Nominal: {dados_op['velocidade_nominal']:.0f} un/h\n"
    return info

def generate_setup_analysis(dados_op, tempo_setup_programado):
    """Generate setup analysis information"""
    analysis = ""
    
    if dados_op['tem_acerto']:
        analysis += "\n⚙️ ANÁLISE DE SETUP\n"
        analysis += f"Tempo Setup Programado: {tempo_setup_programado} min\n"
        analysis += f"Tempo Setup Real: {dados_op['tempo_setup']:.0f} min\n"
        
        # Calculate setup efficiency
        if tempo_setup_programado > 0:
            eficiencia_setup = (tempo_setup_programado / dados_op['tempo_setup']) * 100
            classification = get_efficiency_classification(eficiencia_setup)
            analysis += f"Eficiência Setup: {eficiencia_setup:.1f}% {classification}\n"
        
        if dados_op['tempo_setup'] > tempo_setup_programado:
            atraso = dados_op['tempo_setup'] - tempo_setup_programado
            analysis += f"⚠️ Atraso Setup: {atraso:.0f} min\n"
        else:
            ganho = tempo_setup_programado - dados_op['tempo_setup']
            analysis += f"✨ Ganho Setup: {ganho:.0f} min\n"
    
    return analysis

def generate_production_info(dados_op):
    """Generate production information"""
    info = "\n🏭 ANÁLISE DE PRODUÇÃO\n"
    info += f"Quantidade Produzida: {dados_op['qtd_produzida']:,.0f} un\n"
    info += f"Tempo Total de Produção: {dados_op['tempo_total_producao']:.0f} min\n"
    
    if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
        tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
        atraso = dados_op['tempo_total_producao'] - tempo_programado
        
        info += f"Tempo Programado: {tempo_programado:.0f} min\n"
        
        if atraso > 0:
            info += f"⚠️ Atraso Produção: {atraso:.0f} min\n"
        else:
            info += f"✨ Ganho Produção: {abs(atraso):.0f} min\n"
            
        # Calculate and show production efficiency
        if tempo_programado > 0:
            eficiencia = (tempo_programado / dados_op['tempo_total_producao']) * 100
            classification = get_efficiency_classification(eficiencia)
            info += f"\nEficiência de Produção: {eficiencia:.1f}% {classification}\n"
    
    return info

def generate_groups_summary(grupos_op):
    """Generate summary of all groups in the OP"""
    summary = "\n📊 GRUPOS DE EVENTOS\n"
    
    for nome_grupo, dados in grupos_op:
        summary += f"\n▫️ {nome_grupo}\n"
        if dados['tem_producao']:
            summary += f"  Produção: {dados['qtd_produzida']:,.0f} un em {dados['tempo_total_producao']:.0f} min\n"
        if dados['tem_acerto']:
            summary += f"  Setup: {dados['tempo_setup']:.0f} min\n"
    
    return summary
