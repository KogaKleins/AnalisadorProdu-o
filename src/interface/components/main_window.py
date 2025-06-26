"""
Main window component module.
Contains the main application window setup and layout.
"""

import tkinter as tk
from tkinter import ttk, font
import sys
import platform
sys.path.append('.')
from src.interface import globals
from fpdf import FPDF

from ..components.toolbar import create_toolbar
from ..components.table import create_table_view
from ..components.terminal import create_terminal_panel
from ..handlers.event_handler import register_events
from ..handlers.table_handler import editar_celula, inserir_linha, deletar_linha, aplicar_cores_grupos, editar_celula, configurar_colunas_da_tabela

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
        # Remover text_resultado duplicado
        # self.text_resultado = tk.Text(self.window, height=5, bg='#f5f5f5', font=('Consolas', 10))
        # self.text_resultado.grid(row=5, column=0, columnspan=8, sticky="ew", padx=10, pady=5)
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
        self.table_frame, self.table = create_table_view(self.painel)
        self.painel.add(self.table_frame, height=600, minsize=200)
        globals.tabela = self.table  # <-- garantir referência global

        # Terminal VS Code style
        self.terminal_frame, self.terminal = create_terminal_panel(self.painel)
        self.painel.add(self.terminal_frame, height=200, minsize=50)
        globals.text_resultado = self.terminal  # garantir referência global

        # Add initial feedback
        if self.terminal:
            self.terminal.insert(tk.END, "🎯 Dica: Dê duplo clique em qualquer célula para editá-la!\n")
            self.terminal.insert(tk.END, "🖱️ Clique com botão direito para mais opções de edição.\n\n")
        
        self.table.bind("<Double-1>", lambda event: editar_celula(event, globals.tabela))
        # Remover chamada para self.add_edit_buttons() para evitar botões duplicados

    def add_edit_buttons(self):
        pass  # Remove implementação para evitar botões duplicados
    
    def calcular_desempenho_wrapper(self):
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
        from tkinter import filedialog, messagebox
        conteudo = globals.text_resultado.get("1.0", "end-1c")
        if not conteudo.strip():
            messagebox.showwarning("Aviso", "Não há análise para exportar.")
            return
        # Dialogo com tipos
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt"), ("PDF", "*.pdf"), ("Todos Arquivos", "*.*")]
        )
        if not arquivo:
            return
        # Força extensão conforme filtro
        if arquivo.lower().endswith('.pdf') or arquivo.lower().endswith('.txt'):
            ext = arquivo.lower().split('.')[-1]
        else:
            # Se não digitou extensão, tenta inferir pelo filtro
            if arquivo.endswith('.'):
                arquivo = arquivo[:-1]
            # Pergunta ao usuário
            tipo = messagebox.askquestion("Formato", "Exportar como PDF? (Sim para PDF, Não para TXT)")
            if tipo == 'yes':
                arquivo += '.pdf'
                ext = 'pdf'
            else:
                arquivo += '.txt'
                ext = 'txt'
        try:
            if ext == 'pdf':
                try:
                    from fpdf import FPDF
                except ImportError:
                    messagebox.showerror("Erro", "Biblioteca fpdf2 não instalada no ambiente Python!")
                    return
                pdf = FPDF()
                pdf.add_page()
                # Usa fonte Unicode
                try:
                    pdf.add_font('DejaVu', '', './DejaVuSans.ttf', uni=True)
                    pdf.set_font('DejaVu', '', 10)
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao carregar fonte Unicode: {e}")
                    return
                for linha in conteudo.splitlines():
                    pdf.multi_cell(0, 8, linha)
                pdf.output(arquivo)
            else:
                with open(arquivo, "w", encoding="utf-8") as f:
                    f.write(conteudo)
            messagebox.showinfo("Sucesso", f"Análise exportada para {arquivo}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar análise: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.window.mainloop()
