#coding:gbk

import os

def New():
    true = os.path.exists('user.txt')
    if true == True:
        pass
    else:
        print("识别到当前位置未发现“user.txt”文件，将自动生成....")
        with open('user.txt', 'w', encoding="gbk") as i:
            i.write('USER_NAME=""')
            i.close()
        with open('user.txt', 'a', encoding="gbk") as g:
            g.write('\nKEY=""')
            g.close()
        with open('user.txt', 'a', encoding="gbk") as gp:
            gp.write('\nAGE=""')
            gp.close()

def USERNAME():
    with open("user.txt", 'r', encoding="gbk") as f:
        name = f.readline()
        print(f"@User-Name:{name}")
        key = f.readline()
        print(f"@User-Key:{key}")
        
New()
