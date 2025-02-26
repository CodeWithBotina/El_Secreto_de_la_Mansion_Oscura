# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import site
from PyInstaller.utils.hooks import collect_dynamic_libs

block_cipher = None

# Definir rutas absolutas
PROJ_PATH = os.path.abspath(os.path.dirname('__file__'))
DIST_PATH = os.path.join(PROJ_PATH, 'dist', 'El_Secreto_de_la_Mansion_Oscura')
BUILD_PATH = os.path.join(PROJ_PATH, 'build')

# Crear directorios necesarios
os.makedirs(DIST_PATH, exist_ok=True)
os.makedirs(BUILD_PATH, exist_ok=True)

# Intentar encontrar Z3
try:
    import z3
    z3_path = os.path.dirname(z3.__file__)
    z3_binaries = collect_dynamic_libs('z3')
    print(f"Z3 found at: {z3_path}")
    print(f"Z3 binaries: {z3_binaries}")
except ImportError:
    print("Warning: Z3 not found")
    z3_binaries = []

# Definir archivos a incluir
added_files = [
    ('assets/images/*.png', 'assets/images'),
    ('assets/images/*.ico', 'assets/images'),
    ('assets/sounds/*.mp3', 'assets/sounds'),
    ('src/game/*.py', 'src/game'),
    ('src/ui/*.py', 'src/ui'),
    ('src/utils/*.py', 'src/utils'),
]

a = Analysis(
    ['main.py'],
    pathex=[PROJ_PATH],
    binaries=z3_binaries,
    datas=added_files,
    hiddenimports=[
        'z3',
        'z3.z3core',
        'z3.z3types',
        'pygame',
        'numpy',
        'json',
        'random',
        'time',
        'sys',
        'os'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Crear el ejecutable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # Importante: excluir binarios del EXE
    name='El_Secreto_de_la_Mansion_Oscura',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/images/icono.ico',
)

# Crear el paquete completo
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='El_Secreto_de_la_Mansion_Oscura',
)

# Imprimir información de las rutas
print(f"Project Path: {PROJ_PATH}")
print(f"Distribution Path: {DIST_PATH}")
print(f"Build Path: {BUILD_PATH}")
print("\nEl ejecutable y sus recursos se encontrarán en:")
print(f"{os.path.join(DIST_PATH, 'El_Secreto_de_la_Mansion_Oscura')}")