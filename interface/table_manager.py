import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from interface import globals

def configurar_tabela():
    """Configura os eventos e menu de contexto da tabela existente"""
    tabela = globals.tabela
    if tabela is not None:
        # Configurar evento de duplo clique para edição
        tabela.bind("<Double-1>", editar_celula)
        
        # Adicionar menu de contexto para manipulação de linhas
        criar_menu_contexto()

def criar_menu_contexto():
    """Cria menu de contexto para a tabela com opções de edição"""
    tabela = globals.tabela
    if tabela is not None:
        menu_contexto = tk.Menu(tabela, tearoff=0)
        menu_contexto.add_command(label="✏️ Editar Célula", command=editar_celula_selecionada)
        menu_contexto.add_separator()
        menu_contexto.add_command(label="➕ Inserir Linha Acima", command=lambda: inserir_linha("acima"))
        menu_contexto.add_command(label="➕ Inserir Linha Abaixo", command=lambda: inserir_linha("abaixo"))
        menu_contexto.add_separator()
        menu_contexto.add_command(label="🗑️ Deletar Linha", command=deletar_linha)
        menu_contexto.add_separator()
        menu_contexto.add_command(label="💾 Salvar Alterações", command=salvar_alteracoes)
        
        def mostrar_menu(event):
            try:
                menu_contexto.tk_popup(event.x_root, event.y_root)
            finally:
                menu_contexto.grab_release()
        
        tabela.bind("<Button-3>", mostrar_menu)  # Botão direito

def editar_celula(event):
    tabela = globals.tabela
    df_global = globals.df_global
    if tabela is not None and df_global is not None:
        # Identificar qual item foi clicado
        item = tabela.identify_row(event.y)
        if item:
            column = tabela.identify_column(event.x)
            if column:
                # Converter coluna para índice (ex: "#2" -> 1)
                col_index = int(column.replace("#", "")) - 1
                if col_index >= 0:
                    iniciar_edicao_celula(item, column, col_index)

def editar_celula_selecionada():
    tabela = globals.tabela
    if tabela is not None:
        selecionadas = tabela.selection()
        if selecionadas:
            item = selecionadas[0]
            column = "#1"  # Primeira coluna
            iniciar_edicao_celula(item, column, 0)
        else:
            messagebox.showwarning("Aviso", "Selecione uma linha para editar.")

def extrair_tempo_setup_do_processo(processo):
    import re
    texto = str(processo).lower()
    # Pega 'X h Y min', 'Xh', 'Y min', etc.
    horas = 0
    minutos = 0
    match_hora = re.search(r'(\d{1,2})\s*h', texto)
    match_min = re.search(r'(\d{1,3})\s*min', texto)
    if match_hora:
        horas = int(match_hora.group(1))
    if match_min:
        minutos = int(match_min.group(1))
    total_min = horas * 60 + minutos
    if total_min > 0:
        return total_min
    return None

def iniciar_edicao_celula(item, column, col_index):
    tabela = globals.tabela
    df_global = globals.df_global
    if tabela is None or df_global is None:
        return
    
    # Obter valor atual da célula
    old_value = tabela.set(item, column)
    
    # Obter posição da célula
    bbox = tabela.bbox(item, column)
    if not bbox:
        return
    
    # Criar entry para edição
    entry = tk.Entry(tabela, font=('Arial', 9))
    entry.insert(0, str(old_value))
    
    # Posicionar o entry sobre a célula
    entry.place(x=bbox[0], y=bbox[1], width=bbox[2], height=bbox[3])
    
    def salvar_edicao():
        new_value = entry.get()
        tabela.set(item, column, new_value)
        
        # Atualizar DataFrame global
        linha_index = tabela.index(item)
        if 0 <= linha_index < len(df_global):
            # Se for a primeira coluna (índice), não atualizar o DataFrame
            if col_index > 0:
                col_name = df_global.columns[col_index - 1]  # Ajustar para primeira coluna ser índice
                df_global.at[linha_index, col_name] = new_value
                # Se editou o Processo, atualizar Tempo Setup
                if col_name.lower() == 'processo':
                    tempo_setup = extrair_tempo_setup_do_processo(new_value)
                    if tempo_setup:
                        df_global.at[linha_index, 'Tempo Setup'] = f"{tempo_setup:02d}:00"
                    else:
                        df_global.at[linha_index, 'Tempo Setup'] = ''
                    # Sincronizar toda a coluna após edição
                    sincronizar_tempo_setup()
                if col_name.lower() == 'velocidade média':
                    sincronizar_velocidade_com_media()
        
        entry.destroy()
        
        # Feedback visual
        text_resultado = globals.text_resultado
        if text_resultado:
            text_resultado.insert(tk.END, f"✏️ Célula editada: Linha {linha_index + 1}, Coluna {column}\n")
            text_resultado.see(tk.END)
    
    def cancelar_edicao():
        entry.destroy()
    
    # Eventos para salvar/cancelar
    entry.bind("<Return>", lambda e: salvar_edicao())
    entry.bind("<Escape>", lambda e: cancelar_edicao())
    entry.bind("<FocusOut>", lambda e: salvar_edicao())
    
    entry.focus_set()
    entry.select_range(0, tk.END)

def inserir_linha(posicao="abaixo"):
    tabela = globals.tabela
    df_global = globals.df_global
    linhas_selecionadas = globals.linhas_selecionadas
    import interface.ui_setup as ui_setup
    
    if tabela is None or df_global is None:
        messagebox.showwarning("Aviso", "Nenhuma tabela carregada para editar.")
        return
    
    # Determinar onde inserir
    if linhas_selecionadas:
        linha_ref = linhas_selecionadas[0]
        if posicao == "acima":
            insert_index = linha_ref
        else:
            insert_index = linha_ref + 1
    else:
        insert_index = len(df_global)
    
    # Criar nova linha vazia
    nova_linha = pd.Series([''] * len(df_global.columns), index=df_global.columns)
    # Inicializar Tempo Setup e Velocidade
    if 'Tempo Setup' in nova_linha.index:
        nova_linha['Tempo Setup'] = ''
    if 'Velocidade' in nova_linha.index:
        from interface import globals as gbl
        try:
            nova_linha['Velocidade'] = float(gbl.entrada_velocidade_media.get())
        except:
            nova_linha['Velocidade'] = ''
    # Inserir no DataFrame
    if insert_index >= len(df_global):
        # Inserir no final
        df_global.loc[len(df_global)] = nova_linha
    else:
        # Inserir no meio - recriar DataFrame
        df_parte1 = df_global.iloc[:insert_index].copy()
        df_parte2 = df_global.iloc[insert_index:].copy()
        nova_linha_df = pd.DataFrame([nova_linha])
        
        df_novo = pd.concat([df_parte1, nova_linha_df, df_parte2], ignore_index=True)
        globals.df_global = df_novo
    
    # Recarregar tabela
    ui_setup.carregar_dados_na_tabela()
    # Sincronizar Tempo Setup e Velocidade
    sincronizar_tempo_setup()
    sincronizar_velocidade_com_media()
    ui_setup.carregar_dados_na_tabela()
    messagebox.showinfo("Sucesso", f"Nova linha inserida {posicao} da seleção.")

def deletar_linha():
    tabela = globals.tabela
    df_global = globals.df_global
    linhas_selecionadas = globals.linhas_selecionadas
    import interface.ui_setup as ui_setup
    
    if not linhas_selecionadas:
        messagebox.showwarning("Aviso", "Selecione uma linha para deletar.")
        return
    
    if messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar a(s) linha(s) selecionada(s)?"):
        # Ordenar índices em ordem decrescente para deletar do final para o início
        indices_para_deletar = sorted(linhas_selecionadas, reverse=True)
        
        for index in indices_para_deletar:
            if 0 <= index < len(df_global):
                df_global.drop(df_global.index[index], inplace=True)
        
        # Resetar índices
        df_global.reset_index(drop=True, inplace=True)
        globals.df_global = df_global
        
        # Recarregar tabela
        ui_setup.carregar_dados_na_tabela()
        messagebox.showinfo("Sucesso", f"{len(indices_para_deletar)} linha(s) deletada(s).")

def salvar_alteracoes():
    df_global = globals.df_global
    text_resultado = globals.text_resultado
    
    if df_global is None or df_global.empty:
        messagebox.showwarning("Aviso", "Nenhum dado para salvar.")
        return
    
    try:
        if text_resultado:
            text_resultado.insert(tk.END, f"\n✅ Alterações salvas em memória - {len(df_global)} linhas\n")
            text_resultado.see(tk.END)
        
        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar alterações: {str(e)}")

def exportar_dados():
    df_global = globals.df_global
    from tkinter import filedialog
    
    if df_global is None or df_global.empty:
        messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
        return
    
    try:
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if arquivo:
            if arquivo.endswith('.xlsx'):
                df_global.to_excel(arquivo, index=False)
            else:
                df_global.to_csv(arquivo, index=False)
            
            messagebox.showinfo("Sucesso", f"Dados exportados para: {arquivo}")
    
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar dados: {str(e)}")

def sincronizar_tempo_setup():
    """Sincroniza o tempo de setup conforme a máquina selecionada, atualizando o DataFrame global corretamente."""
    df_global = globals.df_global
    from interface import globals as gbl
    if df_global is not None and not df_global.empty:
        maquina = gbl.entrada_maquina.get().strip().lower() if gbl.entrada_maquina else ''
        novos_setups = []
        for idx, row in df_global.iterrows():
            processo = row.get('Processo', '')
            tempo_setup = extrair_tempo_setup_do_processo(processo)
            if 'komori' in maquina:
                if tempo_setup:
                    novos_setups.append(f"{tempo_setup:02d}:00")
                else:
                    novos_setups.append('')
            elif 'bobst' in maquina:
                if tempo_setup:
                    novos_setups.append(f"{tempo_setup:02d}:00")
                else:
                    novos_setups.append('03:00')
            else:
                if tempo_setup:
                    novos_setups.append(f"{tempo_setup:02d}:00")
                else:
                    novos_setups.append('')
        df_global['Tempo Setup'] = novos_setups
        globals.df_global = df_global

def sincronizar_velocidade_com_media():
    """Atualiza a coluna 'Velocidade' para todas as linhas com o valor da 'Velocidade Média', exceto onde já foi editado manualmente."""
    df_global = globals.df_global
    from interface import globals as gbl
    if df_global is not None and not df_global.empty:
        try:
            velocidade_media = float(gbl.entrada_velocidade_media.get())
        except:
            velocidade_media = None
        if velocidade_media is not None:
            for idx, row in df_global.iterrows():
                # Se estiver vazio ou igual ao valor anterior da média, atualiza
                if not row.get('Velocidade') or str(row.get('Velocidade')).strip() == '' or str(row.get('Velocidade')).strip() == str(gbl.velocidade_media_anterior):
                    df_global.at[idx, 'Velocidade'] = velocidade_media
    # Atualiza valor anterior
    gbl.velocidade_media_anterior = velocidade_media