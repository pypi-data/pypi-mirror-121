
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='calc_naive',
  version='0.0.1',
  description='naive calculator',
  long_description=open('README.txt').read(),
  url='',  
  author='Mehdi anzal',
  author_email='mrezvandehy@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calc', 
  packages=find_packages(),
  install_requires=[''] 
)