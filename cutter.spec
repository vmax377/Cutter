# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(
    ['ui\\finestra_principal.py'],
    pathex=['C:\\CutterPython'],
    binaries=[],
    datas=[('C:\\CutterPython\\logo.png', '.')],
    hiddenimports=[
        'openpyxl',
        'PyQt5.QtPrintSupport',
        'dades.perfils',
        'dades.descomptes_vidre',
        'logica.calculs',
        'logica.funcions',
        'logica.gestor_dades',
        'logica.impressio',
        'logica.esquema',
        'ui.finestra_peca_solta',
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

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Cutter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='C:\\CutterPython\\icona.ico',
)