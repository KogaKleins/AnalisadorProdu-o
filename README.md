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

## Estrutura do Projeto (resumida)

```
AnalisadorProducao/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── core/
│   │   ├── config/
│   │   ├── data/
│   │   ├── extractor/
│   │   └── metrics/
│   └── interface/
│       ├── components/
│       ├── handlers/
│       └── utils/
├── RELATORIOS PRODUTIVIDADE/
│   └── pdf/
└── ...
```

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
