import tkinter as tk
from tkinter import messagebox

def agrupar_selecionadas():
    # Importação dinâmica das variáveis globais
    from interface.ui_setup import df_global, linhas_agrupadas, linhas_selecionadas
    
    if not linhas_selecionadas:
        messagebox.showwarning("Atenção", "Nenhuma linha selecionada para agrupar.")
        return
    
    novo_grupo = f"Grupo_{len(linhas_agrupadas) + 1}"
    linhas_agrupadas[novo_grupo] = linhas_selecionadas.copy()
    linhas_selecionadas.clear()
    
    messagebox.showinfo("Sucesso", f"Linhas agrupadas em {novo_grupo}.")

def desagrupar_selecionadas():
    # Importação dinâmica das variáveis globais
    from interface.ui_setup import linhas_agrupadas, linhas_selecionadas
    
    if not linhas_selecionadas:
        messagebox.showwarning("Atenção", "Nenhuma linha selecionada para desagrupar.")
        return
    
    grupos_a_remover = []
    for grupo, linhas in linhas_agrupadas.items():
        if any(linha in linhas for linha in linhas_selecionadas):
            grupos_a_remover.append(grupo)
    
    for grupo in grupos_a_remover:
        del linhas_agrupadas[grupo]
    
    linhas_selecionadas.clear()
    messagebox.showinfo("Sucesso", "Grupos desagrupados com sucesso.")