import os
import difflib
import platform

def construir_caminho_pdf(data, maquina):
    try:
        # OPÇÃO 1: Detecta automaticamente o sistema operacional
        sistema = platform.system()
        # Caminho base adaptável para Linux e Windows
        if sistema == "Linux":
            # Caminho correto para seu novo local
            base_dir = "/home/koga/wilmar/AnalisadorProducao/RELATORIOS PRODUTIVIDADE/pdf"
        elif sistema == "Windows":
            base_dir = r"C:\\Users\\Usuario\\Desktop\\WILMAR\\AnalisadorProducao\\RELATORIOS PRODUTIVIDADE\\pdf"
        else:
            # Fallback para outros sistemas
            base_dir = os.path.join(os.path.expanduser("~"), "RELATORIOS PRODUTIVIDADE", "pdf")
        
        # OPÇÃO 2: Usando variável de ambiente (descomente para usar)
        # base_dir = os.getenv('RELATORIOS_PATH', base_dir)
        
        # Verifica se o diretório existe
        if not os.path.exists(base_dir):
            raise FileNotFoundError(f"Diretório base não encontrado: {base_dir}")
            
        meses = os.listdir(base_dir)
        meses = [m for m in meses if os.path.isdir(os.path.join(base_dir, m))]

        # Tenta identificar o mês da data
        dia, mes, _ = data.split("/")
        mes = mes.zfill(2)

        # Converter número do mês para nome textual correspondente
        nomes_meses = {
            "01": "janeiro", "02": "fevereiro", "03": "marco", "04": "abril",
            "05": "maio", "06": "junho", "07": "julho", "08": "agosto",
            "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"
        }

        nome_mes = nomes_meses.get(mes, "").lower()

        # Encontrar mês mais próximo com nome semelhante
        mes_correspondente = difflib.get_close_matches(nome_mes, meses, n=1, cutoff=0.6)
        if not mes_correspondente:
            raise FileNotFoundError(f"Mês '{nome_mes}' não encontrado em {base_dir}")
        mes_folder = mes_correspondente[0]

        # Acessa pasta do dia
        pasta_dia = os.path.join(base_dir, mes_folder, dia)
        if not os.path.isdir(pasta_dia):
            raise FileNotFoundError(f"Dia '{dia}' não encontrado em {mes_folder}")

        # Buscar PDF com nome semelhante à máquina informada
        arquivos_pdf = [arq for arq in os.listdir(pasta_dia) if arq.endswith(".pdf")]
        maquina_arquivo = difflib.get_close_matches(maquina.lower() + ".pdf", [a.lower() for a in arquivos_pdf], n=1, cutoff=0.6)

        if not maquina_arquivo:
            raise FileNotFoundError(f"Arquivo correspondente à máquina '{maquina}' não encontrado em {pasta_dia}")

        # Encontra o arquivo original com a capitalização correta
        arquivo_original = None
        for arq in arquivos_pdf:
            if arq.lower() == maquina_arquivo[0]:
                arquivo_original = arq
                break

        return os.path.join(pasta_dia, arquivo_original)

    except Exception as e:
        raise e