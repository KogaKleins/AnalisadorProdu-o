#!/usr/bin/env python3
"""
Script para gerar executável do Analisador de Produção
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Verifica se todos os requisitos estão presentes"""
    print("🔍 Verificando requisitos...")
    
    # Verifica se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado")
    
    # Verifica arquivos necessários
    required_files = [
        "main.py",
        "DejaVuSans.ttf", 
        "icon.ico",
        "analisador.spec"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {missing_files}")
        return False
    
    print("✅ Todos os requisitos atendidos")
    return True

def clean_build_dirs():
    """Limpa diretórios de build anteriores"""
    print("🧹 Limpando builds anteriores...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✅ Removido: {dir_name}")
    
    # Remove arquivos .spec antigos (exceto o nosso)
    for spec_file in Path(".").glob("*.spec"):
        if spec_file.name != "analisador.spec":
            spec_file.unlink()
            print(f"✅ Removido: {spec_file.name}")

def build_executable():
    """Gera o executável"""
    print("🔨 Gerando executável...")
    
    try:
        # Usa o arquivo .spec otimizado
        result = subprocess.run([
            "pyinstaller", 
            "analisador.spec",
            "--clean"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executável gerado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao gerar executável:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro durante build: {e}")
        return False

def verify_executable():
    """Verifica se o executável foi criado corretamente"""
    print("🔍 Verificando executável...")
    
    exe_path = Path("dist/AnalisadorProducao.exe")
    if not exe_path.exists():
        print("❌ Executável não encontrado em dist/")
        return False
    
    print(f"✅ Executável encontrado: {exe_path}")
    print(f"📏 Tamanho: {exe_path.stat().st_size / (1024*1024):.1f} MB")
    
    # Verifica se os arquivos necessários estão na pasta dist
    dist_files = list(Path("dist").glob("*"))
    print(f"📁 Arquivos em dist/: {len(dist_files)}")
    
    return True

def create_shortcut_instructions():
    """Cria instruções para criar atalho"""
    print("\n" + "="*60)
    print("🎯 INSTRUÇÕES PARA CRIAR ATALHO:")
    print("="*60)
    print("1. Vá até a pasta 'dist'")
    print("2. Clique com botão direito em 'AnalisadorProducao.exe'")
    print("3. Selecione 'Enviar para > Área de trabalho (criar atalho)'")
    print("4. O atalho será criado na sua área de trabalho")
    print("="*60)

def main():
    """Função principal"""
    print("🚀 Iniciando build do Analisador de Produção")
    print("="*50)
    
    # Verifica requisitos
    if not check_requirements():
        print("❌ Falha na verificação de requisitos")
        return False
    
    # Limpa builds anteriores
    clean_build_dirs()
    
    # Gera executável
    if not build_executable():
        print("❌ Falha na geração do executável")
        return False
    
    # Verifica resultado
    if not verify_executable():
        print("❌ Falha na verificação do executável")
        return False
    
    # Mostra instruções
    create_shortcut_instructions()
    
    print("\n🎉 Build concluído com sucesso!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 