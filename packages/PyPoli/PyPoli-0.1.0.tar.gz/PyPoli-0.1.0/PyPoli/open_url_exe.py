#coding:gbk
import os

def open_url_exe():
    message = input("open��")
    if message == '':
        print("Ҫ�򿪵�Ϊ�գ�")
    else:
        os.system(f"start {message}")