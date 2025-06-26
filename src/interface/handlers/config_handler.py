"""
Configuration handler module.
Contains functions for managing application configuration.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from core.config.setup_config import get_setup_time, TEMPOS_SETUP
from src.interface import globals

def abrir_configuracoes():
    """Abre a janela de configurações dos tempos de setup"""
    config_window = tk.Toplevel()
    config_window.title("Configuração de Tempos de Setup")
    config_window.geometry("500x400")
    config_window.resizable(False, False)

    main_frame = ttk.Frame(config_window, padding="10")
    main_frame.pack(fill="both", expand=True)

    # Tabela de tempos de setup
    tree = ttk.Treeview(main_frame, columns=("Processo", "Tempo (min)"), show="headings")
    tree.heading("Processo", text="Processo")
    tree.heading("Tempo (min)", text="Tempo (min)")
    tree.column("Processo", width=250)
    tree.column("Tempo (min)", width=100)
    tree.pack(fill="both", expand=True, pady=10)

    # Preenche a tabela
    def atualizar_tabela():
        tree.delete(*tree.get_children())
        for proc, tempo in TEMPOS_SETUP.items():
            tree.insert("", "end", values=(proc, tempo))

    atualizar_tabela()

    # Função para editar célula
    def editar_celula(event):
        item = tree.identify_row(event.y)
        coluna = tree.identify_column(event.x)
        if not item or coluna != "#2":
            return
        valor_atual = tree.item(item, "values")[1]
        novo_valor = simpledialog.askinteger("Editar Tempo", "Novo tempo (min):", initialvalue=valor_atual, minvalue=1)
        if novo_valor:
            proc = tree.item(item, "values")[0]
            TEMPOS_SETUP[proc] = novo_valor
            atualizar_tabela()

    tree.bind("<Double-1>", editar_celula)

    # Adicionar novo processo
    def adicionar_processo():
        proc = simpledialog.askstring("Novo Processo", "Nome do processo:")
        if not proc:
            return
        if proc in TEMPOS_SETUP:
            messagebox.showwarning("Aviso", "Esse processo já existe!")
            return
        tempo = simpledialog.askinteger("Tempo", "Tempo de setup (min):", minvalue=1)
        if tempo:
            TEMPOS_SETUP[proc] = tempo
            atualizar_tabela()

    # Remover processo selecionado
    def remover_processo():
        item = tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um processo para remover.")
            return
        proc = tree.item(item[0], "values")[0]
        if messagebox.askyesno("Remover", f"Remover o processo '{proc}'?"):
            del TEMPOS_SETUP[proc]
            atualizar_tabela()

    # Botões
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=5)
    ttk.Button(btn_frame, text="Adicionar Processo", command=adicionar_processo).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Remover Processo", command=remover_processo).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Salvar", command=lambda: (messagebox.showinfo("Sucesso", "Configuração salva!"), config_window.destroy())).pack(side="right", padx=5)
    ttk.Button(btn_frame, text="Cancelar", command=config_window.destroy).pack(side="right", padx=5)

    # Centraliza a janela
    config_window.update_idletasks()
    width = config_window.winfo_width()
    height = config_window.winfo_height()
    x = (config_window.winfo_screenwidth() // 2) - (width // 2)
    y = (config_window.winfo_screenheight() // 2) - (height // 2)
    config_window.geometry(f'{width}x{height}+{x}+{y}')

    config_window.transient(globals.window)
    config_window.grab_set()
    globals.window.wait_window(config_window)

def configure_machine_settings(machine_type):
    """Configure machine specific settings"""
    setup_time = get_setup_time(machine_type)
    return {
        'setup_time': setup_time,
        'machine_type': machine_type
    }

def validate_config(config):
    """Validate configuration settings"""
    required_fields = ['setup_time', 'machine_type']
    return all(field in config for field in required_fields)

def get_default_config():
    """Get default configuration"""
    return {
        'setup_time': 45,  # Default setup time in minutes
        'machine_type': 'default'
    }
