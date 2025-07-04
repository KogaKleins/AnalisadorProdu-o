"""
Period section handling module.
Contains functions for time calculations and period section generation.
"""

from datetime import datetime, timedelta
import re

def parse_datetime_or_time(value, default_date=None):
    """Parse 'HH:MM' or 'dd/mm/yyyy HH:MM' into datetime object."""
    value = value.strip()
    # Regex para data e hora
    match = re.match(r"(\d{2}/\d{2}/\d{4})?\s*-?\s*(\d{1,2}:\d{2})", value)
    if match:
        date_part, time_part = match.groups()
        if date_part:
            dt = datetime.strptime(f"{date_part} {time_part}", "%d/%m/%Y %H:%M")
        else:
            # Se não tem data, usa default_date (ou hoje)
            base = default_date or datetime.now()
            dt = base.replace(hour=int(time_part.split(":")[0]), minute=int(time_part.split(":")[1]), second=0, microsecond=0)
        return dt
    raise ValueError(f"Formato de data/hora inválido: {value}")

def calculate_available_time(hora_inicio, hora_fim, intervalo):
    """Calculate available time in minutes, supporting date+hour or just hour."""
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    dt_inicio = parse_datetime_or_time(hora_inicio, default_date=base_date)
    dt_fim = parse_datetime_or_time(hora_fim, default_date=dt_inicio)
    # Se fim < início, assume que terminou no dia seguinte
    if dt_fim <= dt_inicio:
        dt_fim += timedelta(days=1)
    total = int((dt_fim - dt_inicio).total_seconds() // 60) - int(intervalo)
    return total

def generate_period_section(hora_inicio, hora_fim, intervalo, tempo_disponivel):
    """Generate period section of the report, showing date+hour if present."""
    section = "⏰ PERÍODO DE TRABALHO\n"
    section += "─" * 40 + "\n"
    section += f"Início: {hora_inicio}\n"
    section += f"Fim: {hora_fim}\n"
    section += f"Intervalo: {intervalo} min\n"
    section += f"Tempo Disponível: {tempo_disponivel} min ({tempo_disponivel/60:.1f}h)\n\n"
    return section
