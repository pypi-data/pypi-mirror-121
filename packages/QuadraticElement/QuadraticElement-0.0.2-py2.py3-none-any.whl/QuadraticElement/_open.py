#coding:gbk

import os
import re

def open_file(exepath):
    os.system(f"start {exepath}")

def open_url(url):
    try:
        os.system(f"start {url}")
    except:
        print("Error!")
