# performance_komori.py

def extrair_tempo_setup_komori(processo):
    """Extrai o tempo de setup do texto do processo para Komori."""
    import re
    texto = str(processo).lower()
    horas = 0
    minutos = 0
    match_hora = re.search(r'(\d{1,2})\s*h', texto)
    match_min = re.search(r'(\d{1,3})\s*min', texto)
    if match_hora:
        horas = int(match_hora.group(1))
    if match_min:
        minutos = int(match_min.group(1))
    total_min = horas * 60 + minutos
    if total_min > 0:
        return total_min
    return None

def sincronizar_tempo_setup_komori(df):
    for idx, row in df.iterrows():
        processo = row.get('Processo', '')
        tempo_setup = extrair_tempo_setup_komori(processo)
        if tempo_setup:
            df.at[idx, 'Tempo Setup'] = f"{tempo_setup:02d}:00"
        else:
            df.at[idx, 'Tempo Setup'] = ''
    return df
