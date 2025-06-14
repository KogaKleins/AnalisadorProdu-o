import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

def configurar_tabela():
    """Configura os eventos e menu de contexto da tabela existente"""
    from interface.ui_setup import tabela
    
    if tabela is not None:
        # Configurar evento de duplo clique para edição
        tabela.bind("<Double-1>", editar_celula)
        
        # Adicionar menu de contexto para manipulação de linhas
        criar_menu_contexto()

def criar_menu_contexto():
    """Cria menu de contexto para a tabela com opções de edição"""
    from interface.ui_setup import tabela
    
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
    """Edita célula clicada com duplo-click"""
    from interface.ui_setup import tabela, df_global
    
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
    """Edita a primeira célula da linha selecionada"""
    from interface.ui_setup import tabela
    
    if tabela is not None:
        selecionadas = tabela.selection()
        if selecionadas:
            item = selecionadas[0]
            column = "#1"  # Primeira coluna
            iniciar_edicao_celula(item, column, 0)
        else:
            messagebox.showwarning("Aviso", "Selecione uma linha para editar.")

def iniciar_edicao_celula(item, column, col_index):
    """Inicia a edição de uma célula específica"""
    from interface.ui_setup import tabela, df_global
    
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
        
        entry.destroy()
        
        # Feedback visual
        from interface.ui_setup import text_resultado
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
    """Insere uma nova linha na posição especificada"""
    from interface.ui_setup import tabela, df_global, linhas_selecionadas
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
        ui_setup.df_global = df_novo
    
    # Recarregar tabela
    ui_setup.carregar_dados_na_tabela()
    messagebox.showinfo("Sucesso", f"Nova linha inserida {posicao} da seleção.")

def deletar_linha():
    """Deleta a linha selecionada"""
    from interface.ui_setup import tabela, df_global, linhas_selecionadas
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
        ui_setup.df_global = df_global
        
        # Recarregar tabela
        ui_setup.carregar_dados_na_tabela()
        messagebox.showinfo("Sucesso", f"{len(indices_para_deletar)} linha(s) deletada(s).")

def salvar_alteracoes():
    """Salva as alterações feitas na tabela"""
    from interface.ui_setup import df_global, text_resultado
    
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
    """Exporta os dados editados para CSV"""
    from interface.ui_setup import df_global
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