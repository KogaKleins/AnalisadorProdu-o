import tkinter as tk
from tkinter import messagebox

# Definição do dicionário de tempos de setup (em minutos)
tempos_setup = {
    'berco': 180,  # Tempo para processos com "berço"
    'colagem_bandeja': 130,  # Tempo para colagem de bandeja
    'fundo_automatico_primeiro': 130,  # Primeiro fundo automático
    'fundo_automatico_outros': 30,  # Outros fundos automáticos
    'colagem_lateral_primeiro': 130,  # Primeiro colagem lateral
    'colagem_lateral_outros': 15,  # Outros colagem lateral
    'default': 180  # Tempo padrão
}

def abrir_configuracoes(janela):
    """
    Abre uma janela de configuração onde o usuário pode ajustar os tempos de setup.
    Recebe a janela principal como argumento para criar uma janela secundária.
    """
    # Criar uma janela secundária
    config_window = tk.Toplevel(janela)
    config_window.title("Configurações de Setup")
    config_window.geometry("400x300")
    config_window.transient(janela)  # Faz a janela ficar na frente da principal
    config_window.grab_set()  # Bloqueia interação com a janela principal até fechar

    # Frame para organizar os widgets
    frame_config = tk.Frame(config_window, padx=10, pady=10)
    frame_config.pack(expand=True, fill="both")

    # Rótulos e entradas para editar tempos de setup
    tk.Label(frame_config, text="Tempos de Setup (em minutos):", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=5)

    # Dicionário para mapear entradas
    entry_vars = {}
    row = 1
    for key, value in tempos_setup.items():
        tk.Label(frame_config, text=f"{key.replace('_', ' ').title()}: ").grid(row=row, column=0, sticky="e", padx=5, pady=2)
        entry_var = tk.StringVar(value=str(value))
        entry = tk.Entry(frame_config, textvariable=entry_var, width=10)
        entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
        entry_vars[key] = entry_var
        row += 1

    # Botão para salvar alterações
    def salvar_configuracoes():
        try:
            for key, entry_var in entry_vars.items():
                novo_valor = int(entry_var.get())
                if novo_valor < 0:
                    raise ValueError("Os tempos não podem ser negativos.")
                tempos_setup[key] = novo_valor
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
            config_window.destroy()
        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

    tk.Button(frame_config, text="Salvar", command=salvar_configuracoes, bg='#4CAF50', fg='white', font=('Arial', 10)).grid(row=row, column=0, columnspan=2, pady=10)

    # Botão para cancelar
    tk.Button(frame_config, text="Cancelar", command=config_window.destroy, bg='#F44336', fg='white', font=('Arial', 10)).grid(row=row+1, column=0, columnspan=2, pady=5)