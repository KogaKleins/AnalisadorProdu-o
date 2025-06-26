"""
Group handler module.
Contains functions for managing data groups.
"""

from tkinter import messagebox
from src.interface import globals

def agrupar_selecionadas_melhorado():
    """Group selected rows with improved functionality"""
    
    if not globals.linhas_selecionadas:
        messagebox.showwarning("Atenção", "Nenhuma linha selecionada para agrupar.")
        return
    
    novo_grupo = f"Grupo_{len(globals.linhas_agrupadas) + 1}"
    globals.linhas_agrupadas[novo_grupo] = globals.linhas_selecionadas.copy()
    globals.linhas_selecionadas.clear()
    
    # Update table colors
    from .table_handler import aplicar_cores_grupos
    aplicar_cores_grupos(globals.tabela, globals.linhas_agrupadas)
    
    messagebox.showinfo("Sucesso", f"Linhas agrupadas em {novo_grupo}.")

def desagrupar_selecionadas_melhorado():
    """Ungroup selected rows with improved functionality"""
    
    if not globals.linhas_selecionadas:
        messagebox.showwarning("Atenção", "Nenhuma linha selecionada para desagrupar.")
        return
    
    grupos_a_remover = []
    for grupo, linhas in globals.linhas_agrupadas.items():
        if any(linha in linhas for linha in globals.linhas_selecionadas):
            grupos_a_remover.append(grupo)
    
    for grupo in grupos_a_remover:
        del globals.linhas_agrupadas[grupo]
    
    globals.linhas_selecionadas.clear()
    
    # Clear table colors
    if globals.tabela:
        for item in globals.tabela.get_children():
            globals.tabela.item(item, tags=())
    
    # Update remaining groups
    from .table_handler import aplicar_cores_grupos
    aplicar_cores_grupos(globals.tabela, globals.linhas_agrupadas)
    
    messagebox.showinfo("Sucesso", "Grupos desagrupados com sucesso.")

def handle_group_action(action, **kwargs):
    """
    Handle group-related actions.
    
    Args:
        action (str): The action to perform ('agrupar' or 'desagrupar')
        **kwargs: Additional arguments for the specific action
    """
    if action == 'agrupar':
        return agrupar_selecionadas_melhorado()
    elif action == 'desagrupar':
        return desagrupar_selecionadas_melhorado()
    else:
        raise ValueError(f"Ação de grupo inválida: {action}")
