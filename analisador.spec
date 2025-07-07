# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Determina o caminho base
import os
base_path = Path(os.getcwd())

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[str(base_path), str(base_path / 'src')],
    binaries=[],
    datas=[
        ('DejaVuSans.ttf', '.'),
        ('icon.ico', '.'),
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.font',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'pandas',
        'numpy',
        'fpdf',
        'pathlib',
        'logging',
        'traceback',
        'platform',
        'subprocess',
        'warnings',
        'src.interface',
        'src.interface.components',
        'src.interface.handlers',
        'src.interface.utils',
        'src.core',
        'src.core.config',
        'src.core.data',
        'src.core.extractor',
        'src.core.metrics',
        'src.core.metrics.maquinas',
        'src.core.metrics.report',
        'src.core.metrics.report.sections',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'PIL',
        'cv2',
        'tensorflow',
        'torch',
        'jupyter',
        'notebook',
        'ipython',
        'spyder',
        'pytest',
        'unittest',
        'doctest',
        'test',
        'tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnalisadorProducao',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False para aplicação GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version_file=None,
) 