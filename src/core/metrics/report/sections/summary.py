"""
Summary section generation module.
Contains functions for generating the general summary section of the report.
"""

from .efficiency import get_efficiency_classification

def generate_general_summary(metrics, tempo_disponivel):
    """Generate general summary section with new structure"""
    section = "📈 RESUMO GERAL\n"
    section += "─" * 40 + "\n"
    
    # Production and setup times
    section += f"Tempo Total Produção: {metrics['tempo_total_producao']} min ({metrics['tempo_total_producao']/60:.1f}h)\n"
    section += f"Tempo Total de Acerto: {metrics['tempo_total_acerto']} min ({metrics['tempo_total_acerto']/60:.1f}h)\n"
    
    # Total quantity produced
    section += f"Quantidade Total Produzida: {metrics['qtd_total_produzida']:,.0f} unidades\n"
    
    # Total time lost/gained
    if metrics['tempo_total_perdido_ganho'] >= 0:
        section += f"Tempo Total Perdido: {metrics['tempo_total_perdido_ganho']:.0f} min\n"
    else:
        section += f"Tempo Total Ganho: {abs(metrics['tempo_total_perdido_ganho']):.0f} min\n"
    
    # Efficiencies
    section += f"Eficiência de Produção: {metrics['eficiencia_producao']:.1f}%\n"
    section += f"Eficiência de Acerto: {metrics['eficiencia_acerto']:.1f}%\n"
    section += f"Tempo Ocioso: {metrics['tempo_ocioso']} min ({metrics['tempo_ocioso']/60:.1f}h)\n"
    
    # Overall time efficiency - HIGHLIGHTED
    section += "\n🎯 " + "="*60 + "\n"
    classification = get_efficiency_classification(metrics['eficiencia_tempo_geral'])
    section += f"║        EFICIÊNCIA DE TEMPO GERAL: {metrics['eficiencia_tempo_geral']:.2f}% {classification}        ║\n"
    section += "🎯 " + "="*60 + "\n\n"
    
    return section
