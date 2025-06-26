"""
PDF file finder module.
Responsável por localizar o caminho do PDF com base na data e na máquina.
"""

import os
import difflib
import platform

def construir_caminho_pdf(data, maquina):
    """
    Build path to PDF file based on date and machine.
    
    Args:
        data (str): Date in format DD/MM/YYYY
        maquina (str): Machine name
        
    Returns:
        str: Absolute path to PDF file
        
    Raises:
        FileNotFoundError: If directory or file not found
    """
    try:
        # Auto-detect operating system
        sistema = platform.system()
        
        if sistema == "Linux":
            base_dir = "/home/koga/wilmar/AnalisadorProducao/RELATORIOS PRODUTIVIDADE/pdf"
        elif sistema == "Windows":
            base_dir = r"C:\\Users\\Usuario\\Desktop\\WILMAR\\AnalisadorProducao\\RELATORIOS PRODUTIVIDADE\\pdf"
        else:
            # Fallback for other systems
            base_dir = os.path.join(os.path.expanduser("~"), "RELATORIOS PRODUTIVIDADE", "pdf")
        
        # Verify directory exists
        if not os.path.exists(base_dir):
            raise FileNotFoundError(f"Diretório base não encontrado: {base_dir}")
            
        meses = os.listdir(base_dir)
        meses = [m for m in meses if os.path.isdir(os.path.join(base_dir, m))]

        # Try to identify month from date
        dia, mes, _ = data.split("/")
        mes = mes.zfill(2)

        # Convert month number to text name
        nomes_meses = {
            "01": "janeiro", "02": "fevereiro", "03": "marco", "04": "abril",
            "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
            "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"
        }

        nome_mes = nomes_meses.get(mes, "").lower()

        # Find closest matching month
        mes_correspondente = difflib.get_close_matches(nome_mes, meses, n=1, cutoff=0.6)
        if not mes_correspondente:
            raise FileNotFoundError(f"Mês '{nome_mes}' não encontrado em {base_dir}")
        mes_folder = mes_correspondente[0]

        # Access day folder
        pasta_dia = os.path.join(base_dir, mes_folder, dia)
        if not os.path.isdir(pasta_dia):
            raise FileNotFoundError(f"Dia '{dia}' não encontrado em {mes_folder}")

        # Search PDF with similar name to machine
        arquivos_pdf = [arq for arq in os.listdir(pasta_dia) if arq.endswith(".pdf")]
        maquina_arquivo = difflib.get_close_matches(maquina.lower() + ".pdf", [a.lower() for a in arquivos_pdf], n=1, cutoff=0.6)

        if not maquina_arquivo:
            raise FileNotFoundError(f"Arquivo correspondente à máquina '{maquina}' não encontrado em {pasta_dia}")

        # Find original file with correct capitalization
        arquivo_original = None
        for arq in arquivos_pdf:
            if arq.lower() == maquina_arquivo[0]:
                arquivo_original = arq
                break

        return os.path.join(pasta_dia, arquivo_original)

    except Exception as e:
        raise FileNotFoundError(f"Erro ao localizar arquivo: {str(e)}")
