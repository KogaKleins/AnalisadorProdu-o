import re
import tkinter as tk

def formatar_data(texto):
    texto = re.sub(r"[^\d]", "", texto)[:8]
    if len(texto) == 8:
        return f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
    return texto

def formatar_hora(texto):
    texto = re.sub(r"[^\d]", "", texto)[:4]
    if len(texto) >= 2:
        if len(texto) == 4:
            return f"{texto[:2]}:{texto[2:]}"
        elif len(texto) == 3:
            return f"0{texto[0]}:{texto[1:]}"
        else:
            return f"{texto}:00"
    return texto

def ao_pressionar_enter(event=None):
    from data.data_handler import carregar_dados
    carregar_dados()

def ao_digitar_data(entrada, event=None):
    texto = entrada.get()
    nova_data = formatar_data(texto)
    entrada.delete(0, tk.END)
    entrada.insert(0, nova_data)

def ao_digitar_hora_inicio(entrada, event=None):
    texto = entrada.get()
    nova_hora = formatar_hora(texto)
    entrada.delete(0, tk.END)
    entrada.insert(0, nova_hora)

def ao_digitar_hora_fim(entrada, event=None):
    texto = entrada.get()
    nova_hora = formatar_hora(texto)
    entrada.delete(0, tk.END)
    entrada.insert(0, nova_hora)