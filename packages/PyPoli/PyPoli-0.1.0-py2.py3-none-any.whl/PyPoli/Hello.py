#coding:gbk

class PoliRobot_Hello:

    def __init__(self,name,age,message):
        self.name = name
        self.age = age
        self.message = message

    def Hello(self):
        print(f"Hello! ����{self.name} !")

    def Poilage(self):
        print(f"���� {self.age} ���ˣ�")

    def Poilmessage(self):
        print(f"{self.message}")