# 🚀 Instruções para Gerar e Usar o Executável

## 📋 Checklist Completo

### ✅ Pré-requisitos
- [ ] Python 3.8+ instalado
- [ ] Todos os arquivos do projeto presentes
- [ ] Arquivo `DejaVuSans.ttf` na raiz do projeto
- [ ] Arquivo `icon.ico` na raiz do projeto

### 🔧 Passos para Gerar o Executável

#### Opção 1: Script Automatizado (Recomendado)
```bash
python build_executavel.py
```

#### Opção 2: Comando Manual
```bash
pyinstaller analisador.spec --clean
```

### 📁 Estrutura Após Build
```
dist/
├── AnalisadorProducao.exe    # ← Seu executável
├── DejaVuSans.ttf           # ← Fonte incluída
└── icon.ico                 # ← Ícone incluído
```

## 🎯 Como Criar o Atalho

1. **Abra a pasta `dist`**
2. **Clique com botão direito** em `AnalisadorProducao.exe`
3. **Selecione** "Enviar para > Área de trabalho (criar atalho)"
4. **Pronto!** O atalho estará na sua área de trabalho

## 🔍 Solução de Problemas

### ❌ Executável não abre / Trava / Pisca

#### 1. Teste pelo Terminal
```bash
cd dist
AnalisadorProducao.exe
```
- Se aparecer erro, você verá a mensagem exata

#### 2. Verifique Arquivos
- [ ] `DejaVuSans.ttf` está na pasta `dist`
- [ ] `icon.ico` está na pasta `dist`
- [ ] Não há arquivos faltando

#### 3. Problemas Comuns

**Erro: "Falta DLL"**
- Reinstale o Visual C++ Redistributable
- Baixe da Microsoft: https://aka.ms/vs/17/release/vc_redist.x64.exe

**Erro: "Falta fonte"**
- Verifique se `DejaVuSans.ttf` está na pasta `dist`
- O executável usa Arial como fallback

**Erro: "Módulo não encontrado"**
- Execute: `python build_executavel.py` novamente
- Isso regenera o executável com todos os módulos

### 🔧 Rebuild Completo
Se nada funcionar:
```bash
# 1. Limpe tudo
rmdir /s build dist
del *.spec

# 2. Regenere
python build_executavel.py
```

## 📊 Verificação de Funcionamento

### ✅ Testes Básicos
1. **Abre sem erro** ✅
2. **Interface aparece** ✅
3. **Pode inserir dados** ✅
4. **Pode exportar PDF** ✅
5. **Pode exportar TXT** ✅

### 🔍 Logs de Erro
Se houver problemas, verifique:
- `logs/analisador.log` (se existir)
- Mensagens no terminal (se executado via terminal)

## 🎨 Personalização

### Mudar Ícone
1. Substitua `icon.ico` por seu ícone
2. Regenere o executável: `python build_executavel.py`

### Mudar Nome
1. Edite `analisador.spec`
2. Mude `name='AnalisadorProducao'` para seu nome
3. Regenere o executável

## 📦 Distribuição

### Para Outros Computadores
1. **Copie toda a pasta `dist`**
2. **Cole em qualquer lugar**
3. **Crie atalho do executável**

### Requisitos do Sistema
- Windows 10/11
- Não precisa de Python instalado
- Não precisa de dependências

## 🆘 Suporte

### Se o Executável Não Funcionar
1. **Execute pelo terminal** para ver erros
2. **Verifique se todos os arquivos estão presentes**
3. **Tente rebuild completo**
4. **Teste em outro computador**

### Logs Úteis
- `logs/analisador.log` - Log da aplicação
- Terminal - Mensagens de erro detalhadas

---

## 🎉 Parabéns!

Se chegou até aqui, seu executável está pronto para uso! 

**Lembre-se:**
- ✅ Sempre teste antes de distribuir
- ✅ Mantenha backup do código fonte
- ✅ Use o script automatizado para rebuilds

**Comandos Úteis:**
```bash
# Gerar executável
python build_executavel.py

# Testar executável
cd dist && AnalisadorProducao.exe

# Limpar builds
rmdir /s build dist
``` 