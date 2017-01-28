"""Installation script."""
import os
from setuptools import setup

if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
elif os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    print('Could not find readme from which to extract long_description.')
    long_description = ''


def run_setup():
    setup(
        name='pycflow2dot',
        version='0.2.1',
        py_modules=['pycflow2dot'],
        license='GPLv3',
        description=(
            'Create C call graphs from multiple source files '
            'using Cflow, producing linked PDF.'),
        long_description=long_description,
        author='Ioannis Filippidis',
        author_email='jfilippidis@gmail.com',
        url='https://github.com/johnyf/pycflow2dot',
        install_requires=[
            'networkx == 1.10',
            'pydot >= 1.2.3'],
        entry_points={
            'console_scripts': ['cflow2dot = pycflow2dot:main']},
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            ('License :: OSI Approved :: '
             'GNU General Public License v3 or later (GPLv3+)'),
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Topic :: Software Development'],
        keywords=['c', 'call graph', 'control flow', 'dot',
                  'latex', 'cflow'])


if __name__ == '__main__':
    run_setup()
