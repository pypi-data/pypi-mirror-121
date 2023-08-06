import os
import sys
import getpass
def gegus():
    print("loading")
    g = sys.version
    h = g.split(".")
    m = str(h[0])+str(h[1])
    os.system('setx hello "C:/Users/'+getpass.getuser()+'/AppData/Local/Programs/Python/Python'+m+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')
    os.system('setx path "%path%;%hello%;" -m')
    # setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python37/Lib/site-packages/mminepy-1.1.1.17.dist-info;