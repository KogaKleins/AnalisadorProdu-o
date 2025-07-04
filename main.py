"""
Main application entry point.
"""

import os
import sys
import platform
import subprocess
import logging
from pathlib import Path

# Configuração do ambiente virtual

def setup_venv():
    venv_dir = Path(__file__).parent / 'venv'
    if not venv_dir.exists():
        print("Criando ambiente virtual...")
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
        print("Ambiente virtual criado com sucesso!")

# Apenas cria o venv se não existir
setup_venv()

# Adiciona o diretório raiz do projeto ao PYTHONPATH
root_dir = Path(__file__).parent.absolute()
src_dir = os.path.join(root_dir, 'src')
sys.path.insert(0, str(root_dir))
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('analisador.log')
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        from src.interface import MainWindow
        logger.info("Iniciando Analisador de Produção...")
        app = MainWindow()
        app.run()
    except Exception as e:
        logger.error(f"Erro ao iniciar aplicação: {str(e)}", exc_info=True)
        sys.exit(1)

# Redireciona para o ponto de entrada principal
if __name__ == "__main__":
    script_path = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
    result = subprocess.run([sys.executable, script_path])
    sys.exit(result.returncode)