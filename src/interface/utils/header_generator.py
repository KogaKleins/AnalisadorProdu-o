"""
Header generation module.
Contains functions for generating table headers and column configurations.
"""

def gerar_headers_colunas():
    """
    Gera a lista de colunas padrão para a tabela de dados.
    
    Returns:
        list: Lista com os nomes das colunas da tabela
    """
    return [
        'Data',
        'Hora',
        'Máquina',
        'Evento',
        'Quantidade',
        'Status',
        'Grupo',
        'Observações'
    ]

def criar_headers_alfabeticos(num_colunas=26):
    """
    Cria headers alfabéticos (A, B, C, ..., Z, AA, AB, etc).
    Útil para tabelas temporárias ou de dados brutos.
    
    Args:
        num_colunas (int): Número de colunas para gerar headers
        
    Returns:
        list: Lista com headers alfabéticos
    """
    headers = []
    for i in range(num_colunas):
        if i < 26:
            headers.append(chr(65 + i))  # A-Z
        else:
            # Para colunas após Z (AA, AB, etc)
            primeira_letra = chr(65 + ((i - 26) // 26))
            segunda_letra = chr(65 + ((i - 26) % 26))
            headers.append(primeira_letra + segunda_letra)
    return headers

def generate_table_headers():
    """Generate standard table headers"""
    return [
        'Data',
        'Hora',
        'Evento',
        'OS',
        'Cliente',
        'Processo',
        'Velocidade',
        'Qtd_Produzida',
        'Qtd_Recebida',
        'Tempo'
    ]

def get_column_alignments():
    """
    Retorna o alinhamento padrão para cada tipo de coluna.
    
    Returns:
        dict: Dicionário com os alinhamentos por tipo de coluna
    """
    return {
        'Data': 'center',
        'Hora': 'center',
        'Máquina': 'center',
        'Evento': 'left',
        'Quantidade': 'right',
        'Status': 'center',
        'Grupo': 'center',
        'Observações': 'left',
        'OS': 'center',
        'Cliente': 'left',
        'Processo': 'left',
        'Velocidade': 'right',
        'Qtd_Produzida': 'right',
        'Qtd_Recebida': 'right',
        'Tempo': 'center'
    }

def get_column_widths():
    """Get standard column widths"""
    return {
        'Data': 100,
        'Hora': 80,
        'Evento': 150,
        'OS': 100,
        'Cliente': 200,
        'Processo': 150,
        'Velocidade': 100,
        'Qtd_Produzida': 120,
        'Qtd_Recebida': 120,
        'Tempo': 80
    }
