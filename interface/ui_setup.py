import tkinter as tk
from tkinter import ttk, font
from interface import globals
from interface.formatters import ao_pressionar_enter, ao_digitar_data, ao_digitar_hora_inicio, ao_digitar_hora_fim
from data.data_handler import carregar_dados
from data.group_manager import agrupar_selecionadas, desagrupar_selecionadas
from data.performance_calculator import calcular_desempenho
from config.setup_config import abrir_configuracoes
from interface.visual_layout import gerar_headers_colunas, configurar_colunas_da_tabela, aplicar_cores_grupos, criar_headers_alfabeticos
from interface.terminal_panel import criar_terminal_painel
from interface.table_manager import configurar_tabela

# Variáveis globais
df_global = None
tabela = None
text_resultado = None
label_selecao = None
linhas_agrupadas = {}
linhas_selecionadas = []
entrada_hora_inicio = None
entrada_hora_fim = None
entrada_intervalo = None
entrada_data = None
entrada_maquina = None
frame_headers = None
frame_tabela_container = None

def sincronizar_variaveis_globais():
    globals.df_global = df_global
    globals.tabela = tabela
    globals.text_resultado = text_resultado
    globals.label_selecao = label_selecao
    globals.linhas_agrupadas = linhas_agrupadas
    globals.linhas_selecionadas = linhas_selecionadas
    globals.entrada_hora_inicio = entrada_hora_inicio
    globals.entrada_hora_fim = entrada_hora_fim
    globals.entrada_intervalo = entrada_intervalo
    globals.entrada_data = entrada_data
    globals.entrada_maquina = entrada_maquina

def ao_selecionar_linha(event):
    global linhas_selecionadas, label_selecao, tabela
    if tabela is not None:
        item = tabela.selection()
        linhas_selecionadas.clear()
        linhas_selecionadas.extend(tabela.index(i) for i in item)
        label_selecao.config(text=f"{len(linhas_selecionadas)} linha(s) selecionada(s)" if linhas_selecionadas else "Nenhuma linha selecionada")

def carregar_dados_na_tabela():
    global tabela, df_global, label_selecao, linhas_selecionadas, frame_headers, frame_tabela_container
    if tabela is not None and df_global is not None and not df_global.empty:
        for item in tabela.get_children():
            tabela.delete(item)

        num_colunas = len(df_global.columns)
        headers_alfabeticos = gerar_headers_colunas(num_colunas)
        
        if frame_headers is not None:
            frame_headers.destroy()
        frame_headers = criar_headers_alfabeticos(frame_tabela_container, headers_alfabeticos, df_global.columns)
        
        configurar_colunas_da_tabela(tabela, headers_alfabeticos, df_global.columns)

        for index, row in df_global.iterrows():
            valores = list(row)
            tabela.insert("", "end", values=[index + 1] + valores)

        aplicar_cores_grupos(tabela, linhas_agrupadas)
        linhas_selecionadas.clear()
        label_selecao.config(text="Nenhuma linha selecionada")

def carregar_dados_wrapper():
    global entrada_data, entrada_maquina
    carregar_dados(entrada_data.get(), entrada_maquina.get())
    carregar_dados_na_tabela()
    sincronizar_variaveis_globais()

def agrupar_selecionadas_melhorado():
    agrupar_selecionadas()
    aplicar_cores_grupos(tabela, linhas_agrupadas)

def desagrupar_selecionadas_melhorado():
    global tabela
    if tabela:
        for item in tabela.get_children():
            tabela.item(item, tags=())
    desagrupar_selecionadas()
    aplicar_cores_grupos(tabela, linhas_agrupadas)

def criar_menu_edicao(frame_botoes):
    from interface.table_manager import inserir_linha, deletar_linha, salvar_alteracoes, exportar_dados
    
    frame_edicao = tk.LabelFrame(frame_botoes, text="📝 Edição da Tabela", bg='#f5f5f5')
    frame_edicao.pack(side="left", padx=10, fill="y")
    
    tk.Button(frame_edicao, text="➕ Nova Linha", command=lambda: inserir_linha("abaixo"), bg='#4CAF50', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
    tk.Button(frame_edicao, text="🗑️ Deletar", command=deletar_linha, bg='#F44336', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
    tk.Button(frame_edicao, text="💾 Salvar", command=salvar_alteracoes, bg='#2196F3', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
    tk.Button(frame_edicao, text="📤 Exportar", command=exportar_dados, bg='#FF9800', fg='white', font=('Arial', 8)).pack(side="left", padx=2)

def abrir_janela():
    global tabela, text_resultado, linhas_agrupadas, linhas_selecionadas, df_global, label_selecao
    global entrada_hora_inicio, entrada_hora_fim, entrada_intervalo, entrada_data, entrada_maquina
    global frame_headers, frame_tabela_container

    janela = tk.Tk()
    janela.title("Analisador de Produção")
    janela.geometry("1800x1000")
    janela.configure(bg='#f5f5f5')

    fonte_padrao = font.nametofont("TkDefaultFont")
    fonte_padrao.configure(size=9)

    frame_principal = tk.Frame(janela, bg='#f5f5f5', relief='raised', bd=1)
    frame_principal.grid(row=0, column=0, columnspan=8, sticky="ew", padx=10, pady=5)

    tk.Label(frame_principal, text="Data:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5)
    entrada_data = tk.Entry(frame_principal, width=12)
    entrada_data.grid(row=0, column=1, padx=5)
    entrada_data.bind("<KeyRelease>", lambda event: ao_digitar_data(entrada_data, event))
    entrada_data.bind("<Return>", ao_pressionar_enter)

    tk.Label(frame_principal, text="Máquina:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5)
    entrada_maquina = tk.Entry(frame_principal, width=15)
    entrada_maquina.grid(row=0, column=3, padx=5)
    entrada_maquina.bind("<Return>", lambda event: carregar_dados_wrapper())

    tk.Button(frame_principal, text="📊 Carregar Dados", command=carregar_dados_wrapper).grid(row=0, column=4, padx=10)
    tk.Button(frame_principal, text="⚙ Config Setup", command=lambda: abrir_configuracoes(janela)).grid(row=0, column=5, padx=5)

    frame_periodo = tk.LabelFrame(frame_principal, text="Período de Trabalho", bg='#f5f5f5')
    frame_periodo.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=5)

    tk.Label(frame_periodo, text="Início:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entrada_hora_inicio = tk.Entry(frame_periodo, width=8)
    entrada_hora_inicio.grid(row=0, column=1, padx=5, pady=5)
    entrada_hora_inicio.bind("<KeyRelease>", lambda event: ao_digitar_hora_inicio(entrada_hora_inicio, event))

    tk.Label(frame_periodo, text="Fim:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entrada_hora_fim = tk.Entry(frame_periodo, width=8)
    entrada_hora_fim.grid(row=0, column=3, padx=5, pady=5)
    entrada_hora_fim.bind("<KeyRelease>", lambda event: ao_digitar_hora_fim(entrada_hora_fim, event))

    tk.Label(frame_periodo, text="Intervalo (min):", bg='#f5f5f5').grid(row=0, column=4, sticky="w", padx=5, pady=5)
    entrada_intervalo = tk.Entry(frame_periodo, width=8)
    entrada_intervalo.grid(row=0, column=5, padx=5, pady=5)
    entrada_intervalo.insert(0, "60")

    frame_botoes = tk.Frame(janela, bg='#f5f5f5')
    frame_botoes.grid(row=2, column=0, columnspan=8, sticky="ew", padx=10, pady=5)

    frame_agrupamento = tk.LabelFrame(frame_botoes, text="🔗 Agrupamento", bg='#f5f5f5')
    frame_agrupamento.pack(side="left", fill="y")
    
    tk.Button(frame_agrupamento, text="🔗 Agrupar", command=agrupar_selecionadas_melhorado).pack(side="left", padx=2)
    tk.Button(frame_agrupamento, text="🔓 Desagrupar", command=desagrupar_selecionadas_melhorado).pack(side="left", padx=2)
    tk.Button(frame_agrupamento, text="📈 Calcular Desempenho", command=calcular_desempenho).pack(side="left", padx=5)

    criar_menu_edicao(frame_botoes)

    label_selecao = tk.Label(frame_botoes, text="Nenhuma linha selecionada", bg='#f5f5f5')
    label_selecao.pack(side="right", padx=10)

    painel = tk.PanedWindow(janela, orient=tk.VERTICAL, sashwidth=8, sashrelief="groove", sashpad=2, bg='#e0e0e0')
    painel.grid(row=3, column=0, columnspan=8, sticky="nsew", padx=10, pady=5)

    janela.grid_rowconfigure(3, weight=1)
    janela.grid_columnconfigure(0, weight=1)

    frame_tabela_superior = tk.Frame(painel, bg='#ffffff', relief='sunken', bd=2)
    painel.add(frame_tabela_superior, height=600, minsize=400)

    frame_tabela_container = tk.Frame(frame_tabela_superior, bg='#ffffff')
    frame_tabela_container.pack(fill="both", expand=True, padx=5, pady=5)

    frame_tree = tk.Frame(frame_tabela_container, bg='#ffffff')
    frame_tree.pack(fill="both", expand=True, pady=(30, 0))

    scrollbar_y = ttk.Scrollbar(frame_tree, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x = ttk.Scrollbar(frame_tree, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")

    tabela = ttk.Treeview(frame_tree, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set, selectmode="extended", height=20)
    tabela.pack(fill="both", expand=True)

    scrollbar_y.config(command=tabela.yview)
    scrollbar_x.config(command=tabela.xview)

    # Configurar evento de seleção
    tabela.bind("<<TreeviewSelect>>", ao_selecionar_linha)

    # CORREÇÃO: Configurar tabela APÓS criá-la
    configurar_tabela()  # Isso vai adicionar o duplo clique e menu de contexto

    frame_inferior = tk.Frame(painel, bg='#2d2d2d', relief='sunken', bd=2)
    painel.add(frame_inferior, height=300, minsize=150)

    frame_terminal, text_resultado_widget = criar_terminal_painel(frame_inferior)
    frame_terminal.pack(fill="both", expand=True)
    text_resultado = text_resultado_widget

    # Adicionar mensagem de feedback sobre a edição
    if text_resultado:
        text_resultado.insert(tk.END, "🎯 Dica: Dê duplo clique em qualquer célula para editá-la!\n")
        text_resultado.insert(tk.END, "🖱️ Clique com botão direito para mais opções de edição.\n\n")

    print(f"DEBUG: Tipo correto de text_resultado: {type(text_resultado)}")

    sincronizar_variaveis_globais()

    janela.mainloop()

if __name__ == "__main__":
    abrir_janela()# oiii