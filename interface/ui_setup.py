import tkinter as tk
from tkinter import ttk, font
from interface import globals
from interface.formatters import ao_pressionar_enter, ao_digitar_data, ao_digitar_hora_inicio, ao_digitar_hora_fim
from data.data_handler import carregar_dados
from data.group_manager import agrupar_selecionadas, desagrupar_selecionadas
from config.setup_config import abrir_configuracoes
from interface.visual_layout import gerar_headers_colunas, configurar_colunas_da_tabela, aplicar_cores_grupos, criar_headers_alfabeticos
from interface.terminal_panel import criar_terminal_painel
from interface.table_manager import configurar_tabela
import pandas as pd  # Importação do pandas para correção da média geral

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
    import interface.globals as globals
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
    globals.frame_headers = frame_headers
    globals.frame_tabela_container = frame_tabela_container

def ao_selecionar_linha(event):
    global linhas_selecionadas, label_selecao, tabela
    if tabela is not None:
        item = tabela.selection()
        linhas_selecionadas.clear()
        linhas_selecionadas.extend(tabela.index(i) for i in item)
        label_selecao.config(text=f"{len(linhas_selecionadas)} linha(s) selecionada(s)" if linhas_selecionadas else "Nenhuma linha selecionada")

def carregar_dados_na_tabela():
    global tabela, df_global, label_selecao, linhas_selecionadas, frame_headers, frame_tabela_container
    from interface.table_manager import configurar_colunas_da_tabela, aplicar_cores_grupos, sincronizar_tempo_setup, sincronizar_velocidade_com_media
    # --- Garantir colunas obrigatórias e ordem ---
    obrigatorias = ['Tempo Setup', 'Velocidade']
    for col in obrigatorias:
        if df_global is not None and col not in df_global.columns:
            df_global[col] = ''
    # Reordena para garantir posição após 'Término' (ou no final se não existir)
    if df_global is not None:
        cols = list(df_global.columns)
        for col in obrigatorias:
            if col in cols:
                cols.remove(col)
        # Insere após 'Término' se existir
        if 'Término' in cols:
            idx = cols.index('Término') + 1
        else:
            idx = len(cols)
        for i, col in enumerate(obrigatorias):
            cols.insert(idx + i, col)
        df_global = df_global[cols]
    # --- Sincronizar dados ---
    sincronizar_tempo_setup()
    sincronizar_velocidade_com_media()
    # --- Atualizar tabela visual ---
    if tabela is not None and df_global is not None and not df_global.empty:
        for item in tabela.get_children():
            tabela.delete(item)
        num_colunas = len(df_global.columns)
        from interface.visual_layout import gerar_headers_colunas, criar_headers_alfabeticos
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
    sincronizar_variaveis_globais()
    # Atualizar média geral visual SEMPRE
    if hasattr(globals, 'label_media_geral'):
        try:
            df = globals.df_global
            if df is not None and 'Velocidade' in df.columns and not df.empty:
                media = pd.to_numeric(df['Velocidade'], errors='coerce').mean()
                globals.label_media_geral.config(text=f"Média Geral: {media:,.0f} p/h")
            else:
                globals.label_media_geral.config(text="Média Geral: -")
        except:
            globals.label_media_geral.config(text="Média Geral: -")
    # Atualiza df_global global
    globals.df_global = df_global

def carregar_dados_wrapper():
    global entrada_data, entrada_maquina
    carregar_dados(entrada_data.get(), entrada_maquina.get())
    carregar_dados_na_tabela()
    sincronizar_variaveis_globais()

def agrupar_selecionadas_melhorado():
    from data.performance_calculator import calcular_desempenho  # Import local para evitar circularidade
    agrupar_selecionadas()
    aplicar_cores_grupos(tabela, linhas_agrupadas)

def desagrupar_selecionadas_melhorado():
    from data.performance_calculator import calcular_desempenho  # Import local para evitar circularidade
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
    print("Ola")  # Console log solicitado
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

    tk.Label(frame_principal, text="Velocidade Média:", bg='#f5f5f5', font=('Arial', 10, 'bold')).grid(row=0, column=6, sticky="w", padx=5)
    entrada_velocidade_media = tk.Entry(frame_principal, width=10, font=('Arial', 10, 'bold'), fg='#0055aa')
    entrada_velocidade_media.grid(row=0, column=7, padx=5)
    entrada_velocidade_media.insert(0, "6000")
    globals.entrada_velocidade_media = entrada_velocidade_media

    # Campo visual para exibir a média geral de velocidade
    label_media_geral = tk.Label(frame_principal, text="Média Geral: -", bg='#e0e0e0', font=('Arial', 10, 'bold'), fg='#0055aa')
    label_media_geral.grid(row=0, column=8, padx=10)
    globals.label_media_geral = label_media_geral

    def atualizar_media_geral():
        df = globals.df_global
        if df is not None and 'Velocidade' in df.columns and not df.empty:
            try:
                media = df['Velocidade'].astype(float).mean()
                label_media_geral.config(text=f"Média Geral: {media:,.0f} p/h")
            except:
                label_media_geral.config(text="Média Geral: -")
        else:
            label_media_geral.config(text="Média Geral: -")

    # Atualizar sempre que carregar dados ou alterar velocidade média
    def carregar_dados_na_tabela_com_media():
        carregar_dados_na_tabela()
        atualizar_media_geral()
    globals.carregar_dados_na_tabela_com_media = carregar_dados_na_tabela_com_media

    def aplicar_velocidade_media(event=None):
        from interface import globals
        valor = entrada_velocidade_media.get()
        try:
            valor_float = float(valor)
        except ValueError:
            return
        df = globals.df_global
        if df is not None and 'Velocidade' in df.columns:
            for idx, row in df.iterrows():
                # Só atualiza se for Komori e se não foi editado manualmente (valor igual ao anterior ou igual ao padrão)
                if globals.entrada_maquina.get().strip().lower() == 'komori' or globals.entrada_maquina.get().strip() == '1':
                    atual = str(row['Velocidade'])
                    if atual == '' or atual == '6000' or atual == str(globals.entrada_velocidade_media._last_value) or atual == str(valor_float):
                        df.at[idx, 'Velocidade'] = valor_float
            globals.df_global = df
            carregar_dados_na_tabela()
        globals.entrada_velocidade_media._last_value = valor_float

    entrada_velocidade_media._last_value = 6000
    entrada_velocidade_media.bind("<Return>", aplicar_velocidade_media)
    entrada_velocidade_media.bind("<FocusOut>", aplicar_velocidade_media)

    frame_periodo = tk.LabelFrame(frame_principal, text="Período de Trabalho", bg='#f5f5f5')
    frame_periodo.grid(row=1, column=0, columnspan=6, sticky="ew", padx=5, pady=5)

    tk.Label(frame_periodo, text="Início:", bg='#f5f5f5').grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entrada_hora_inicio = tk.Entry(frame_periodo, width=22)  # Aumentado para datas completas
    entrada_hora_inicio.grid(row=0, column=1, padx=5, pady=5)
    entrada_hora_inicio.bind("<KeyRelease>", lambda event: ao_digitar_hora_inicio(entrada_hora_inicio, event))

    tk.Label(frame_periodo, text="Fim:", bg='#f5f5f5').grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entrada_hora_fim = tk.Entry(frame_periodo, width=22)  # Aumentado para datas completas
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
    tk.Button(frame_agrupamento, text="📈 Calcular Desempenho", command=lambda: __import__('data.performance_calculator').performance_calculator.calcular_desempenho()).pack(side="left", padx=5)

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
    # Configurar evento de duplo clique para edição de célula
    from interface.table_manager import editar_celula
    tabela.bind("<Double-1>", editar_celula)

    # CORREÇÃO: Configurar tabela APÓS criá-la
    from interface.table_manager import configurar_tabela
    configurar_tabela()
    sincronizar_variaveis_globais()

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

    # Mapeamento de máquinas
    MAPA_MAQUINAS = {
        '1': 'KOMORI',
        '2': 'HCD',
        '3': 'SBL',
        '4': 'FURNAX',
        '5': 'C/V MANUAL',
        '6': 'SAMKOON',
        '7': 'LAMINADORA',
        '8': 'VERNIZ UV SAKURAI',
        '9': 'BOBST',
    }
    def ao_digitar_maquina(event=None):
        valor = entrada_maquina.get().strip()
        if valor in MAPA_MAQUINAS:
            entrada_maquina.delete(0, tk.END)
            entrada_maquina.insert(0, MAPA_MAQUINAS[valor])

    def ao_maquina_enter(event=None):
        ao_digitar_maquina()
        carregar_dados_wrapper()

    entrada_maquina.bind("<Return>", ao_maquina_enter)
    entrada_maquina.bind("<FocusOut>", ao_digitar_maquina)

    def autocompletar_maquina(event=None):
        valor = entrada_maquina.get().strip().lower()
        # Se for número
        if valor in MAPA_MAQUINAS:
            entrada_maquina.delete(0, tk.END)
            entrada_maquina.insert(0, MAPA_MAQUINAS[valor])
            return
        # Se for prefixo de nome
        for nome in MAPA_MAQUINAS.values():
            if nome.lower().startswith(valor) and valor:
                entrada_maquina.delete(0, tk.END)
                entrada_maquina.insert(0, nome)
                return
    entrada_maquina.bind("<KeyRelease>", autocompletar_maquina)
    entrada_maquina.bind("<FocusOut>", autocompletar_maquina)
    entrada_maquina.bind("<Return>", ao_maquina_enter)

    from datetime import datetime, timedelta
    hoje = datetime.now()
    if hoje.weekday() == 0:  # Segunda-feira
        sugestao = hoje - timedelta(days=3)
    else:
        sugestao = hoje - timedelta(days=1)
    entrada_data.insert(0, sugestao.strftime("%d/%m/%Y"))

    # Permitir formato completo no campo de hora início/fim
    def ao_digitar_hora_inicio_completo(entry, event):
        valor = entry.get().strip()
        # Aceita formatos: 'dd/mm/yyyy HH:MM', 'dd/mm/yyyy - HH:MM', 'HH:MM', 'H:MM', etc.
        import re
        if re.match(r"^(\d{2}/\d{2}/\d{4}\s*-?\s*)?\d{1,2}:\d{2}$", valor):
            entry.config(bg='#d0ffd0')
        else:
            entry.config(bg='#ffd0d0')
    entrada_hora_inicio.bind("<KeyRelease>", lambda event: ao_digitar_hora_inicio_completo(entrada_hora_inicio, event))
    entrada_hora_fim.bind("<KeyRelease>", lambda event: ao_digitar_hora_inicio_completo(entrada_hora_fim, event))

    janela.mainloop()

if __name__ == "__main__":
    abrir_janela()