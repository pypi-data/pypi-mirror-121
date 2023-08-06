# coding:gbk
"""
OS:Windows 10 专业版
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
def img_ys(path):  # 彩蛋01
    img = cv2.imread(path, 1)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


"""
|library
检测第三方库是否安装
"""
_library.pip_library()  # 检查需要的第三方库是否安装
os.system("color 2")  # 更换界面字体颜色
# 无限循环命令行
while True:
    _user = input("\n@QuadraticElement#>")  # user输入
    '''
    |user_message
    用户信息查询
    '''
    help_user_message = "$用户信息|User information"  # help
    if _user == "user_message":
        print("\n")
        um.USERNAME()
        continue

    """
    |wget
    网页下载工具
    """
    help_dow = "$下载命令|Download command"  # help
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
    新建user.txt配置文件
    """
    new_user = "$生成user.txt配置文件|Generate user.txt configuration file !"
    if _user == 'new user':
        try:
            print("\n生成user.txt文件")
            new.new_user()
            true = os.path.exists('user.txt')
            if true == True:
                print("\nuser.txt文件已存在！\n")
            else:
                print("\n生成成功！\n")
        except:
            print("\n生成失败！\n")
        continue
    """
    |原神
    原神彩蛋
    """
    if _user == 'Genshin Impact' or _user == 'ys':
        print("\nGenshin Impact !")
        print("\n$原来！你也玩原神呀！")
        print("\n$original! You also play with the original God !\n")
        img_ys("QuadraticElement\\img\\ys2.1.jfif")
        continue
    """
    |open
    打开文件或网页
    """
    open_file = "$打开指定路径中的文件|Open the file in the specified path"
    if _user == 'open>file':
        file = input("EXE_path>")
        if os.path.exists(file) == True:  # 判断文件夹路径是否存在
            if os.path.isfile(file) == True:  # 判断文件路径是否存在
                op.open_file(f"{file}")
            elif os.path.exists(file) == False:
                print("There is no such file !")
        elif os.path.exists(file) == False:
            print("There is no such path !")
        continue
    open_url = "$打开指定链接网页|Open the specified linked page"
    if _user == 'open>url':
        urls = input("URL>")
        op.open_url(urls)
        continue
    """
    |color
    颜色调整
    """
    colors = "$自定义命令行颜色|Custom command line colors"
    if _user == 'color':
        color_ = input("color>")
        os.system(f"color {color_}")
        continue
    """
    |Poli
    连接Poli机器人
    """
    Polis = "$连接Poli机器人|Connect Poli robot"
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
    在指定盘符查询文件位置
    """
    folder = "$在指定盘符查询文件位置|Query the file location in the specified drive letter"
    if _user == 'Find_folder>' or _user == 'seefile':
        path = input("PATH>") # 文件夹位置
        file = input("FILE_NAME>") # 文件夹名字
        com = input("Export folder>") # 是否输出文件夹
        if com == '':
            see.seefile(f'{path}', f'{file}')
        else:
            see.seefile(f'{path}', f'{file}', f'{com}')
        continue
    """
    |Suffix_lookup>
    输出指定盘符中的指定后缀名文件
    """
    Suffix = "$输出指定盘符中的指定后缀名文件|Output the file with the specified suffix in the specified drive letter"
    if _user == 'Suffix_lookup>' or _user == 'SL':
        path = input("PATH>") # 路径
        Suffix = input("Suffix>") # 后缀名
        see.seeSuffix(f'{path}', f'{Suffix}')
        continue
    """
    |help
    帮助命令，查看命令使用方法。
    """
    if _user == "help":
        message = input("Help>")
        # 全部指令
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
            input("回车确认：")
            os.system("color 2")
            continue
        # 下载指令
        if message == 'download' or message == 'dow':
            print("=====================================")
            print("\t", help_dow)
            print("\t输入：download 或 dow 即可使用下载命令")
            print("\tURL>下载文件网页链接")
            print("\tFILE>下载文件至路径")
            continue
        # 用户信息
        if message == 'user_message':
            print("=====================================")
            print("\t", help_user_message)
            print("\t输入命令：user_message")
            print("\t查看配置文件所有信息")
            continue
        # 新建用户配置文件
        if message == 'new user':
            print("=====================================")
            print("\t", new_user)
            print("\t输入命令：new user")
            print("\t新建一个用户配置文件:user.txt")
            continue
        # 打开文件
        if message == 'open>file':
            print("=====================================")
            print("\t", open_file)
            print("\t输入命令：open>file")
            print("\t打开指定路径文件")
            continue
        # 打开网页
        if message == 'open>url':
            print("=====================================")
            print("\t", open_url)
            print("\t输入：open>url")
            print("\tURL>处输入网页链接如：www.baidu.com")
            continue
        # color命令行自定义颜色
        if message == 'color':
            print("=====================================")
            print("\t", colors)
            print("\t输入命令：color xxx xxx等于颜色数字")
            print("\tcolor>输入要更改的颜色类型")
            print("\t与windows系统中的color命令相同")
            print("\t颜色属性由两个十六进制数字指定 -- ")
            print("\t第一个对应于背景，第二个对应于前景。每个数字，可以为以下任何值:")
            print("\n\t\t 0 = 黑色    8 = 灰色")
            print("\n\t\t 1 = 蓝色    9 = 淡蓝色")
            print("\n\t\t 2 = 绿色    A = 淡绿色")
            print("\n\t\t 3 = 浅绿色  B = 淡浅绿色")
            print("\n\t\t 4 = 红色    C = 淡红色")
            print("\n\t\t 5 = 紫色    D = 淡紫色")
            print("\n\t\t 6 = 黄色    E = 淡黄色")
            print("\n\t\t 7 = 白色    F = 亮白色")
            continue
        # 打开Poli机器人命令查询
        if message == "Poli":
            print("=====================================")
            print('\t', Polis)
            print("\t输入命令：Poli即可打开")
            print("\t输入help查看所有指令")
            print("\t具体使用方法，可以参考网站：https://47.108.189.192/PyPoli/")
        # 在指定盘符查询文件位置
        if message == "Find_folder>" or message == 'seefile':
            print("=====================================")
            print("\t", folder)
            print('\t输入命令：Find_folder 或 seefile')
            print('\tPATH> 输入要查询的盘符如：C')
            print('\tFILE_NAME> 文件名字')
            print('\tExport folder> 是否输出查找时的文件夹 Y是 回车表示不输出')
        # 输出指定盘符中的指定后缀名文件
        if message == 'Suffix_lookup>' or message == 'SL':
            print("=====================================")
            print("\t", Suffix)
            print("\t PATH> 输入要查询的盘符如：C")
            print("\t Suffix> 要查找的文件后缀名")
        # 用户输入命令无效执行以下命令
        else:
            print(f"Not command {message}")
        continue
    """
    |quit
    退出终端命令
    """
    if _user == 'quit' or _user == 'q':
        break
    # 用户输入命令无效执行以下命令
    else:
        print(f"{_user} Is Not Command !")
        continue
