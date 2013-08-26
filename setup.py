# -*- coding: utf-8 -*-

from setuptools import setup
 
setup(
    name='pycflow2dot',
    version='0.2',
    py_modules=['pycflow2dot'],
    license='GPLv3',
    description='Create C call graphs from multiple source files ' +
        'using Cflow, producing linked PDF.',
    long_description=open('README.md').read(),
    author='Dabaichi Valbendan, Ioannis Filippidis',
    author_email='valbendan@hotmail.com',
    install_requires=['networkx'],
    entry_points={
        'console_scripts': [
            'pycflow2dot = pycflow2dot:main',
        ]
    }
)
