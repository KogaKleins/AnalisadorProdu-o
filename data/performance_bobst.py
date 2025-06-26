# performance_bobst.py

def extrair_tempo_setup_bobst(processo):
    """Extrai o tempo de setup do texto do processo para Bobst, ou aplica default 03:00 se não houver."""
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
    return 180  # Default 03:00

def sincronizar_tempo_setup_bobst(df):
    for idx, row in df.iterrows():
        processo = row.get('Processo', '')
        tempo_setup = extrair_tempo_setup_bobst(processo)
        df.at[idx, 'Tempo Setup'] = f"{tempo_setup:02d}:00"
    return df
