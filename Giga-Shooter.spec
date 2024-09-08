# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['shooter_game.py'],
    pathex=[],
    binaries=[],
    datas=[('galaxy.jpg', '.'), ('rocket.png', '.'), ('bullet.png', '.'), ('ufo.png', '.'), ('space.ogg', '.'), ('fire.ogg', '.'), ('asteroid.png', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Giga-Shooter',
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
)
