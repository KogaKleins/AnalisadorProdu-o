import pandas as pd
import re

def limpar_setup_op_sem_acerto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove o tempo de setup de todas as linhas de uma OP se não houver nenhum evento de acerto para aquela OP.
    Funciona para qualquer máquina.
    """
    if 'Tempo Setup' not in df.columns or ('OS' not in df.columns and 'OP' not in df.columns) or 'Evento' not in df.columns:
        return df
    op_col = 'OS' if 'OS' in df.columns else 'OP'
    ops = df[op_col].unique()
    for op in ops:
        mask_op = df[op_col] == op
        eventos = df.loc[mask_op, 'Evento'].astype(str).str.lower()
        tem_acerto = eventos.str.contains('acerto').any()
        if not tem_acerto:
            df.loc[mask_op, 'Tempo Setup'] = ''
    return df

def preencher_campos_generico(df, regras_setup, regras_media):
    """
    Preenche Tempo Setup e Média Produção conforme regras passadas, mas só se o campo estiver vazio.
    regras_setup: lista de tuplas (condição, valor), prioridade da primeira para a última. Ex: [(lambda proc, evt: 'destaque' in proc, '03:00'), ...]
    regras_media: lista de tuplas (condição, valor), prioridade da primeira para a última. Ex: [(lambda proc, evt: 'micro ondulado' in proc, '2000 p/h'), ...]
    """
    for idx, row in df.iterrows():
        processo = str(row.get('Processo', '')).lower()
        evento = str(row.get('Evento', '')).lower()
        # Tempo Setup
        setup_atual = str(row.get('Tempo Setup', '')).strip()
        if 'acerto' in evento and not setup_atual:
            for cond, valor in regras_setup:
                if cond(processo, evento):
                    df.at[idx, 'Tempo Setup'] = valor
                    break
        # Média Produção: só para linhas de produção
        media_atual = str(row.get('Média Produção', '')).strip()
        if 'produção' in evento:
            if not media_atual:
                for cond, valor in regras_media:
                    if cond(processo, evento):
                        df.at[idx, 'Média Produção'] = valor(processo, evento) if callable(valor) else valor
                        break
        else:
            df.at[idx, 'Média Produção'] = ''
    return df 

# --- FUNÇÕES GLOBAIS UNIVERSAIS ---
def formatar_quantidade(valor):
    """Formata número para string com separador de milhar (ex: 10000 -> '10.000', 1234.56 -> '1.234,56')"""
    try:
        if isinstance(valor, str):
            valor = float(valor.replace('.', '').replace(',', '.'))
        if isinstance(valor, float) and not valor.is_integer():
            inteiro = int(valor)
            decimal = abs(valor - inteiro)
            return f"{inteiro:,}".replace(",", ".") + f",{str(round(decimal*100)).zfill(2)}"
        else:
            return f"{int(valor):,}".replace(",", ".")
    except Exception:
        return str(valor)

def parse_quantidade(valor):
    """Converte string formatada (milhar) ou número para float (ex: '10.000' -> 10000.0)"""
    if valor is None or valor == '':
        return 0.0
    if isinstance(valor, (int, float)):
        return float(valor)
    try:
        return float(str(valor).replace('.', '').replace(',', '.'))
    except Exception:
        return 0.0

def formatar_tempo(valor):
    """Formata minutos para HH:MM (ex: 90 -> '01:30', '01:30' -> '01:30')"""
    if valor is None or valor == '':
        return '00:00'
    if isinstance(valor, str) and ':' in valor:
        partes = valor.split(':')
        if len(partes) == 2:
            h, m = partes
            try:
                h = int(h)
                m = int(m)
                if m > 59:
                    h += m // 60
                    m = m % 60
                return f'{h:02d}:{m:02d}'
            except Exception:
                return valor.zfill(5) if len(valor) < 5 else valor
        return valor.zfill(5) if len(valor) < 5 else valor
    try:
        minutos = int(round(float(valor)))
        h = minutos // 60
        m = minutos % 60
        return f'{h:02d}:{m:02d}'
    except Exception:
        return str(valor)

def parse_tempo(valor):
    """Converte HH:MM ou string/float para minutos inteiros (ex: '01:30' -> 90, 90 -> 90)"""
    if valor is None or valor == '':
        return 0
    if isinstance(valor, (int, float)):
        return int(round(float(valor)))
    if isinstance(valor, str):
        v = valor.strip()
        # Caso HH:MM
        if ':' in v:
            partes = v.split(':')
            if len(partes) == 2:
                try:
                    h, m = map(int, partes)
                    if m > 59:
                        h += m // 60
                        m = m % 60
                    return h * 60 + m
                except Exception:
                    return 0
        # Caso número puro: 900 -> 09:00, 130 -> 01:30, 75 -> 01:15
        if v.isdigit():
            n = int(v)
            if n < 60:
                return n
            elif n < 100:
                # 2 dígitos, trata como minutos
                return n
            elif n < 1000:
                # 3 dígitos, ex: 130 -> 1h30
                h = n // 100
                m = n % 100
                if m > 59:
                    h += m // 60
                    m = m % 60
                return h * 60 + m
            elif n < 10000:
                # 4 dígitos, ex: 1230 -> 12h30
                h = n // 100
                m = n % 100
                if m > 59:
                    h += m // 60
                    m = m % 60
                return h * 60 + m
            else:
                # Números muito grandes, trata como minutos
                return n
        # Caso string com ponto ou vírgula
        try:
            return int(round(float(v.replace('.', '').replace(',', '.'))))
        except Exception:
            return 0
    return 0

# --- FIM FUNÇÕES GLOBAIS UNIVERSAIS --- 