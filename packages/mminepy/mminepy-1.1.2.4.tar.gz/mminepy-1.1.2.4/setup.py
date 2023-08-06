from setuptools import setup, find_packages
class PostDevelopCommand():
    def __init__(self):
        import os
        import sys
        m = sys.version
        mr = m.split(".")
        h = mr[0]+mr[1]
        os.system('setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python'+h+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')
        print('setx path "%path%;C:/Users/KIMMJU/AppData/Local/Programs/Python/Python'+h+'/Lib/site-packages/mminepy-1.1.1.17.dist-info;"')

setup(name='mminepy', # 패키지 명

version='1.1.2.4',

description='minepy from elbert06',

author='elbert06',

author_email='elbert06@hanmail.net',

license='MIT', # MIT에서 정한 표준 라이센스 따른다
packages=find_packages(),
py_modules=['mminepy'], # 패키지에 포함되는 모듈
python_requires='>=3',
include_package_data=True,
cmdclass={
    'develop': PostDevelopCommand,
},
)