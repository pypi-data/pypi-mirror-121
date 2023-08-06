import os
import sys
m = sys.version
mr = m.split(".")
h = mr[0]+mr[1]
os.system('setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python'+h+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')
print('setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python'+h+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')