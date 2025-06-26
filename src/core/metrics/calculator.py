"""
Performance analysis and calculation module.
"""

import tkinter as tk
from ..config.setup_config import TEMPOS_SETUP
import importlib

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
    if df_global is None or df_global.empty:
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, "❌ ERRO: Nenhum dado carregado para calcular o desempenho.")
        return

    try:
        maquina = config.get('maquina', '').strip().lower()
        modulo = None
        for key, modname in MACHINES_MAP.items():
            if key in maquina:
                modulo = modname
                break
        if modulo:
            mod = importlib.import_module(f"src.core.metrics.maquinas.{modulo}")
            resultado = mod.calcular_desempenho(df_global, config)
        else:
            # Lógica padrão
            hora_inicio = config.get('hora_inicio')
            hora_fim = config.get('hora_fim')
            intervalo_str = config.get('intervalo', '60')

            if not hora_inicio or not hora_fim:
                text_resultado.delete("1.0", tk.END)
                text_resultado.insert(tk.END, "❌ ERRO: Preencha os horários de início e fim.")
                return

            intervalo = int(intervalo_str) if intervalo_str else 60

            # Calculate metrics
            from data.metrics.agrupamento import agrupar_dados
            from data.metrics.relatorio import gerar_relatorio

            df = df_global.copy()
            grupos_para_analise, ops_analise = agrupar_dados(df, config.get('linhas_agrupadas', {}))
            resultado = gerar_relatorio(grupos_para_analise, ops_analise, hora_inicio, hora_fim, intervalo)

        # Exibe resultado
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, resultado)

    except Exception as e:
        text_resultado.delete("1.0", tk.END)
        text_resultado.insert(tk.END, f"❌ ERRO ao calcular desempenho: {str(e)}")
        import traceback
        traceback.print_exc()
