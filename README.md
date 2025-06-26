# Analisador de Produção

Sistema para análise de dados de produção industrial com geração de relatórios de desempenho.

## Descrição
Sistema desenvolvido para analisar dados de produção industrial, processando relatórios de máquinas e gerando análises detalhadas de desempenho, eficiência e produtividade.

## Recursos
- Extração de dados de PDFs de relatórios de produção
- Interface gráfica intuitiva
- Análise de eficiência de produção
- Geração de relatórios detalhados
- Agrupamento de dados por ordem de produção
- Cálculos de tempo de setup e produção

## Estrutura Completa do Projeto

```
ARVORE_PROJETO.md
README.md
analisador.log
DejaVuSans.ttf
main.py
pyproject.toml
requirements.txt
setup.py
config/
    setup_config.py
    __pycache__/
        setup_config.cpython-313.pyc
data/
    data_handler.py
    group_manager.py
    performance_calculator.py
    __pycache__/
        data_handler.cpython-313.pyc
        group_manager.cpython-313.pyc
        performance_calculator.cpython-313.pyc
    metrics/
        agrupamento.py
        __init__.py
        relatorio.py
        utils.py
        __pycache__/
            agrupamento.cpython-313.pyc
            relatorio.cpython-313.pyc
            utils.cpython-313.pyc
docs/
extrator/
    __init__.py
    caminhos.py
    extrator_pdf.py
    __pycache__/
        __init__.cpython-313.pyc
        caminhos.cpython-313.pyc
        extrator_pdf.cpython-313.pyc
interface/
    __init__.py
    formatters.py
    globals.py
    table_manager.py
    terminal_panel.py
    ui_setup.py
    visual_layout.py
    __pycache__/
        __init__.cpython-313.pyc
        formatters.cpython-313.pyc
        globals.cpython-313.pyc
        janela_principal.cpython-313.pyc
        table_manager.cpython-313.pyc
        terminal_panel.cpython-313.pyc
        ui_setup.cpython-313.pyc
        visual_layout.cpython-313.pyc
RELATORIOS PRODUTIVIDADE/
    pdf/
        abril/
            15/
        junho/
            06/
            09/
            10/
            11/
            12/
            13/
src/
    __init__.py
    __pycache__/
        __init__.cpython-313.pyc
    core/
        __init__.py
        __pycache__/
            __init__.cpython-313.pyc
        config/
            setup_config.py
            __pycache__/
        data/
            __init__.py
            data_processor.py
            group_manager.py
            __pycache__/
        extractor/
            __init__.py
            file_finder.py
            pdf_extractor.py
            __pycache__/
        metrics/
            calculator.py
            __pycache__/
            maquinas/
            report/
    interface/
        __init__.py
        globals.py
        __pycache__/
            __init__.cpython-313.pyc
            globals.cpython-313.pyc
        components/
            __init__.py
            main_window.py
            table.py
            terminal.py
            toolbar.py
            __pycache__/
        handlers/
            __init__.py
            config_handler.py
            data_handler.py
            event_handler.py
            formatters.py
            group_handler.py
            table_handler.py
            __pycache__/
        utils/
    utils/
        __init__.py
        formatters.py
        validators.py
tests/
```

## Interface Gráfica

A interface principal é montada em `interface/ui_setup.py` e `interface/table_manager.py`.

### Botões e Ações
Os botões principais ficam em um frame logo abaixo do período de trabalho:

- **🔗 Agrupar**: Agrupa as linhas selecionadas
- **🔓 Desagrupar**: Desagrupa as linhas selecionadas
- **📈 Calcular Desempenho**: Calcula os indicadores de produtividade
- **➕ Nova Linha**: Insere uma nova linha na tabela
- **🗑️ Deletar**: Deleta a(s) linha(s) selecionada(s)
- **💾 Salvar**: Salva as alterações feitas na tabela
- **📤 Exportar**: Exporta os dados editados para CSV/Excel

### Organização dos Handlers
- **Agrupamento/Desagrupamento**: `data/group_manager.py`
- **Edição/Exportação de tabela**: `interface/table_manager.py`
- **Cálculo de desempenho**: `data/performance_calculator.py` e `data/metrics/relatorio.py`
- **Configuração de setup**: `config/setup_config.py`

---

> **Nota:** Esta árvore reflete a estrutura real do workspace e serve como referência única e centralizada para desenvolvedores e usuários do projeto.
