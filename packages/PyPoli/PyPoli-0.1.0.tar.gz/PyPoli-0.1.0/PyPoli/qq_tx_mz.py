#coding:gbk
from urllib.parse import urlencode
import requests
import urllib
import json

def qq_tx_mz():
    message = str(input("Ҫ��ѯ��QQ��"))

    url="https://api.iyk0.com/qqxx/?qq={}".format(message)
    request=url
    re=requests.get(request)
    rep = re.json()

    code = rep.get('code')
    imgurl = rep.get('imgurl')
    name = rep.get('name')
    print("\nQQ��Ϊ��",message)
    print("QQͷ���ַ��",imgurl)
    print("QQ���֣�",name,"\n")
