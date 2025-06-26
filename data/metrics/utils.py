# Arquivo: data/metrics/utils.py

import re

def converter_tempo_para_minutos(tempo_str):
    """Converte tempo em formato HH:MM para minutos"""
    if not tempo_str or tempo_str == "00:00" or tempo_str == "nan" or str(tempo_str).lower() == 'nan':
        return 0
    try:
        tempo_str = str(tempo_str).strip()
        if ':' in tempo_str:
            partes = tempo_str.split(':')
            if len(partes) == 2:
                h, m = map(int, partes)
                return h * 60 + m
        else:
            # Se não tem ':', assume que já está em minutos
            return int(float(tempo_str))
    except (ValueError, TypeError):
        return 0

def extrair_velocidade_nominal(processo):
    """Extrai velocidade nominal do processo (formato: X.XXX p/h)"""
    if not processo:
        return 0
    
    # Busca padrões como "4.000 p/h", "3000 p/h", etc.
    matches = re.findall(r'(\d{1,2}\.?\d{3})\s*p/h', str(processo), re.IGNORECASE)
    if matches:
        try:
            # Pega o primeiro match e remove pontos de milhar
            numero_str = matches[0].replace('.', '')
            return float(numero_str)
        except (ValueError, TypeError):
            return 0
    return 0

def eh_acerto(evento):
    """Verifica se o evento é de acerto/setup"""
    if not evento:
        return False
    evento_str = str(evento).lower().strip()
    palavras_acerto = ['acerto', '01 acerto', 'setup', 'ajuste']
    return any(palavra in evento_str for palavra in palavras_acerto)

def eh_producao(evento):
    """Verifica se o evento é de produção"""
    if not evento:
        return False
    evento_str = str(evento).lower().strip()
    palavras_producao = ['produção', 'producao', '02 produção', '02 producao', 'produz']
    return any(palavra in evento_str for palavra in palavras_producao)

def extrair_op_numero(os_value):
    """Extrai número da OP/OS de forma mais robusta (versão limpa)"""
    if not os_value or str(os_value) == '0' or str(os_value).lower() == 'nan':
        return None
    
    os_str = str(os_value).strip()
    
    # Se já é só número, retorna
    if os_str.isdigit():
        return os_str
    
    # Remove pontos e busca apenas números
    os_limpo = re.sub(r'[^\d]', '', os_str)
    if os_limpo:
        return os_limpo
    
    return os_str

def extrair_op_numero_original(os_value):
    """Mantém o formato original da OP (118.951, 119.000, etc.)"""
    if not os_value or str(os_value) == '0' or str(os_value).lower() == 'nan':
        return None
    
    return str(os_value).strip()

def extrair_quantidades_melhorada(row, df):
    """Extrai quantidades de forma mais precisa, separando produzida de recebida"""
    qtd_produzida = 0
    qtd_recebida = 0
    
    # Mapeia as colunas para identificar qual é qual
    colunas_qtd = [col for col in df.columns if "qtd" in str(col).lower()]
    
    for col in colunas_qtd:
        try:
            valor_str = str(row.get(col, 0)).replace('.', '').replace(',', '.')
            if valor_str and valor_str.lower() != 'nan':
                valor = float(valor_str)
                col_lower = str(col).lower()
                
                # Identifica se é produzida ou recebida
                if "produz" in col_lower or "produzida" in col_lower:
                    qtd_produzida = valor
                elif "receb" in col_lower or "recebida" in col_lower:
                    qtd_recebida = valor
                else:
                    # Se não conseguir identificar, assume como produzida
                    qtd_produzida = valor
        except (ValueError, TypeError):
            continue
    
    return qtd_produzida, qtd_recebida

def validar_dados_linha(row, df):
    """Valida se os dados da linha fazem sentido"""
    evento = str(row.get('Evento', ''))
    
    # Verifica se tem evento válido
    if not (eh_acerto(evento) or eh_producao(evento)):
        return False
    
    # Verifica se tem tempo válido
    tempo_valido = False
    for col in df.columns:
        if "tempo" in str(col).lower():
            tempo = str(row.get(col, '00:00'))
            if converter_tempo_para_minutos(tempo) > 0:
                tempo_valido = True
                break
    
    return tempo_valido

def calcular_eficiencia_tempo_geral(tempo_utilizado_total, tempo_disponivel):
    """
    Calcula a eficiência de tempo geral conforme solicitado:
    Fórmula: tempo_utilizado / tempo_disponivel * 100
    """
    if tempo_disponivel <= 0:
        return 0
    
    return (tempo_utilizado_total / tempo_disponivel) * 100

def formatar_tempo_minutos(minutos):
    """Formata minutos para formato HH:MM"""
    if minutos <= 0:
        return "00:00"
    
    horas = int(minutos // 60)
    mins = int(minutos % 60)
    return f"{horas:02d}:{mins:02d}"

def calcular_diferenca_setup(tempo_programado, tempo_utilizado):
    """Calcula diferença entre tempo programado e utilizado"""
    return tempo_programado - tempo_utilizado