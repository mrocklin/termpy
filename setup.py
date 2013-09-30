from os.path import exists
from setuptools import setup

setup(name='termpy',
      version='0.1',
      description='Term manipulation',
      url='http://github.com/logpy/term/',
      author='Matthew Rocklin',
      author_email='mrocklin@gmail.com',
      license='BSD',
      packages=['termpy'],
      long_description=open('README.md').read() if exists("README.md") else "",
      zip_safe=False)
