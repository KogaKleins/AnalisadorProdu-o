"""
Performance analysis and calculation module.
"""

import tkinter as tk
from ..config.setup_config import TEMPOS_SETUP
import importlib
from src.interface.handlers.data_handler import MACHINE_ALIASES

MACHINES_MAP = {
    'komori': 'komori',
    'hcd': 'hcd',
    'sbl': 'sbl',
    'furnax': 'furnax',
    'c/v manual': 'cv_manual',
    'cv manual': 'cv_manual',
    'samkoon': 'samkoon',
    'laminadora': 'laminadora',
    'verniz.uv sakurai': 'verniz_uv_sakurai',
    'bobst': 'bobst',
}

def calcular_desempenho(df_global, text_resultado, config):
    """
    Calculate performance metrics from production data.
    
    Args:
        df_global (pd.DataFrame): Production data
        text_resultado (tk.Text): Result display widget
        config (dict): Analysis configuration
        
    Returns:
        None: Results are displayed in text_resultado widget
    """
    import importlib
    import sys
    if df_global is None or df_global.empty:
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, "❌ ERRO: Nenhum dado carregado para calcular o desempenho.")
        return

    try:
        maquina = config.get('maquina', '').strip().lower()
        maquina_padrao = MACHINE_ALIASES.get(maquina, maquina)
        modulo = None
        for key, modname in MACHINES_MAP.items():
            if key == maquina_padrao:
                modulo = modname
                break
        if modulo:
            try:
                mod = importlib.import_module(f"src.core.metrics.maquinas.{modulo}")
            except ModuleNotFoundError:
                maquinas_disp = ', '.join(sorted(set(MACHINES_MAP.keys())))
                text_resultado.delete("1.0", tk.END)
                text_resultado.insert(tk.END, f"❌ ERRO: Máquina '{maquina}' não encontrada ou não implementada.\nMáquinas disponíveis: {maquinas_disp}")
                return
            resultado = mod.calcular_desempenho(df_global, config)
        else:
            maquinas_disp = ', '.join(sorted(set(MACHINES_MAP.keys())))
            text_resultado.delete("1.0", tk.END)
            text_resultado.insert(tk.END, f"❌ ERRO: Máquina '{maquina}' não encontrada ou não implementada.\nMáquinas disponíveis: {maquinas_disp}")
            return
        # Exibe resultado
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)

    except Exception as e:
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, f"❌ ERRO ao calcular desempenho: {str(e)}")
        import traceback
        traceback.print_exc()
