import os
import sys
import getpass
def gegus():
    print("loading")
    g = sys.version
    h = g.split(".")
    m = str(h[0])+str(h[1])
    os.chdir("C:/Users/"+getpass.getuser()+"/AppData/Local/Programs/Python/Python"+m+"/Lib/site-packages/mminepy-1.1.3.0.dist-info")
    os.system("move minepy.exe ..")
    os.chdir("..")
    os.system("move minepy.exe ..")
    os.chdir("..")
    os.system("move minepy.exe ..")
    os.chdir("..")
    # setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python37/Lib/site-packages/mminepy-1.1.1.17.dist-info;