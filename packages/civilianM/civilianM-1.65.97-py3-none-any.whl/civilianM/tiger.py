import __init__ as cm
#coding:UTF-8
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : AUX/ For wang-jin-hu Only
#Now version: V1.65.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
class i():
    def __init__(self):
        mx='不可以昧着良心说话！'
        xt='不可以瞎填！'
        a = cm.judge('小虎帅不帅？','tf')
        if a == False:
            b = cm.judge("想不想加入撕虎集团？",'yn')
            if b == True:
                print("这才对")
                return None
            elif b == False:
                raise FutureWarning(mx)
            elif b == None:
                raise SyntaxError(xt)
        elif a == True:
            raise SyntaxWarning(mx)
        elif a == None:
            raise SyntaxError(xt)
i()
