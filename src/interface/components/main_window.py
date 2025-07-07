"""
Main window component module.
Contains the main application window setup and layout.
"""

import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
import sys
import platform
import os
import warnings
from pathlib import Path
sys.path.append('.')
from src.interface import globals
from fpdf import FPDF

from ..components.toolbar import create_toolbar
from ..components.table import create_table_view
from ..components.terminal import create_terminal_panel
from ..handlers.event_handler import register_events
from ..handlers.table_handler import editar_celula, inserir_linha, deletar_linha, aplicar_cores_grupos, editar_celula, configurar_colunas_da_tabela, atualizar_dataframe_global

class MainWindow:
    def __init__(self):
        self.window = tk.Tk()
        sistema = platform.system()
        if sistema == "Windows":
            self.window.state('zoomed')  # Maximiza no Windows
        else:
            self.window.attributes('-zoomed', True)  # Maximiza no Linux/Outros
        self.setup_window()
        self.create_layout()
        self.initialize_components()
        # Adiciona referências dos campos de entrada ao objeto global
        if hasattr(self.toolbar, 'entrada_data'):
            globals.entrada_data = self.toolbar.entrada_data
        if hasattr(self.toolbar, 'entrada_maquina'):
            globals.entrada_maquina = self.toolbar.entrada_maquina
        if hasattr(self.toolbar, 'entrada_hora_inicio'):
            globals.entrada_hora_inicio = self.toolbar.entrada_hora_inicio
        if hasattr(self.toolbar, 'entrada_hora_fim'):
            globals.entrada_hora_fim = self.toolbar.entrada_hora_fim
        if hasattr(self.toolbar, 'entrada_intervalo'):
            globals.entrada_intervalo = self.toolbar.entrada_intervalo
        self.create_action_buttons()
        register_events(self)
        globals.main_window_instance = self
    
    def setup_window(self):
        """Setup main window properties"""
        self.window.title("Analisador de Produção")
        self.window.geometry("1800x1000")
        self.window.configure(bg='#f5f5f5')
        
        # Set default font
        fonte_padrao = font.nametofont("TkDefaultFont")
        fonte_padrao.configure(size=9)
    
    def create_layout(self):
        """Create main window layout"""
        # Create main frame
        self.frame_principal = tk.Frame(self.window, bg='#f5f5f5', relief='raised', bd=1)
        self.frame_principal.grid(row=0, column=0, columnspan=8, sticky="ew", padx=10, pady=5)
        
        # Campo de Média Geral acima da tabela
        self.frame_media_geral = tk.Frame(self.window, bg='#f5f5f5')
        self.frame_media_geral.grid(row=1, column=0, columnspan=8, sticky="ew", padx=10, pady=2)
        tk.Label(self.frame_media_geral, text="Média Geral:", bg='#f5f5f5', font=('Arial', 10, 'bold')).pack(side="left", padx=(10,2))
        self.entrada_media_geral = tk.Entry(self.frame_media_geral, width=15, font=('Arial', 10))
        self.entrada_media_geral.pack(side="left")
        # Botão aplicar média geral
        btn_aplicar_media = tk.Button(self.frame_media_geral, text="Aplicar Média Geral", command=self.aplicar_media_geral, bg='#2196F3', fg='white', font=('Arial', 9, 'bold'))
        btn_aplicar_media.pack(side="left", padx=5)
        # Armazena referência global
        globals.entrada_media_geral = self.entrada_media_geral
        
        # Create toolbar with input fields
        self.toolbar = create_toolbar(self.frame_principal)
        
        # PanedWindow para permitir redimensionamento estilo VS Code
        self.painel = tk.PanedWindow(self.window, orient=tk.VERTICAL, 
                                   sashwidth=8, sashrelief="groove", 
                                   sashpad=2, bg='#e0e0e0')
        self.painel.grid(row=3, column=0, columnspan=8, sticky="nsew", padx=10, pady=5)
        self.painel.configure(showhandle=True, handlesize=16)
        
        # Configure grid weights
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
    
    def initialize_components(self):
        """Initialize main components"""
        # Create table view
        from src.interface.components.table import TableComponent
        self.table_component = TableComponent(self.painel)
        self.table_frame = self.table_component.frame
        self.table = self.table_component.table
        self.painel.add(self.table_frame, height=600, minsize=200)
        globals.tabela = self.table
        globals.table_component = self.table_component

        # Terminal VS Code style
        self.terminal_frame, self.terminal = create_terminal_panel(self.painel)
        self.painel.add(self.terminal_frame, height=200, minsize=50)
        globals.text_resultado = self.terminal  # garantir referência global

        # Add initial feedback
        if self.terminal:
            self.terminal.insert(tk.END, "🎯 Dica: Dê duplo clique em qualquer célula para editá-la!\n")
            self.terminal.insert(tk.END, "🖱️ Clique com botão direito para mais opções de edição.\n\n")
        
        self.table.bind("<Double-1>", lambda event: editar_celula(event, globals.tabela))

    def calcular_desempenho_wrapper(self):
        from src.interface.handlers.table_handler import atualizar_dataframe_global
        atualizar_dataframe_global()
        from src.core.metrics.calculator import calcular_desempenho
        from src.core.config.setup_config import TEMPOS_SETUP
        config = TEMPOS_SETUP.copy()
        config['hora_inicio'] = globals.entrada_hora_inicio.get() if globals.entrada_hora_inicio else ''
        config['hora_fim'] = globals.entrada_hora_fim.get() if globals.entrada_hora_fim else ''
        config['intervalo'] = globals.entrada_intervalo.get() if globals.entrada_intervalo else '60'
        config['linhas_agrupadas'] = globals.linhas_agrupadas
        # Adiciona máquina selecionada
        config['maquina'] = globals.entrada_maquina.get() if globals.entrada_maquina else ''
        calcular_desempenho(
            globals.df_global,
            globals.text_resultado,
            config
        )
    
    def create_action_buttons(self):
        """Adiciona frame de botões de agrupamento e edição de tabela"""
        from ..handlers.group_handler import agrupar_selecionadas_melhorado, desagrupar_selecionadas_melhorado
        from src.interface.handlers.table_handler import inserir_linha, deletar_linha, exportar_dados

        frame_botoes = tk.Frame(self.window, bg='#f5f5f5')
        frame_botoes.grid(row=2, column=0, columnspan=8, sticky="ew", padx=10, pady=5)

        frame_agrupamento = tk.LabelFrame(frame_botoes, text="🔗 Agrupamento", bg='#f5f5f5')
        frame_agrupamento.pack(side="left", fill="y")
        tk.Button(frame_agrupamento, text="🔗 Agrupar", command=agrupar_selecionadas_melhorado).pack(side="left", padx=2)
        tk.Button(frame_agrupamento, text="🔓 Desagrupar", command=desagrupar_selecionadas_melhorado).pack(side="left", padx=2)
        tk.Button(frame_agrupamento, text="📈 Calcular Desempenho", command=self.calcular_desempenho_wrapper).pack(side="left", padx=5)

        frame_edicao = tk.LabelFrame(frame_botoes, text="📝 Edição da Tabela", bg='#f5f5f5')
        frame_edicao.pack(side="left", padx=10, fill="y")
        tk.Button(frame_edicao, text="➕ Nova Linha", command=lambda: inserir_linha(globals.tabela), bg='#4CAF50', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
        tk.Button(frame_edicao, text="🗑️ Deletar", command=lambda: deletar_linha(globals.tabela), bg='#F44336', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
        tk.Button(frame_edicao, text="📤 Exportar Dados", command=lambda: exportar_dados(globals.tabela), bg='#FF9800', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
        tk.Button(frame_edicao, text="📑 Exportar Análise", command=self.exportar_analise, bg='#9C27B0', fg='white', font=('Arial', 8)).pack(side="left", padx=2)
    
    def exportar_analise(self):
        """Exporta o conteúdo do widget text_resultado para um arquivo .txt ou PDF"""
        # Verifica se há conteúdo para exportar
        if not hasattr(globals, 'text_resultado') or globals.text_resultado is None:
            messagebox.showwarning("Aviso", "Terminal de análise não encontrado.")
            return
        
        try:
            conteudo = globals.text_resultado.get("1.0", "end-1c")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter conteúdo do terminal: {e}")
            return
        
        if not conteudo.strip():
            messagebox.showwarning("Aviso", "Não há análise para exportar.")
            return
        
        # Abre diálogo para salvar com opções de formato
        arquivo = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[
                ("Arquivo de Texto", "*.txt"), 
                ("PDF", "*.pdf"), 
                ("Todos Arquivos", "*.*")
            ],
            initialfile='analise.txt'
        )
        
        if not arquivo:
            return
        
        # Determina o formato baseado na extensão escolhida
        if arquivo.lower().endswith('.pdf'):
            formato = 'pdf'
        else:
            formato = 'txt'
            # Garante extensão .txt se não for PDF
            if not arquivo.lower().endswith('.txt'):
                arquivo = arquivo.rsplit('.', 1)[0] + '.txt'
        
        try:
            if formato == 'pdf':
                self._exportar_como_pdf(arquivo, conteudo)
            else:
                self._exportar_como_txt(arquivo, conteudo)
            
            messagebox.showinfo("Sucesso", f"Análise exportada para {arquivo}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar análise: {str(e)}")
            print(f"Erro detalhado na exportação: {e}")
    
    def _exportar_como_pdf(self, arquivo, conteudo):
        """Exporta conteúdo como PDF - versão otimizada para executável"""
        try:
            # Suprime warnings da fpdf
            warnings.filterwarnings("ignore", category=UserWarning, module="fpdf")
            
            # Cria o PDF
            pdf = FPDF()
            pdf.add_page()
            
            # Tenta usar fonte DejaVu se disponível, senão usa Arial
            try:
                # Determina caminho da fonte
                if getattr(sys, 'frozen', False):
                    # Executável PyInstaller
                    base_path = Path(sys._MEIPASS)
                else:
                    # Script Python
                    base_path = Path(__file__).parent.parent.parent.parent
                
                font_path = base_path / 'DejaVuSans.ttf'
                
                if font_path.exists():
                    pdf.add_font('DejaVu', '', str(font_path))
                    pdf.set_font('DejaVu', '', 10)
                    use_dejavu = True
                else:
                    pdf.set_font('Arial', '', 10)
                    use_dejavu = False
            except Exception as font_error:
                print(f"Aviso: Erro ao carregar fonte DejaVu: {font_error}")
                pdf.set_font('Arial', '', 10)
                use_dejavu = False
            
            # Limpa o conteúdo removendo caracteres especiais
            conteudo_limpo = self._limpar_caracteres_especiais(conteudo)
            
            # Processa o conteúdo linha por linha
            linhas = conteudo_limpo.split('\n')
            
            # Adiciona título
            if use_dejavu:
                pdf.set_font('DejaVu', 'B', 14)
            else:
                pdf.set_font('Arial', 'B', 14)
            pdf.cell(0, 10, 'Análise de Produção', ln=True, align='C')
            pdf.ln(5)
            
            # Volta para fonte normal
            if use_dejavu:
                pdf.set_font('DejaVu', '', 10)
            else:
                pdf.set_font('Arial', '', 10)
            
            # Processa cada linha
            for linha in linhas:
                try:
                    # Verifica se ainda há espaço na página
                    if pdf.get_y() > 270:  # Próximo da margem inferior
                        pdf.add_page()
                    
                    # Processa a linha
                    linha_str = str(linha).strip()
                    
                    # Se a linha estiver vazia, adiciona uma quebra de linha
                    if not linha_str:
                        pdf.ln(4)
                        continue
                    
                    # Quebra linhas muito longas
                    if len(linha_str) > 80:
                        # Usa multi_cell para quebrar automaticamente
                        pdf.multi_cell(0, 6, linha_str)
                    else:
                        # Usa cell para linhas normais
                        pdf.cell(0, 6, linha_str, ln=True)
                        
                except Exception as e:
                    print(f"Erro ao processar linha: {e}")
                    # Continua com próxima linha
                    continue
            
            # Salva o PDF
            pdf.output(arquivo)
            
        except Exception as e:
            raise Exception(f"Erro na geração do PDF: {str(e)}")
    
    def _exportar_como_txt(self, arquivo, conteudo):
        """Exporta conteúdo como TXT"""
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(conteudo)
        except Exception as e:
            raise Exception(f"Erro ao salvar arquivo TXT: {str(e)}")
    
    def _limpar_caracteres_especiais(self, texto):
        """Remove ou substitui caracteres especiais que podem causar problemas no PDF"""
        # Dicionário de substituições para emojis comuns
        substituicoes = {
            '🎯': '-> ',
            '🖱️': '-> ',
            '📊': '[GRAFICO] ',
            '⚡': '[RAPIDO] ',
            '🔧': '[CONFIG] ',
            '📈': '[CRESCIMENTO] ',
            '⏰': '[TEMPO] ',
            '🏭': '[FABRICA] ',
            '🔗': '[LINK] ',
            '🔓': '[DESBLOQUEADO] ',
            '📝': '[EDICAO] ',
            '➕': '+ ',
            '🗑️': '- ',
            '📤': '[EXPORTAR] ',
            '📑': '[RELATORIO] ',
            '✅': '[OK] ',
            '❌': '[ERRO] ',
            '⭐': '* ',
            '🚀': '[LANCAMENTO] ',
            '💡': '[IDEIA] ',
            '🎨': '[DESIGN] ',
            '🔍': '[BUSCA] ',
            '📋': '[LISTA] ',
            '⚙️': '[CONFIGURACAO] ',
            '🎪': '[EVENTO] ',
            '📦': '[PACOTE] ',
            '🔄': '[ATUALIZAR] ',
            '📅': '[DATA] ',
            '🕐': '[HORA] ',
            '📌': '[FIXAR] ',
            '🎵': '[MUSICA] ',
            '🎶': '[SOM] ',
            '🎼': '[PARTITURA] ',
            '🎹': '[PIANO] ',
            '🎺': '[TROMPETE] ',
            '🎻': '[VIOLINO] ',
            '🎸': '[GUITARRA] ',
            '🥁': '[BATERIA] ',
            '🎷': '[SAXOFONE] '
        }
        
        # Aplica as substituições
        for emoji, substituto in substituicoes.items():
            texto = texto.replace(emoji, substituto)
        
        # Remove outros caracteres que podem causar problemas
        # Mantém apenas caracteres ASCII imprimíveis e alguns especiais
        texto_limpo = ""
        for char in texto:
            if ord(char) < 32:  # Caracteres de controle
                if char in ['\n', '\r', '\t']:  # Mantém quebras de linha e tabs
                    texto_limpo += char
                else:
                    texto_limpo += ' '  # Substitui outros por espaço
            elif ord(char) <= 126:  # Caracteres ASCII imprimíveis
                texto_limpo += char
            elif ord(char) >= 160 and ord(char) <= 255:  # Caracteres latinos estendidos
                texto_limpo += char
            else:  # Outros caracteres especiais
                texto_limpo += ' '
        
        return texto_limpo
    
    def aplicar_media_geral(self):
        """Atualiza apenas as linhas de produção na coluna 'Média Produção' com o valor digitado na média geral."""
        valor = self.entrada_media_geral.get().strip()
        if not valor:
            return
        
        # Garante o sufixo 'p/h'
        if 'p/h' not in valor:
            valor = valor + ' p/h'
        
        # Atualiza DataFrame global
        import pandas as pd
        if hasattr(globals, 'df_global') and isinstance(globals.df_global, pd.DataFrame):
            if 'Média Produção' in globals.df_global.columns and 'Evento' in globals.df_global.columns:
                mask = globals.df_global['Evento'].str.lower().str.contains('produção', na=False)
                globals.df_global.loc[mask, 'Média Produção'] = valor
        
        # Atualiza visual da tabela
        tabela = globals.tabela
        if tabela is not None:
            try:
                colunas = list(tabela['columns'])
                if 'Média Produção' in colunas and 'Evento' in colunas:
                    idx_media = colunas.index('Média Produção')
                    idx_evento = colunas.index('Evento')
                    
                    for item in tabela.get_children():
                        valores = list(tabela.item(item)['values'])
                        if len(valores) > max(idx_media, idx_evento):
                            evento = str(valores[idx_evento]).lower()
                            if 'produção' in evento:
                                valores[idx_media] = valor
                                tabela.item(item, values=valores)
            except Exception as e:
                print(f"Erro ao aplicar média geral: {e}")
    
    def run(self):
        """Start the application"""
        self.window.mainloop()