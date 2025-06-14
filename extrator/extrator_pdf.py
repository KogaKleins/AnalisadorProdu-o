
import os
import pdfplumber
import pandas as pd

COLUNAS = ["Início", "Término", "Tempo", "OS", "Cliente", "Processo", "Evento", "Qtd. Recebida", "Qtd. Produzida", "Observações"]

def extrair_dados_pdf(caminho_pdf):
    dados = []
    if not os.path.exists(caminho_pdf):
        return pd.DataFrame()

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                for linha in tabela:
                    if linha and any(linha):
                        linha_corrigida = (linha + [''] * (len(COLUNAS) - len(linha)))[:len(COLUNAS)]
                        dados.append(linha_corrigida)

    return pd.DataFrame(dados, columns=COLUNAS)
