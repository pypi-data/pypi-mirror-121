from setuptools import setup, find_packages

setup(
    name='QuadraticElement',#包名
    version='0.0.4',#版本
    description=("命令行项目"), #包简介
    long_description=open('README.md',encoding="utf-8").read(),#读取文件中介绍包的详细内容
    long_description_content_type="text/markdown",
    author='PYmili',#作者
    author_email='mc2005wj@163.com',#作者邮件
    maintainer='PYmili',#维护者
    maintainer_email='mc2005wj@163.com',#维护者邮件
    license='MIT License',#协议
    url='https://codechina.csdn.net/qq_53280175/quadraticelement',#包存放地址
    packages=find_packages(),#包的目录
    classifiers=[
          #'Intended Audience :: Developers',#目标受众   Developers:开发者
          'Operating System :: OS Independent',#操作系统
          'Natural Language :: Chinese (Simplified)',#使用语言中文简体
          'License :: OSI Approved :: MIT License',#许可证
          #'Programming Language :: Python',
          #'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 2.7',
          #'Programming Language :: Python :: 3',#使用版本
          #'Programming Language :: Python :: 3.5',
          #'Programming Language :: Python :: 3.6',
          #'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'#主题  软件开发  库
          #"License :: OSI Approved :: GNU General Public License (GPL)",#许可证
      ],
    python_requires='>=3.8',
    #install_requires=[''],
    install_requires=[
        'FastDataTime>=0.0.8',
        'RandomKey>=0.0.1',
        'numpy>=1.21.2',
        'wget>=3.2',
        'opencv-python>=4.5.3.56',
        'PyPoli>=0.1.0',
        'FolderProcessing>=0.1.1.2',
    ]#安装所需要的库
)

