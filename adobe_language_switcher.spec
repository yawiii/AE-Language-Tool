# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['adobe_language_switcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'asyncio', 'concurrent', 'ctypes.macholib', 'distutils',
        'lib2to3', 'multiprocessing', 'pydoc_data', 'test', 'unittest',
        'xml.dom', 'xml.sax', 'xmlrpc', 'email', 'html', 'http',
        'logging', 'pkg_resources', 'setuptools', 'tty', 'typing',
        'wcwidth', 'webbrowser'
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='adobe_language_switcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
