"""
Period section handling module.
Contains functions for time calculations and period section generation.
"""

def calculate_available_time(hora_inicio, hora_fim, intervalo):
    """Calculate available time in minutes"""
    def minutes(hora):
        h, m = map(int, hora.split(':'))
        return h * 60 + m
    
    inicio_min = minutes(hora_inicio)
    fim_min = minutes(hora_fim)
    return fim_min - inicio_min - intervalo

def generate_period_section(hora_inicio, hora_fim, intervalo, tempo_disponivel):
    """Generate period section of the report"""
    section = "⏰ PERÍODO DE TRABALHO\n"
    section += "─" * 40 + "\n"
    section += f"Início: {hora_inicio}\n"
    section += f"Fim: {hora_fim}\n"
    section += f"Intervalo: {intervalo} min\n"
    section += f"Tempo Disponível: {tempo_disponivel} min ({tempo_disponivel/60:.1f}h)\n\n"
    return section
