from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
from distutils.command.install import install as _install
import os
def _post_install(dir):
    from subprocess import call
    call([sys.executable, 'hello.py'])
class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install)
setup(name='mminepy', # 패키지 명
version='1.1.2.12',

description='minepy from elbert06',

author='elbert06',

author_email='elbert06@hanmail.net',

license='MIT', # MIT에서 정한 표준 라이센스 따른다
packages=find_packages(),
py_modules=['mminepy'], # 패키지에 포함되는 모듈
python_requires='>=3',
include_package_data=True,
cmdclass={
    'install':install
}
)