"""
Data formatting utilities for handlers.
"""

from datetime import datetime

def format_date(date_str):
    """Format date to display format"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    except:
        return date_str

def format_time(minutes):
    """Format minutes to hours:minutes"""
    try:
        hours = minutes // 60
        mins = minutes % 60
        return f"{int(hours):02d}:{int(mins):02d}"
    except:
        return str(minutes)

def format_quantity(value):
    """Format quantity with thousand separator"""
    try:
        return f"{int(value):,}"
    except:
        return str(value)

def format_efficiency(value):
    """Format efficiency percentage"""
    try:
        return f"{float(value):.1f}%"
    except:
        return str(value)

def ao_digitar_data(widget, event=None):
    """
    Validação para entrada de data no formato DD/MM/YYYY.
    Atualiza o valor do widget Entry conforme o usuário digita.
    """
    valor = widget.get()
    # Remove caracteres não numéricos exceto '/'
    texto = ''.join(c for c in valor if c.isdigit() or c == '/')
    if len(texto) > 10:
        texto = texto[:10]
    # Insere barras automaticamente
    if len(texto) > 2 and texto[2] != '/':
        texto = texto[:2] + '/' + texto[2:]
    if len(texto) > 5 and texto[5] != '/':
        texto = texto[:5] + '/' + texto[5:]
    # Atualiza o valor do widget
    widget.delete(0, 'end')
    widget.insert(0, texto)

def ao_digitar_hora_inicio(widget, event=None):
    valor = widget.get()
    # Remove tudo que não for número
    numeros = ''.join(c for c in valor if c.isdigit())
    novo = ''
    # Formatação para dd/mm/yyyy HH:MM
    if len(numeros) >= 2:
        novo += numeros[:2]
    if len(numeros) >= 4:
        novo += '/' + numeros[2:4]
    if len(numeros) >= 8:
        novo += '/' + numeros[4:8]
    if len(numeros) > 8:
        novo += ' '
        if len(numeros) >= 10:
            novo += numeros[8:10]
        if len(numeros) >= 12:
            novo += ':' + numeros[10:12]
    widget.delete(0, 'end')
    widget.insert(0, novo)

def ao_digitar_hora_fim(widget, event=None):
    ao_digitar_hora_inicio(widget, event)

def ao_sair_hora(widget, event=None):
    valor = widget.get().strip()
    # Tenta formatar se for só números
    numeros = ''.join(c for c in valor if c.isdigit())
    if len(numeros) == 12:  # ddmmYYYYhhmm
        novo = f"{numeros[:2]}/{numeros[2:4]}/{numeros[4:8]} {numeros[8:10]}:{numeros[10:12]}"
        widget.delete(0, 'end')
        widget.insert(0, novo)
    elif len(numeros) == 4:  # hhmm
        novo = f"{numeros[:2]}:{numeros[2:4]}"
        widget.delete(0, 'end')
        widget.insert(0, novo)
    # Se não for válido, não faz nada (ou pode colorir de vermelho)
