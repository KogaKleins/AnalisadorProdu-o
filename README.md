# Analisador de Produção

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Sistema para análise de dados de produção industrial com geração de relatórios de desempenho.

---

![Screenshot da Interface](docs/screenshot_interface.png)

## Descrição
Sistema desenvolvido para analisar dados de produção industrial, processando relatórios de máquinas e gerando análises detalhadas de desempenho, eficiência e produtividade.

## Principais Recursos
- Extração de dados de PDFs de relatórios de produção
- Interface gráfica intuitiva e moderna (Tkinter)
- Análise de eficiência de produção
- Geração de relatórios detalhados e visuais
- Agrupamento de dados por ordem de produção
- Cálculos de tempo de setup e produção
- **Campos de período de trabalho inteligentes:** aceitam tanto hora (`08:00`) quanto data+hora (`06/06/2025 06:00`), com formatação automática
- Exportação para CSV, Excel e PDF

## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd AnalisadorProducao
   ```
2. **Crie o ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   # Ative o ambiente:
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```
3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Execute o sistema:**
   ```bash
   python main.py
   ```

## Como Usar

- **Carregue os dados** informando a data e a máquina, depois clique em "Carregar Dados".
- **Período de Trabalho:**
  - Os campos de início e fim aceitam tanto hora (`08:00`) quanto data+hora (`06/06/2025 06:00`).
  - Você pode digitar apenas números e o campo será formatado automaticamente (ex: `060620250600` vira `06/06/2025 06:00`).
  - O campo é adaptável e largo para caber toda a informação.
- **Agrupe, desagrupe e edite linhas** usando os botões da interface.
- **Calcule o desempenho** e gere relatórios detalhados com um clique.
- **Exporte os dados** para CSV, Excel ou PDF.

## Estrutura Completa do Projeto

```
AnalisadorProducao/
│
├── ARVORE_PROJETO.md
├── DejaVuSans.cw127.pkl
├── DejaVuSans.pkl
├── DejaVuSans.ttf
├── README.md
├── main.py
├── analisador.log
├── requirements.txt
├── pyproject.toml
├── setup.py
├── icon.png
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __pycache__/
│   │   └── setup_config.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config/
│   │   │   ├── __pycache__/
│   │   │   └── setup_config.py
│   │   ├── data/
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── data_processor.py
│   │   │   └── group_manager.py
│   │   ├── extractor/
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── file_finder.py
│   │   │   └── pdf_extractor.py
│   │   ├── metrics/
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__/
│   │   │   ├── calculator.py
│   │   │   ├── utils.py
│   │   │   ├── maquinas/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── bobst.py
│   │   │   │   ├── cv_guangya.py
│   │   │   │   ├── cv_manual.py
│   │   │   │   ├── furnax.py
│   │   │   │   ├── hcd.py
│   │   │   │   ├── heidelberg.py
│   │   │   │   ├── komori.py
│   │   │   │   ├── laminadora.py
│   │   │   │   ├── sakurai.py
│   │   │   │   ├── samkoon.py
│   │   │   │   └── sbl.py
│   │   │   ├── report/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── generator.py
│   │   │   │   ├── calculator.py
│   │   │   │   ├── sections.py
│   │   │   │   ├── utils.py
│   │   │   │   └── sections/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── __pycache__/
│   │   │   │       ├── efficiency.py
│   │   │   │       ├── ops.py
│   │   │   │       ├── period.py
│   │   │   │       └── summary.py
│   │   │   │
│   │   │   ├── data/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── data_processor.py
│   │   │   │   └── group_manager.py
│   │   │   │
│   │   │   ├── extractor/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── file_finder.py
│   │   │   │   └── pdf_extractor.py
│   │   │   │
│   │   │   ├── metrics/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── __pycache__/
│   │   │   │   ├── calculator.py
│   │   │   │   ├── utils.py
│   │   │   │   ├── maquinas/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── bobst.py
│   │   │   │   │   ├── cv_guangya.py
│   │   │   │   │   ├── cv_manual.py
│   │   │   │   │   ├── furnax.py
│   │   │   │   │   ├── hcd.py
│   │   │   │   │   ├── heidelberg.py
│   │   │   │   │   ├── komori.py
│   │   │   │   │   ├── laminadora.py
│   │   │   │   │   ├── sakurai.py
│   │   │   │   │   ├── samkoon.py
│   │   │   │   │   └── sbl.py
│   │   │   │   │
│   │   │   │   ├── report/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── generator.py
│   │   │   │   │   ├── calculator.py
│   │   │   │   │   ├── sections.py
│   │   │   │   │   ├── utils.py
│   │   │   │   │   └── sections/
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── __pycache__/
│   │   │   │   │       ├── efficiency.py
│   │   │   │   │       ├── ops.py
│   │   │   │   │       ├── period.py
│   │   │   │   │       └── summary.py
│   │   │   │   │
│   │   │   │   ├── data/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── data_processor.py
│   │   │   │   │   └── group_manager.py
│   │   │   │   │
│   │   │   │   ├── extractor/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── file_finder.py
│   │   │   │   │   └── pdf_extractor.py
│   │   │   │   │
│   │   │   │   ├── metrics/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── __pycache__/
│   │   │   │   │   ├── calculator.py
│   │   │   │   │   ├── utils.py
│   │   │   │   │   ├── maquinas/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── __pycache__/
│   │   │   │   │   │   ├── bobst.py
│   │   │   │   │   │   ├── cv_guangya.py
│   │   │   │   │   │   ├── cv_manual.py
│   │   │   │   │   │   ├── furnax.py
│   │   │   │   │   │   ├── hcd.py
│   │   │   │   │   │   ├── heidelberg.py
│   │   │   │   │   │   ├── komori.py
│   │   │   │   │   │   ├── laminadora.py
│   │   │   │   │   │   ├── sakurai.py
│   │   │   │   │   │   ├── samkoon.py
│   │   │   │   │   │   └── sbl.py
│   │   │   │   │   │
│   │   │   │   │   ├── report/
│   │   │   │   │   │   ├── __init__.py
│   │   │   │   │   │   ├── __pycache__/
│   │   │   │   │   │   ├── generator.py
│   │   │   │   │   │   ├── calculator.py
│   │   │   │   │   │   ├── sections.py
│   │   │   │   │   │   ├── utils.py
│   │   │   │   │   │   └── sections/
│   │   │   │   │   │       ├── __init__.py
│   │   │   │   │   │       ├── __pycache__/
│   │   │   │   │   │       ├── efficiency.py
│   │   │   │   │   │       ├── ops.py
│   │   │   │   │   │       ├── period.py
│   │   │   │   │   │       └── summary.py
│   │   │   │   │   │
│   │   │   │   │   └── data/
│   │   │   │   │       ├── __init__.py
│   │   │   │   │       ├── __pycache__/
│   │   │   │   │       ├── data_processor.py
│   │   │   │   │       └── group_manager.py
│   │   │   │   │
│   │   │   │   └── interface/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── __pycache__/
│   │   │   │       ├── globals.py
│   │   │   │       ├── dialogs/
│   │   │   │       │   └── __init__.py
│   │   │   │       ├── utils/
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── __pycache__/
│   │   │   │       │   ├── formatters.py
│   │   │   │       │   ├── globals.py
│   │   │   │       │   └── header_generator.py
│   │   │   │       ├── handlers/
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── __pycache__/
│   │   │   │       │   ├── config_handler.py
│   │   │   │       │   ├── data_handler.py
│   │   │   │       │   ├── event_handler.py
│   │   │   │       │   ├── formatters.py
│   │   │   │       │   ├── group_handler.py
│   │   │   │       │   ├── table_handler.py
│   │   │   │       └── components/
│   │   │   │       │   ├── __init__.py
│   │   │   │       │   ├── __pycache__/
│   │   │   │       │   ├── main_window.py
│   │   │   │       │   ├── table.py
│   │   │   │       │   ├── terminal.py
│   │   │   │       │   └── toolbar.py
│   │   │   │       └── models/
│   │   │   │           └── __init__.py
│   │   │   └── services/
│   │   │       └── __init__.py
│   │   └── tests/
│   │       └── __init__.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── formatters.py
│   │   └── validators.py
│   └── docs/
│       └── ... (documentação, licenças etc)
│
├── tests/
│   └── __init__.py
│
├── RELATORIOS PRODUTIVIDADE/
│   └── pdf/
│       ├── abril/
│       │   └── 15/
│       │       └── bobst.pdf
│       ├── junho/
│       │   ├── 06/ ... 13/
│       │   └── ...
│       └── julho/
│           ├── 02/
│           └── 03/
│
├── dejavu-fonts-ttf-2.37/
│   ├── ttf/
│   │   ├── DejaVuSans.ttf
│   │   └── ... (outras fontes)
│   └── ... (documentação, licenças etc)
│
└── venv/
```

---

## Explicação Detalhada de Cada Pasta e Arquivo

### Raiz do Projeto

- **main.py**: Script principal para inicialização do sistema.
- **README.md**: Documentação principal do projeto.
- **requirements.txt**: Lista de dependências Python.
- **pyproject.toml / setup.py**: Configuração de build/instalação do projeto.
- **ARVORE_PROJETO.md**: (Opcional) Documento para árvore do projeto.
- **DejaVuSans.ttf**: Fonte Unicode usada para exportação de PDF.
- **icon.png**: Ícone do sistema.
- **analisador.log**: Log de execução do sistema.
- **.gitignore**: Arquivos/pastas ignorados pelo git.
- **venv/**: Ambiente virtual Python.
- **docs/**: Documentação adicional (vazia ou para uso futuro).
- **tests/**: Testes automatizados (estrutura inicial).
- **RELATORIOS PRODUTIVIDADE/**: Relatórios PDF de produção organizados por mês/dia/máquina.
- **dejavu-fonts-ttf-2.37/**: Pasta da fonte DejaVu completa (apenas DejaVuSans.ttf é usada pelo sistema).

---

### src/ (Código-fonte principal)

- **src/main.py**: Ponto de entrada do sistema (pode importar e rodar a interface principal).
- **src/__init__.py**: Marca o diretório como pacote Python.

#### src/config/
- **setup_config.py**: Configurações globais do sistema (ex: tempos padrão, parâmetros de máquinas).

#### src/core/
- **config/**: Configurações do núcleo.
- **data/**: Processamento e agrupamento de dados de produção.
  - **data_processor.py**: Funções para manipulação e limpeza de dados.
  - **group_manager.py**: Gerenciamento de agrupamentos de linhas/OPs.
- **extractor/**: Extração de dados de arquivos.
  - **file_finder.py**: Localização de arquivos PDF.
  - **pdf_extractor.py**: Extração de dados de PDFs.
- **metrics/**: Lógica de cálculo de métricas de produção.
  - **calculator.py**: Funções principais de cálculo de desempenho.
  - **utils.py**: Utilitários para métricas (formatação, parsing, etc).
  - **maquinas/**: Cálculo específico para cada máquina (bobst, komori, etc).
  - **report/**: Geração de relatórios de desempenho.
    - **generator.py**: Gera o texto do relatório.
    - **calculator.py**: Cálculo detalhado para relatórios.
    - **sections.py**: Organização das seções do relatório.
    - **utils.py**: Utilitários para relatórios.
    - **sections/**: Seções específicas do relatório (eficiência, operações, resumo, período).

#### src/interface/
- **globals.py**: Variáveis globais da interface.
- **dialogs/**: Diálogos customizados (estrutura inicial).
- **utils/**: Utilitários da interface (formatação, headers, etc).
- **handlers/**: Manipuladores de eventos, dados e lógica da interface.
  - **config_handler.py**: Manipulação de configurações.
  - **data_handler.py**: Manipulação de dados da tabela.
  - **event_handler.py**: Eventos da interface.
  - **formatters.py**: Funções de formatação.
  - **group_handler.py**: Agrupamento/desagrupamento de linhas.
  - **table_handler.py**: Lógica de manipulação da tabela (inserção, deleção, exportação, etc).
- **components/**: Componentes visuais da interface.
  - **main_window.py**: Janela principal do sistema (layout, botões, exportação, etc).
  - **table.py**: Componente visual da tabela (estilo planilha).
  - **toolbar.py**: Barra de ferramentas e filtros.
  - **terminal.py**: Terminal de mensagens/resultados.

#### src/data/, src/models/, src/services/, src/tests/, src/utils/
- **Estruturas para expansão futura**:
  - **data/**: Dados auxiliares.
  - **models/**: Modelos de dados (ex: classes para produção, OP, etc).
  - **services/**: Serviços auxiliares (ex: integração externa).
  - **tests/**: Testes automatizados.
  - **utils/**: Utilitários gerais (formatação, validação).

---

### RELATORIOS PRODUTIVIDADE/
- **pdf/**: Relatórios PDF reais, organizados por mês/dia/máquina.

---

### dejavu-fonts-ttf-2.37/
- **ttf/**: Vários arquivos de fonte DejaVu (apenas DejaVuSans.ttf é usada).
- **Outros arquivos**: Licença, documentação, status, etc.

---

Se quiser uma explicação ainda mais detalhada de algum arquivo ou pasta, ou um texto pronto para README, só pedir!

## Testes

- Para rodar os testes (se houver):
  ```bash
  pytest src/tests/
  ```

## Contribuindo

Contribuições são bem-vindas! Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature/correção
3. Envie um pull request
4. Descreva claramente sua alteração

## Créditos
- Desenvolvedor principal: [Wilmar]


---

> **Atualizado para aceitar datas e horas completas nos campos de período de trabalho, com formatação automática e campo adaptável.**

## Build do Executável (Windows)

Se você deseja gerar um executável para Windows:

1. Execute o script de build:
   ```bash
   python build_executavel.py
   ```
   O executável será criado em `dist/AnalisadorProducao.exe`.
2. Crie um atalho:
   - Clique com o botão direito em `AnalisadorProducao.exe` → Enviar para → Área de trabalho (criar atalho)
3. Pronto! Basta usar o atalho normalmente.

> Para instruções detalhadas, consulte o arquivo `INSTRUCOES_EXECUTAVEL.md`.

### Compatibilidade
- O executável gerado no Windows **não funciona no Linux**. Para rodar no Linux, use o código Python conforme instruções acima.
- O executável é portátil: basta copiar a pasta `dist` para outro Windows e criar o atalho.

## Dependências Principais (requirements.txt)
- `pandas`, `numpy`: manipulação de dados
- `pdfplumber`: extração de tabelas de PDFs
- `fpdf`: geração de PDF (exportação de análise)
- `unidecode`: normalização de textos para busca e comparação
- `tkinter`: interface gráfica (já incluso no Python padrão)
- Outras: `python-dateutil`, `pytz`, `tzdata`, `charset-normalizer`

> **Nota:** Dependências como `tkinter`, `logging`, `pathlib`, `subprocess` já fazem parte da biblioteca padrão do Python e não precisam ser instaladas via pip.

- **build_executavel.py**: Script automatizado para gerar o executável Windows.
- **analisador.spec**: Arquivo de configuração do PyInstaller para build do executável.
- **INSTRUCOES_EXECUTAVEL.md**: Instruções detalhadas para build, distribuição e solução de problemas do executável.
- **icon.ico**: Ícone personalizado do executável.
