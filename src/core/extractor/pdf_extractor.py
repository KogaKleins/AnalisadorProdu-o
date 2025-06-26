"""
PDF data extraction module.
"""

import os
import pdfplumber
import pandas as pd

COLUNAS = [
    "Início", "Término", "Tempo", "OS", "Cliente", 
    "Processo", "Evento", "Qtd. Recebida", "Qtd. Produzida", 
    "Observações"
]

def extrair_dados_pdf(caminho_pdf):
    """
    Extract data from production PDF report.
    
    Args:
        caminho_pdf (str): Path to PDF file
        
    Returns:
        pd.DataFrame: Extracted data in DataFrame format
        
    Raises:
        FileNotFoundError: If PDF file not found
    """
    dados = []
    if not os.path.exists(caminho_pdf):
        raise FileNotFoundError(f"Arquivo PDF não encontrado: {caminho_pdf}")

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    if linha and any(linha):
                        # Ensure line has correct number of columns
                        linha_corrigida = (linha + [''] * (len(COLUNAS) - len(linha)))[:len(COLUNAS)]
                        dados.append(linha_corrigida)

    if not dados:
        raise ValueError(f"Nenhum dado encontrado no arquivo: {caminho_pdf}")

    return pd.DataFrame(dados, columns=COLUNAS)
