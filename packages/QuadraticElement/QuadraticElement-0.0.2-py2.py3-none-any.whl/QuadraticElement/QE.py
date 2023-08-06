# coding:gbk
"""
OS:Windows 10 רҵ��
Python version:3.9.7
Time:2021/9/xx
author:PYmili
"""

import wget
import os
import os.path
import cv2
import numpy as np
from urllib import request

from QuadraticElement import _library
from QuadraticElement import user_message as um
from QuadraticElement import new_user as new
from QuadraticElement import _open as op

from FolderProcessing import seefile as see

# Poli
def run_Poli():
    from PyPoli import Poli


# ys
def img_ys(path):  # �ʵ�01
    img = cv2.imread(path, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
|library
�����������Ƿ�װ
"""
_library.pip_library()  # �����Ҫ�ĵ��������Ƿ�װ
os.system("color 2")  # ��������������ɫ
# ����ѭ��������
while True:
    _user = input("\n@QuadraticElement#>")  # user����
    '''
    |user_message
    �û���Ϣ��ѯ
    '''
    help_user_message = "$�û���Ϣ|User information"  # help
    if _user == "user_message":
        print("\n")
        um.USERNAME()
        continue

    """
    |wget
    ��ҳ���ع���
    """
    help_dow = "$��������|Download command"  # help
    if _user == 'download' or _user == 'dow':
        try:
            url = input("URL>")
            file = input("FILE>")
            wget.download(url, out=f"{file}")
        except:
            print("error!")
        continue
    """
    |new user.txt
    �½�user.txt�����ļ�
    """
    new_user = "$����user.txt�����ļ�|Generate user.txt configuration file !"
    if _user == 'new user':
        try:
            print("\n����user.txt�ļ�")
            new.new_user()
            true = os.path.exists('user.txt')
            if true == True:
                print("\nuser.txt�ļ��Ѵ��ڣ�\n")
            else:
                print("\n���ɳɹ���\n")
        except:
            print("\n����ʧ�ܣ�\n")
        continue
    """
    |ԭ��
    ԭ��ʵ�
    """
    if _user == 'Genshin Impact' or _user == 'ys':
        print("\nGenshin Impact !")
        print("\n$ԭ������Ҳ��ԭ��ѽ��")
        print("\n$original! You also play with the original God !\n")
        img_ys("QuadraticElement\\img\\ys2.1.jfif")
        continue
    """
    |open
    ���ļ�����ҳ
    """
    open_file = "$��ָ��·���е��ļ�|Open the file in the specified path"
    if _user == 'open>file':
        file = input("EXE_path>")
        if os.path.exists(file) == True:  # �ж��ļ���·���Ƿ����
            if os.path.isfile(file) == True:  # �ж��ļ�·���Ƿ����
                op.open_file(f"{file}")
            elif os.path.exists(file) == False:
                print("There is no such file !")
        elif os.path.exists(file) == False:
            print("There is no such path !")
        continue
    open_url = "$��ָ��������ҳ|Open the specified linked page"
    if _user == 'open>url':
        urls = input("URL>")
        op.open_url(urls)
        continue
    """
    |color
    ��ɫ����
    """
    colors = "$�Զ�����������ɫ|Custom command line colors"
    if _user == 'color':
        color_ = input("color>")
        os.system(f"color {color_}")
        continue
    """
    |Poli
    ����Poli������
    """
    Polis = "$����Poli������|Connect Poli robot"
    if _user == 'Poli':
        run_Poli()
        continue
    """
    |cd
    """
    if _user in 'cd':
        path = input("PATH>")
        os.system(f"cd {path}")
        continue
    """
    |Find_folder>
    ��ָ���̷���ѯ�ļ�λ��
    """
    folder = "$��ָ���̷���ѯ�ļ�λ��|Query the file location in the specified drive letter"
    if _user == 'Find_folder>' or _user == 'seefile':
        path = input("PATH>") # �ļ���λ��
        file = input("FILE_NAME>") # �ļ�������
        com = input("Export folder>") # �Ƿ�����ļ���
        if com == '':
            see.seefile(f'{path}', f'{file}')
        else:
            see.seefile(f'{path}', f'{file}', f'{com}')
        continue
    """
    |Suffix_lookup>
    ���ָ���̷��е�ָ����׺���ļ�
    """
    Suffix = "$���ָ���̷��е�ָ����׺���ļ�|Output the file with the specified suffix in the specified drive letter"
    if _user == 'Suffix_lookup>' or _user == 'SL':
        path = input("PATH>") # ·��
        Suffix = input("Suffix>") # ��׺��
        see.seeSuffix(f'{path}', f'{Suffix}')
        continue
    """
    |help
    ��������鿴����ʹ�÷�����
    """
    if _user == "help":
        message = input("Help>")
        # ȫ��ָ��
        if message == '--help':
            os.system("color 5")
            print("\n\t=====================================")
            print("\n\tdownload", help_dow,
                  "\n\tuser_message", help_user_message,
                  "\n\tnew user", new_user,
                  "\n\topen>file", open_file,
                  "\n\topen>url", open_url,
                  "\n\tcolor", colors,
                  "\n\tPoli", Polis,
                  "\n\t", folder,
                  "\n\t", Suffix,
                  )
            input("�س�ȷ�ϣ�")
            os.system("color 2")
            continue
        # ����ָ��
        if message == 'download' or message == 'dow':
            print("=====================================")
            print("\t", help_dow)
            print("\t���룺download �� dow ����ʹ����������")
            print("\tURL>�����ļ���ҳ����")
            print("\tFILE>�����ļ���·��")
            continue
        # �û���Ϣ
        if message == 'user_message':
            print("=====================================")
            print("\t", help_user_message)
            print("\t�������user_message")
            print("\t�鿴�����ļ�������Ϣ")
            continue
        # �½��û������ļ�
        if message == 'new user':
            print("=====================================")
            print("\t", new_user)
            print("\t�������new user")
            print("\t�½�һ���û������ļ�:user.txt")
            continue
        # ���ļ�
        if message == 'open>file':
            print("=====================================")
            print("\t", open_file)
            print("\t�������open>file")
            print("\t��ָ��·���ļ�")
            continue
        # ����ҳ
        if message == 'open>url':
            print("=====================================")
            print("\t", open_url)
            print("\t���룺open>url")
            print("\tURL>��������ҳ�����磺www.baidu.com")
            continue
        # color�������Զ�����ɫ
        if message == 'color':
            print("=====================================")
            print("\t", colors)
            print("\t�������color xxx xxx������ɫ����")
            print("\tcolor>����Ҫ���ĵ���ɫ����")
            print("\t��windowsϵͳ�е�color������ͬ")
            print("\t��ɫ����������ʮ����������ָ�� -- ")
            print("\t��һ����Ӧ�ڱ������ڶ�����Ӧ��ǰ����ÿ�����֣�����Ϊ�����κ�ֵ:")
            print("\n\t\t 0 = ��ɫ    8 = ��ɫ")
            print("\n\t\t 1 = ��ɫ    9 = ����ɫ")
            print("\n\t\t 2 = ��ɫ    A = ����ɫ")
            print("\n\t\t 3 = ǳ��ɫ  B = ��ǳ��ɫ")
            print("\n\t\t 4 = ��ɫ    C = ����ɫ")
            print("\n\t\t 5 = ��ɫ    D = ����ɫ")
            print("\n\t\t 6 = ��ɫ    E = ����ɫ")
            print("\n\t\t 7 = ��ɫ    F = ����ɫ")
            continue
        # ��Poli�����������ѯ
        if message == "Poli":
            print("=====================================")
            print('\t', Polis)
            print("\t�������Poli���ɴ�")
            print("\t����help�鿴����ָ��")
            print("\t����ʹ�÷��������Բο���վ��https://47.108.189.192/PyPoli/")
        # ��ָ���̷���ѯ�ļ�λ��
        if message == "Find_folder>" or message == 'seefile':
            print("=====================================")
            print("\t", folder)
            print('\t�������Find_folder �� seefile')
            print('\tPATH> ����Ҫ��ѯ���̷��磺C')
            print('\tFILE_NAME> �ļ�����')
            print('\tExport folder> �Ƿ��������ʱ���ļ��� Y�� �س���ʾ�����')
        # ���ָ���̷��е�ָ����׺���ļ�
        if message == 'Suffix_lookup>' or message == 'SL':
            print("=====================================")
            print("\t", Suffix)
            print("\t PATH> ����Ҫ��ѯ���̷��磺C")
            print("\t Suffix> Ҫ���ҵ��ļ���׺��")
        # �û�����������Чִ����������
        else:
            print(f"Not command {message}")
        continue
    """
    |quit
    �˳��ն�����
    """
    if _user == 'quit' or _user == 'q':
        break
    # �û�����������Чִ����������
    else:
        print(f"{_user} Is Not Command !")
        continue
