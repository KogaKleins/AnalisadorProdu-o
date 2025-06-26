"""
Group data handling module.
Contains functions for grouping and managing data groups.
"""

import tkinter as tk
from tkinter import messagebox

class GroupManager:
    def __init__(self):
        self.grupos = {}
        self.linhas_selecionadas = []
    
    def agrupar_selecionadas(self):
        """Group selected lines"""
        if not self.linhas_selecionadas:
            messagebox.showwarning("Atenção", "Nenhuma linha selecionada para agrupar.")
            return False
        
        novo_grupo = f"Grupo_{len(self.grupos) + 1}"
        self.grupos[novo_grupo] = self.linhas_selecionadas.copy()
        self.linhas_selecionadas.clear()
        
        messagebox.showinfo("Sucesso", f"Linhas agrupadas em {novo_grupo}.")
        return True
    
    def desagrupar_selecionadas(self):
        """Ungroup selected lines"""
        if not self.linhas_selecionadas:
            messagebox.showwarning("Atenção", "Nenhuma linha selecionada para desagrupar.")
            return False
        
        grupos_a_remover = []
        for grupo, linhas in self.grupos.items():
            if any(linha in linhas for linha in self.linhas_selecionadas):
                grupos_a_remover.append(grupo)
        
        for grupo in grupos_a_remover:
            del self.grupos[grupo]
        
        self.linhas_selecionadas.clear()
        messagebox.showinfo("Sucesso", "Grupos desagrupados com sucesso.")
        return True
    
    def atualizar_selecao(self, novas_linhas):
        """Update selected lines"""
        self.linhas_selecionadas = novas_linhas.copy()
    
    def obter_grupos(self):
        """Get current groups"""
        return self.grupos.copy()
    
    def limpar_grupos(self):
        """Clear all groups"""
        self.grupos.clear()
        self.linhas_selecionadas.clear()
    
    def adicionar_grupo(self, nome_grupo, linhas):
        """Add new group"""
        if nome_grupo not in self.grupos:
            self.grupos[nome_grupo] = linhas.copy()
            return True
        return False
    
    def remover_grupo(self, nome_grupo):
        """Remove group by name"""
        if nome_grupo in self.grupos:
            del self.grupos[nome_grupo]
            return True
        return False
    
    def obter_linhas_grupo(self, nome_grupo):
        """Get lines from specific group"""
        return self.grupos.get(nome_grupo, []).copy()
    
    def linha_esta_agrupada(self, linha):
        """Check if line is in any group"""
        return any(linha in linhas for linhas in self.grupos.values())
