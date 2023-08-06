#coding:gbk

import os

def new_user():
    true = os.path.exists('user.txt')
    if true == True:
        print("user.txt文件存在!")
    else:
        with open('user.txt', 'w', encoding="gbk") as i:
            i.write('USER_NAME=""')
            i.close()
        with open('user.txt', 'a', encoding="gbk") as g:
            g.write('\nKEY=""')
            g.close()
        with open('user.txt', 'a', encoding="gbk") as gp:
            gp.write('\nAGE=""')
            gp.close()
