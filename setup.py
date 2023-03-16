import setuptools
from setuptools import find_packages
import re

with open("README.md", 'r', encoding="utf-8") as f: 
    long_description = f.read()

setuptools.setup(
        name='consulting_utils', 
        version='0.0.1', 
        author='Sebastian Barry', 
        author_email='barrys@sms-inc.net', 
        long_description=long_description, 
        description='Tools for Technical Consultants - Like never seen before.',
        url='https://github.com/sycbarry/consulting_utils.git', 
        license='MIT', 
        install_requires=['pandas', 'langchain', 'oracledb', 'ibm-db', 'untangle', 'openai', 'tqdm', 'cx_Oracle --upgrade', 'tqdm'],
        packages=find_packages(),
        )
