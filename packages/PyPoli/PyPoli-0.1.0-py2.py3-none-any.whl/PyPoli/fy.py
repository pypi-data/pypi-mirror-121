#coding:gbk
from urllib.parse import urlencode
import requests
import urllib
import json

def fy():
    message = input("����Ҫ��������֣�")
    url="https://api.vvhan.com/api/fy?text={}".format(message)
    request=url
    re=requests.get(request)
    rep = re.json()

    data = rep.get('data')
    print("\n",data['text'])
    print(data['fanyi'],"\n")
