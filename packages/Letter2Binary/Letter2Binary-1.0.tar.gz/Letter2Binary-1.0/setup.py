from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open('README.md') as f:
    long_description = f.read()

setup(
  name = 'Letter2Binary',        
  packages = ['ltb_s'],   
  version = '1.0',    
  license='MIT',     
  description = 'Letter to binary', 
  long_description=long_description,
  author = 'iFanpS',                  
  author_email = 'imezz8424@gmail.com',     
  keywords = ['ltbfan', 'ltb_s', 'ltb'], 
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)