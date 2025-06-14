# interface/visual_layout.py

import tkinter as tk
from tkinter import ttk

def gerar_headers_colunas(num_colunas):
    headers = []
    for i in range(num_colunas):
        if i < 26:
            headers.append(chr(65 + i))  # A-Z
        else:
            first = chr(65 + (i // 26) - 1)
            second = chr(65 + (i % 26))
            headers.append(first + second)  # AA, AB...
    return headers

def criar_headers_alfabeticos(parent_frame, headers_alfabeticos, colunas_reais):
    """
    Cria uma linha de headers alfabéticos acima da tabela
    """
    frame_headers = tk.Frame(parent_frame, bg='#e8e8e8', height=25)
    frame_headers.pack(fill="x", padx=0, pady=0)
    frame_headers.pack_propagate(False)
    
    # Header para coluna de numeração
    label_num = tk.Label(frame_headers, text="#", bg='#d0d0d0', fg='#333', 
                        font=('Arial', 8, 'bold'), relief='raised', bd=1)
    label_num.pack(side="left", fill="y")
    label_num.config(width=4)
    
    # Headers alfabéticos
    for header in headers_alfabeticos:
        label_header = tk.Label(frame_headers, text=header, bg='#e8e8e8', fg='#333', 
                               font=('Arial', 8, 'bold'), relief='raised', bd=1)
        label_header.pack(side="left", fill="both", expand=True)
    
    return frame_headers

def configurar_colunas_da_tabela(tabela, headers_alfabeticos, colunas_reais):
    """
    Configura apenas os nomes reais das colunas na tabela (sem headers alfabéticos)
    """
    tabela["columns"] = ["#"] + headers_alfabeticos
    tabela.column("#0", width=0, stretch=False)

    # Coluna de numeração
    tabela.heading("#", text="#")
    tabela.column("#", width=40, anchor="center")

    # Colunas com apenas os nomes reais (sem A, B, C...)
    for header, nome_real in zip(headers_alfabeticos, colunas_reais):
        largura_nome = len(nome_real) * 9
        largura_minima = max(120, largura_nome)
        
        tabela.heading(header, text=nome_real)  # Só o nome real
        tabela.column(header, width=largura_minima, anchor="center", stretch=True)

def aplicar_cores_grupos(tabela, linhas_agrupadas):
    if not tabela or not linhas_agrupadas:
        return

    cores_grupos = [
        "#E3F2FD", "#F3E5F5", "#E8F5E8", "#FFF3E0",
        "#FCE4EC", "#F1F8E9", "#E0F2F1", "#FFF8E1",
    ]
    for i, cor in enumerate(cores_grupos):
        tabela.tag_configure(f"grupo_{i}", background=cor, foreground="black")

    for grupo_idx, (_, linhas) in enumerate(linhas_agrupadas.items()):
        cor_tag = f"grupo_{grupo_idx % len(cores_grupos)}"
        for idx in linhas:
            try:
                children = tabela.get_children()
                if idx < len(children):
                    item_id = children[idx]
                    tabela.item(item_id, tags=(cor_tag,))
            except:
                continue