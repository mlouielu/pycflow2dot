# -*- coding: utf-8 -*-

import os
from setuptools import setup

if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
elif os.path.exists('README.md'):
    long_description=open('README.md').read()
else:
    print('Could not find readme from which to extract long_description.')
    long_description = ''

setup(
    name='pycflow2dot',
    version='0.2',
    py_modules=['pycflow2dot'],
    license='GPLv3',
    description='Create C call graphs from multiple source files ' +
        'using Cflow, producing linked PDF.',
    long_description=long_description,
    author='Ioannis Filippidis',
    author_email='jfilippidis@gmail.com',
    url = 'https://github.com/johnyf/pycflow2dot',
    download_url = 'https://github.com/johnyf/pycflow2dot/archive/v0.2.tar.gz',
    install_requires=['networkx'],
    entry_points={
        'console_scripts': [
            'cflow2dot = pycflow2dot:main',
        ]
    },
    keywords = ['c', 'call graph', 'control flow', 'dot',
                'latex', 'cflow'],
    classifiers = [],
)
