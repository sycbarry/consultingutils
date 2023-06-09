import setuptools
from setuptools import find_packages
import re

with open("README.md", 'r', encoding="utf-8") as f: 
    long_description = f.read()

setuptools.setup(
        name='consultingutils', 
        version='0.0.1', 
        author='Sebastian Barry', 
        author_email='barrys@sms-inc.net', 
        long_description=long_description, 
        description='Tools for Technical Consultants - Like never seen before.',
        url='https://github.com/sycbarry/consultingutils.git', 
        license='MIT', 
        install_requires=['pandas', 'langchain', 'oracledb', 'ibm-db', 'untangle', 'openai', 'tqdm', 'cx_Oracle', 'tqdm', 'setuptools'],
        packages=find_packages(),
        )
