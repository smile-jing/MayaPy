import maya.cmds as cmds
cmds.file(force=True, new=True)
cmds.polySphere()
cmds.file(rename=r'D:\{file_name}.ma')
cmds.file(force=True, type='mayaAscii', save=True)
print('MAYA LOG ------ Welcome To http://td.cineuse.com')