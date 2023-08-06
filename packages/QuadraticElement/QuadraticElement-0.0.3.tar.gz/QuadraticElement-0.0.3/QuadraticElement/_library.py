import os

'''
try与except检测第三方库是否安装
libs加上for循环安装

'''

def pip_library():
    libs = ['numpy', 'wget', 'request', 'opencv-python', 'RandomKey', 'PyPoli', 'FolderProcessing']#安装列表中名字的第三方库

    url = r'https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/'#清华镜像源
    try:
        import wget
        import os
        import os.path
        import cv2
        import numpy as np
        from RandomKey import key
        from PyPoli import Hello
        from FolderProcessing import seefile
        print('Input library successful')
    except ModuleNotFoundError:
            print('Failed SomeHow')
            for lib in libs:
                print("Start install {0}".format(lib))
                os.system('pip install -U %s -i %s'%(lib,url))
                print('{0} install successful'.format(lib))
            print('All install successful ')
            print("请重启！")
            import numpy as np
