from setuptools import setup, find_packages

VERSION = '6.2'
PROJECT_NAME = 'evolene'

setup(name=PROJECT_NAME,
      version=VERSION,
      description='KTH CD/CI pipeline tool',
      url='https://gita.sys.kth.se/Infosys/evolene',
      author='Jens Tinglev',
      author_email='tinglev@kth.se',
      license='MIT',
      zip_safe=False,
      packages=find_packages())
