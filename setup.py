# -*- coding: utf-8 -*-

import os
from setuptools import setup

long_description = 'Add a fallback short description here'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
else:
    long_description=open('README.md').read()

setup(
    name='pycflow2dot',
    version='0.2',
    py_modules=['pycflow2dot'],
    license='GPLv3',
    description='Create C call graphs from multiple source files ' +
        'using Cflow, producing linked PDF.',
    long_description=long_description,
    author='Ioannis Filippidis, Dabaichi Valbendan',
    author_email='jfilippidis@gmail.com',
    url = 'https://github.com/johnyf/pycflow2dot',
    download_url = 'https://github.com/johnyf/pycflow2dot/tarball/0.2',
    install_requires=['networkx'],
    entry_points={
        'console_scripts': [
            'pycflow2dot = pycflow2dot:main',
        ]
    },
    keywords = ['c', 'call graph', 'control flow', 'dot',
                'latex', 'cflow'],
    classifiers = [],
)
