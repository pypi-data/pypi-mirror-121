#coding:gbk
from urllib.parse import urlencode
import requests
import urllib
import json

def yq():
    message = input("������У�")
    url="https://api.iyk0.com/yq/?msg={}".format(message)
    request=url
    re=requests.get(request)
    rep = re.json()

    code = rep.get('code')
    msg = rep.get('msg')
    cxdq = rep.get('��ѯ����')
    mqqz = rep.get('Ŀǰȷ��')
    swrs = rep.get('��������')
    zyrs = rep.get('��������')
    xzqz = rep.get('����ȷ��')
    xcqz = rep.get('�ִ�ȷ��')
    xcwzz = rep.get('�ִ���֢״')
    time = rep.get('time')

    print("��ѯ������",cxdq)
    print("\tĿǰȷ�",mqqz)
    print("\t����������",swrs)
    print("\t����������",zyrs)
    print("\t����ȷ�",xzqz)
    print("\t�ִ�ȷ�",xcqz)
    print("\t�ִ���֢״��",xcwzz)
    print("\t����ʱ�䣺",time)
