# -*- mode: python ; coding: utf-8 -*-
# Build: pip install pyinstaller pillow fonttools python-docx && pyinstaller InkRanker.spec

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src/sample.txt', '.'),
        ('src/fonts.txt', '.'),
        ('src/icon.png', '.'),
    ],
    hiddenimports=[
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'numpy', 'scipy', 'pandas', 'matplotlib',
        '_ssl', 'ssl', 'email', 'unittest', 'pdb', 'pydoc',
        'xmlrpc', 'http.server', 'multiprocessing', 'sqlite3',
        'asyncio', 'curses', 'distutils', 'test',
        'pkg_resources', 'setuptools', 'wheel',
        'PIL.ImageQt', 'PIL.ImageTk',
        'tkinter.tix', 'lib2to3',
        'fontTools.feaLib', 'fontTools.designspaceLib',
        'fontTools.varLib', 'fontTools.colorLib',
        'fontTools.svgLib', 'fontTools.t1Lib',
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
    name='InkRanker',
    icon='src/icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Disabled for faster startup
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
