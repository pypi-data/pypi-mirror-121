import os
import sys
import getpass
def gegus():
    print("loading")
    g = sys.version
    h = g.split(".")
    m = str(h[0])+str(h[1])
    path_dir = "C:/Users/"+getpass.getuser()+"/AppData/Local/Programs/Python"
    os.chdir("C:/Users/"+getpass.getuser()+"/AppData/Local/Programs/Python")
    file_list = os.listdir(path_dir)
    for i in file_list:
        if os.path.isdir(i+"/Lib/site-packages/mminepy-1.1.3.5.dist-info"):
            os.chdir(i+"/Lib/site-packages/mminepy-1.1.3.5.dist-info")
            os.system("move minepy.exe ..")
            os.chdir("..")
            os.system("move minepy.exe ..")
            os.chdir("..")
            os.system("move minepy.exe ..")
            os.chdir("..")
    # setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python37/Lib/site-packages/mminepy-1.1.1.17.dist-info;