try:
    from civilianM import *
    #from __init__ import *
    import os
    from OpenSSL import crypto,SSL
except:
    e = error()
    e.Import("Please first install 'PyOpenSSL' module")
e=error()
#coding:UTF-8
#Author : AC97
#Project name : civilianM
#Class : MAIN
#Now version: V1.80.97
#Contact EMail: ehcemc@163.com
#NO COPYING!
class do():
    def __init__(self):
        a = input("Enter your country(example:CN/EN):")
        if len(a) != 2:
            raise NameError("Must enter country name abbreviation,example:EN,and must upper")
        b = input("Enter where are you's province/state/region:")
        c = input("Enter where're you's city:")
        d = input("Enter Your organization name:")
        e = input("Enter Issuer name:")
        f = input("Enter file name:")
        cn = judge("Please make sure that the falsity of the exported information has nothing to do with me. Please know",'yn')
        if cn:
            vd = captcha()
            cs = hideInput('('+vd+')Please enter verification-code:')
            if cs!=vd:
                raise Exception("Verification defeat")
            else:
                print("verification success")
                wait(2)
                print("Save to "+os.getcwd())
                wait(2)
                savefilename = f+ ".crt"
                passwordfile = f + ".key"
                k = crypto.PKey()
                k.generate_key(crypto.TYPE_RSA, 2048)
                cert = crypto.X509()
                cert.get_subject().C = a
                cert.get_subject().ST = b
                cert.get_subject().L = c
                cert.get_subject().O = d
                cert.get_subject().OU = "IT and Security Department"
                cert.get_subject().CN = e
                cert.gmtime_adj_notBefore(0)
                cert.set_serial_number(1000)
                cert.gmtime_adj_notAfter(68*365*24*60*60)
                cert.set_issuer(cert.get_subject())
                cert.set_pubkey(k)
                cert.sign(k, 'SHA256')
                open(savefilename,'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
                open(passwordfile,'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
                openFolder(os.getcwd())
        elif cn==False or cn==None:
            raise NameError('This session is terminated because you do not agree to the agreement')
do()
