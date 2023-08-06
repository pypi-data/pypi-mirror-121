#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : MAIN
#Now version: V1.65.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
import time
import platform
import os
import random
import winreg
import requests
import json
import getpass
from bs4 import BeautifulSoup as bs
from datetime import datetime as dt
v='1.65.97'
print("Welcome use civilianM,current version：1.65.97")

def upgrade():
    global v
    dd = []
    try:
        r = requests.get('https://pypi.org/project/civilianM/#history')
    except:
        raise Exception('Please check network connect status')
    s = bs(r.text,'lxml')
    d = s.find_all('p',class_='release__version')
    for nn in d:
        ev = nn.text.strip()
        dd.append(ev)
    if dd[0] != v:
        print('You are using '+versions()+',A new version is available:'+dd[0])
    elif dd[0] == v:
        print("You are currently using's "+dd[0]+" is the latest version and doesnt need to be updated")
def how():
    print("""""")

def versions():
    global v
    return v

def checkClass(objects,need):
    if need == 'str':
        return type(objects) is type('')
    elif need == 'list':
        return type(objects) is type([])
    elif need == 'dict':
        return type(objects) is type({})
    elif need == 'int':
        return type(objects) is type(1)
    elif need == 'float':
        return type(objects) is type(0.1)
    elif need == 'tuple':
        return type(objects) is type(())
    else:
        raise AttributeError("In checkClass this function,No "+str(need)+" this attribute")

#Sleep
def wait(t):
    if checkClass(t,'float') or checkClass(t,'int'):
        time.sleep(t)
    else:
        raise ValueError("You enter's result must is a int/float-number")

#Randomly generated number
def randint(mins,maxs):
    if checkClass(mins,'int') == False or checkClass(maxs,'int') == False:
        raise ValueError("You enter's result must is a int-number")
    if maxs == mins:
        raise ValueError("Max-number cannot equal to min-number")
    elif mins > maxs:
        raise ValueError("Min-number cannot greater than max-number")
    return random.randint(mins,maxs)

def garbledCode(digit=20,types=None):
    result = ""
    if types == None or types == 'Upper':
        pass
    else:
        raise AttributeError('GarbledCode this function has not have '+str(types)+'  this parameter')
    np= ""
    standard = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f']
    if checkClass(digit,'int')==False:
        raise ValueError("You enter's result must is a not string number!")
    for n in range(digit):
        np = standard[randint(0,15)]
        if types == 'Upper':
            if checkClass(np,'str'):
                result += np.upper()
            else:
                result += str(np)
        else:
            result += str(np)
    return result

def pausePrint(*content,pause=0.2):
    if checkClass(pause,'float') or checkClass(pause,'int'):
        for tex in content:
            for prin in tex:
                print(prin,end='',flush=True)
                wait(pause)
            print(" ",flush=True,end="")
        print("\n",flush=True,end="")
    else:
        raise ValueError("You enter's result must is a int/float-number")
    
def captcha():
    capt = ''
    N = [1,2,3,4,5,6,7,8,9,0,'a','A','b','B','c','C','d','D','e','E','f','F','g','G','h','H','i','I','j','J','k','K','l','L','m','M',
         'n','N','o','O','p','P','q','Q','r','R','s','S','t','T','u','U','v','V','w','W','x','X','y','Y','z','Z']
    for n in range(4):
        capt += str(N[randint(0,57)])
    return capt

def judge(content,classes):
    """
    Two option,
    content is can custom.
    classes:
        yn(Yes/No)
        tf(True/False)
        oc(Ok/Cancel)
    """
    if classes == 'yn':
        ace = input(content+'(Y/N):')
        ace = ace.upper()
        if ace == 'Y':
            return True
        elif ace == 'N':
            return False
        else:
            return None
    if classes == 'tf':
        ace = input(content+'(T/F):')
        ace = ace.upper()
        if ace == 'T':
            return True
        elif ace == 'F':
            return False
        else:
            return None
    if classes == 'oc':
        ace = input(content+"(ok/cancel):")
        ace = ace.lower()
        if ace == 'ok':
            return True
        elif ace == 'cancel':
            return False
        else:
            return None
        
def hideInput(con):
    a = getpass.getpass(con)
    return a

def justNow():
    b = dt.today()
    return b.strftime("%Y-%m-%d %H:%M:%S")

def openFolder(fn):
    def efve():
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0] + "/"
    if fn:
        nh = efve() + fn
    if not os.path.exists(nh):
            os.mkdir(nh)
    else:
        nh = os.getcwd()

    if platform.system() == "Windows":
        os.startfile(nh)

    #return nh + "/"

def getAddress():
    try:
        re = requests.get('https://ipw.cn/api/ip/locate')
    except:
        raise Exception("Please check network connect status")
    d = json.loads(re.text)
    PR = d['Address']['Province']
    ISP = "中国"+d['ISP']
    if PR == '广西' or PR == '内蒙古' or PR == '宁夏' or PR == '新疆':
        if PR == '广西':
            PR += '壮族自治区'
        if PR == '内蒙古':
            PR += '自治区'
        if PR == '宁夏':
            PR += '回族自治区'
        if PR == '新疆':
            PR += '维吾尔自治区'
    else:
        PR += '省'
    C = d['Address']['City'] + '市'
    nr = [d['Address']['Country'],PR,C,d['IP'],ISP]
    return nr

class os():
    def __init__(self):
        pass
    def clearScreen(self):
        try:
            os.system('cls')
        except:
            raise Exception("Please do not use the editor to run clearScreen")
    def shutdown(self):
        """DANGEROUS"""
        os.system("shutdown -p")

class error():
    def __init__(self):
        pass
    def attr(self,cont=None):
        if cont==None:
            raise AttributeError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise AttributeError(cont)
    def synt(self,cont=None):
        if cont==None:
            raise SyntaxError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise SyntaxError(cont)
    def valu(self,cont=None):
        if cont ==None:
            raise ValueError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise ValueError(cont)
    def exce(self,cont=None):
        if cont==None:
            raise Exception('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise Exception(cont)
    def name(self,cont=None):
        if cont==None:
            raise NameError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise NameError(cont)
    def io(self,cont=None):
        if cont==None:
            raise IOError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IOError(cont)
    def Type(self,cont=None):
        if cont==None:
            raise TypeError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise TypeError(cont)
    def inde(self,cont=None):
        if cont==None:
            raise IndentationError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IndentationError(cont)
    def index(self,cont=None):
        if cont==None:
            raise IndexError('The passed in function cannot be left blank and equal to None')
        elif cont != None:
            raise IndexError(cont)
    def impo(self,cont=None):
        if cont == None:
            raise ImportError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise ImportError(cont)
    def key(self,cont=None):
        if cont == None:
            raise KeyError('The passed in function cannot be left blank and equal to None')
        elif cont!=None:
            raise KeyError(cont)
    #'The passed in function cannot be left blank and equal to None'

class author():
    def __init__(self):
        pass
    def name(self):
        print('AC97')
    def email(self):
        print("ehcemc@163.com")
    def old(self):
        print("UNKNOWN")
    def gender(self):
        print('male')
    def phoneNumber(self):
        print('13417----01')
    def From(self):
        print("CN")
    
