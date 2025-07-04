import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

"""
Ponto de entrada da aplicação Analisador de Produção.
Inicializa a aplicação, configura logging e chama a interface principal.
"""
import logging
from interface.components.main_window import MainWindow

def main():
    logging.basicConfig(level=logging.INFO)
    app = MainWindow()
    app.run()

if __name__ == "__main__":
    main()
