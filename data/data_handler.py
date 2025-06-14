import pandas as pd
from tkinter import messagebox
import tkinter as tk
from extrator.caminhos import construir_caminho_pdf
from extrator.extrator_pdf import extrair_dados_pdf
from config.setup_config import tempos_setup  # Importação de tempos_setup

def calcular_tempo_setup(processo, os_anterior=None):
    """Calcula o tempo de setup baseado no processo e OS anterior"""
    processo_lower = processo.lower()
    
    # Verificar se contém "berço"
    if "berço" in processo_lower or "berco" in processo_lower:
        return tempos_setup['berco']
    
    # Verificar colagem bandeja
    if "colagem" in processo_lower and "bandeja" in processo_lower:
        return tempos_setup['colagem_bandeja']
    
    # Verificar fundo automático
    if "fundo" in processo_lower and "automatic" in processo_lower.replace("ô", "o").replace("á", "a"):
        if os_anterior is None:
            return tempos_setup['fundo_automatico_primeiro']
        else:
            return tempos_setup['fundo_automatico_outros']
    
    # Verificar colagem lateral
    if "colagem" in processo_lower and ("lateral" in processo_lower or "lat" in processo_lower):
        if os_anterior is None:
            return tempos_setup['colagem_lateral_primeiro']
        else:
            return tempos_setup['colagem_lateral_outros']
    
    # Padrão
    return tempos_setup['default']

def carregar_dados(data, maquina):
    # Importação dinâmica das variáveis globais
    import interface.ui_setup as ui_setup
    
    if not data or not maquina:
        messagebox.showwarning("Atenção", "Preencha a data e a máquina.")
        return

    try:
        caminho_pdf = construir_caminho_pdf(data, maquina)
        df = extrair_dados_pdf(caminho_pdf)

        # Detectar cabeçalho real na primeira linha
        header = list(df.iloc[0])
        df = df[1:].reset_index(drop=True)
        df.columns = header
        
        # Inserir nova coluna C para tempo de setup
        if len(df.columns) >= 3:
            colunas_antigas = df.columns.tolist()
            novas_colunas = colunas_antigas[:2] + ['Tempo Setup'] + colunas_antigas[2:]
            
            df_novo = pd.DataFrame(index=df.index)
            df_novo[novas_colunas[0]] = df[colunas_antigas[0]]  # A
            df_novo[novas_colunas[1]] = df[colunas_antigas[1]]  # B
            df_novo['Tempo Setup'] = ''  # Nova coluna C - SEMPRE VAZIA INICIALMENTE
            
            # Copiar as demais colunas
            for i, col_antiga in enumerate(colunas_antigas[2:], start=3):
                df_novo[novas_colunas[i]] = df[col_antiga]
            
            df = df_novo
        
        # Calcular tempos de setup automaticamente - CORREÇÃO AQUI
        os_anteriores_por_processo = {}
        
        for idx, row in df.iterrows():
            # Buscar processo
            processo = ""
            for col in df.columns:
                if "processo" in str(col).lower():
                    processo = str(row.get(col, ""))
                    break
            
            # Buscar OS
            os_value = ""
            for col in df.columns:
                if col.upper() == "OS" or "os" in str(col).lower():
                    os_value = str(row.get(col, ""))
                    break
            
            # Buscar evento
            evento = ""
            for col in df.columns:
                if "evento" in str(col).lower():
                    evento = str(row.get(col, "")).strip().lower()
                    break
            
            # CORREÇÃO: Somente atribui tempo de setup se o evento for "acerto" ou similar
            # E não for "produção"
            if processo and evento and evento != "produção":
                # Verificar se é evento de acerto/setup
                eventos_setup = ["acerto", "setup", "ajuste", "troca", "preparação"]
                is_evento_setup = any(termo in evento for termo in eventos_setup)
                
                if is_evento_setup:
                    tipo_processo = processo.lower()
                    os_anterior = os_anteriores_por_processo.get(tipo_processo)
                    
                    tempo_setup = calcular_tempo_setup(processo, os_anterior)
                    df.at[idx, 'Tempo Setup'] = f"{tempo_setup//60}:{tempo_setup%60:02d}"
                else:
                    # Para eventos que não são setup (como "ócioso"), deixar vazio
                    df.at[idx, 'Tempo Setup'] = ""
            else:
                # Para produção ou eventos vazios, deixar vazio
                df.at[idx, 'Tempo Setup'] = ""
            
            # Atualizar OS anterior apenas se houver OS válido
            if processo and os_value and os_value != "0" and os_value.strip():
                tipo_processo = processo.lower()
                os_anteriores_por_processo[tipo_processo] = os_value

        # Atualizar a variável global corretamente
        ui_setup.df_global = df.copy()
        ui_setup.linhas_agrupadas = {}

        # Importação dinâmica e configuração da tabela
        from interface.table_manager import configurar_tabela, carregar_dados_na_tabela
        configurar_tabela()
        carregar_dados_na_tabela()

        if ui_setup.text_resultado:
            ui_setup.text_resultado.delete("1.0", tk.END)
            ui_setup.text_resultado.insert(tk.END, "Dados carregados! Selecione linhas e clique em 'Agrupar' ou 'Calcular Desempenho'")

    except Exception as e:
        messagebox.showerror("Erro", str(e))