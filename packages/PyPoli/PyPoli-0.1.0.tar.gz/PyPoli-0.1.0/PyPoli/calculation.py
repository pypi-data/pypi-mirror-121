#coding:gbk

def addition():
    try:
        number = eval(input("��������1��"))
        numbers = eval(input("��������2��"))
        additions = number + numbers
        print(additions)
    except:
        print("����������")
def multiplication():
    number = eval(input("��������1��"))
    numbers = eval(input("��������2��"))
    multiplications = number * numbers
    print(multiplications)
def division():
    number_c = eval(input("��������1��"))
    numbers_c = eval(input("��������2��"))
    divisions = number_c/numbers_c
    divisionr = number_c//numbers_c
    print(divisions)
    print(divisionr)