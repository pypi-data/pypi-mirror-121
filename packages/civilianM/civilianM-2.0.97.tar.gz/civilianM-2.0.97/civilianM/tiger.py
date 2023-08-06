from civilianM import *
#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : AUX/ For wang-jin-hu Only
#Now version: V2.00.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
ceb = False
class test():
    def __init__(self):
        global ceb
        mx='不可以昧着良心说话！'
        xt='不可以瞎填！'
        a = judge('小虎帅不帅？','tf')
        if a == False:
            b = judge("想不想加入撕虎集团？",'yn')
            if b == True:
                ceb=True
            elif b == False:
                raise ConscienceError(mx)
            elif b == None:
                raise SyntaxError(xt)
        elif a == True:
            raise ConscienceError(mx)
        elif a == None:
            raise SyntaxError(xt)
def re():
    global ceb
    if ceb:
        return  True

