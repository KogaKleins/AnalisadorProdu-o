# data/performance_calculator.py

import tkinter as tk
from interface import globals
from data.metrics.agrupamento import agrupar_dados
from data.metrics.relatorio import gerar_relatorio

def calcular_desempenho():
    if globals.df_global is None or globals.df_global.empty:
        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, "❌ ERRO: Nenhum dado carregado para calcular o desempenho.")
        return

    try:
        hora_inicio = globals.entrada_hora_inicio.get()
        hora_fim = globals.entrada_hora_fim.get()
        intervalo_str = globals.entrada_intervalo.get()

        if not hora_inicio or not hora_fim:
            globals.text_resultado.delete("1.0", tk.END)
            globals.text_resultado.insert(tk.END, "❌ ERRO: Preencha os horários de início e fim.")
            return

        intervalo = int(intervalo_str) if intervalo_str else 60

        df = globals.df_global.copy()
        grupos_para_analise, ops_analise = agrupar_dados(df, globals.linhas_agrupadas)
        relatorio = gerar_relatorio(grupos_para_analise, ops_analise, hora_inicio, hora_fim, intervalo)

        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, relatorio)

    except Exception as e:
        globals.text_resultado.delete("1.0", tk.END)
        globals.text_resultado.insert(tk.END, f"❌ ERRO ao calcular desempenho: {str(e)}")
        import traceback
        traceback.print_exc()

