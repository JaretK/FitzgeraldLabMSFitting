# -*- mode: python -*-
a = Analysis(['__main__.py'],
             pathex=['/Volumes/Macintosh HD/Code/Eclipse workspace/CurveFitting'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='__main__',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='__main__')
app = BUNDLE(coll,
             name='__main__.app',
             icon=None)
