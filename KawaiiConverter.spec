# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['kawaii_converter.py'],
    pathex=[],
    binaries=[],
    datas=[('requirements.txt', '.')],
    hiddenimports=['pandas', 'pandas.plotting', 'pandas.core.algorithms', 'pandas.core.arrays', 'pandas.core.computation.expressions', 'pandas.core.indexes.numeric', 'pandas.core.dtypes.common', 'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'scipy', 'numpy.random._examples'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KawaiiConverter',
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
    icon=['jelly.ico'],
)
