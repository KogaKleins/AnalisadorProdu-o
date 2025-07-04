"""
Summary section generation module.
Contains functions for generating the general summary section of the report.
"""

from .efficiency import get_efficiency_classification

def generate_general_summary(metrics, tempo_disponivel):
    """Generate general summary section with improved layout and highlights"""
    section = "\n📈 RESUMO GERAL\n"
    section += "─" * 60 + "\n"
    section += f"⏱️  Tempo Total Produção:   {metrics['tempo_total_producao']:>5.0f} min  ({metrics['tempo_total_producao']/60:>4.1f}h)\n"
    section += f"🛠️  Tempo Total de Acerto:  {metrics['tempo_total_acerto']:>5.0f} min  ({metrics['tempo_total_acerto']/60:>4.1f}h)\n"
    section += f"📦  Quantidade Produzida:   {metrics['qtd_total_produzida']:>8,.0f} unidades\n"
    if metrics['tempo_total_perdido_ganho'] < 0:
        section += f"💡 Tempo Total Ganho:      {abs(metrics['tempo_total_perdido_ganho']):>5.0f} min\n"
    elif metrics['tempo_total_perdido_ganho'] > 0:
        section += f"⏳ Tempo Total Perdido:    {metrics['tempo_total_perdido_ganho']:>5.0f} min\n"
    else:
        section += f"⏳ Tempo Total Perdido:        0 min\n"
    section += f"⚡  Eficiência de Produção: {metrics['eficiencia_producao']:>6.1f}%\n"
    section += f"🔧  Eficiência de Acerto:   {metrics['eficiencia_acerto']:>6.1f}%\n"
    section += f"🕒  Tempo Ocioso:           {metrics['tempo_ocioso']:>5.0f} min  ({metrics['tempo_ocioso']/60:>4.1f}h)\n"
    section += "\n🎯 " + "="*59 + "\n"
    classification = get_efficiency_classification(metrics['eficiencia_tempo_geral'])
    section += f"║  EFICIÊNCIA DE TEMPO GERAL: {metrics['eficiencia_tempo_geral']:>7.2f}% {classification:<15} ║\n"
    section += "🎯 " + "="*59 + "\n\n"
    return section
