"""
Main application entry point - Otimizado para Executável PyInstaller
"""

import os
import sys
import platform
import subprocess
import logging
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def get_base_path():
    """Determina o caminho base da aplicação (executável ou script)"""
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller
        return Path(sys._MEIPASS)
    else:
        # Script Python
        return Path(__file__).parent.absolute()

def setup_logging():
    """Configura logging com tratamento para executável"""
    try:
        # Cria pasta de logs se não existir
        log_dir = get_base_path() / 'logs'
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / 'analisador.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file, encoding='utf-8')
            ]
        )
    except Exception as e:
        # Fallback para logging básico
        logging.basicConfig(level=logging.INFO)
        logging.error(f"Erro ao configurar logging: {e}")

def setup_environment():
    """Configura o ambiente da aplicação"""
    try:
        base_path = get_base_path()
        src_dir = base_path / 'src'
        
        # Adiciona diretórios ao PYTHONPATH
        if str(base_path) not in sys.path:
            sys.path.insert(0, str(base_path))
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
            
        # Configura variáveis de ambiente
        os.environ['ANALISADOR_BASE_PATH'] = str(base_path)
        
        return True
    except Exception as e:
        logging.error(f"Erro ao configurar ambiente: {e}")
        return False

def show_error_dialog(error_msg, details=None):
    """Mostra diálogo de erro amigável"""
    try:
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal
        
        title = "Erro Fatal - Analisador de Produção"
        message = f"{error_msg}\n\n"
        
        if details:
            message += f"Detalhes técnicos:\n{details}"
        
        messagebox.showerror(title, message)
        root.destroy()
    except:
        # Fallback para console
        print(f"ERRO FATAL: {error_msg}")
        if details:
            print(f"Detalhes: {details}")

def main():
    """Ponto de entrada principal com tratamento robusto de erros"""
    try:
        # Configura logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Iniciando Analisador de Produção...")
        
        # Configura ambiente
        if not setup_environment():
            raise Exception("Falha ao configurar ambiente da aplicação")
        
        # Verifica se estamos em modo executável
        if getattr(sys, 'frozen', False):
            logger.info("Executando em modo executável")
        else:
            logger.info("Executando em modo desenvolvimento")
        
        # Importa e inicia a aplicação
        from src.interface.components.main_window import MainWindow
        
        logger.info("Criando janela principal...")
        app = MainWindow()
        
        logger.info("Iniciando loop principal...")
        app.run()
        
    except ImportError as e:
        error_msg = "Erro ao importar módulos necessários"
        details = f"ImportError: {str(e)}\n\nVerifique se todos os arquivos estão presentes."
        show_error_dialog(error_msg, details)
        sys.exit(1)
        
    except Exception as e:
        error_msg = "Erro inesperado ao iniciar a aplicação"
        details = f"Tipo: {type(e).__name__}\nErro: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        show_error_dialog(error_msg, details)
        sys.exit(1)

if __name__ == "__main__":
    main()