import os
import sys
import getpass
def gegus():
    print("loading")
    g = sys.version
    h = g.split(".")
    m = str(h[0])+str(h[1])
    os.system('setx path "%path%;C:/Users/'+getpass.getuser()+'/AppData/Local/Programs/Python/Python'+m+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')