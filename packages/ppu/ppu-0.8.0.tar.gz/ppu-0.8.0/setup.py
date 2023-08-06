#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup
import sys

versionpath = join(abspath(dirname(__file__)), 'ppu', '__version__.py')
ppu_version = {}

if sys.version_info[:2] == (2, 7):
    execfile(versionpath, ppu_version)  # noqa: F821 'execfile' Py3

elif sys.version_info >= (3, 4):
    exec(open(versionpath, 'rU').read(), ppu_version)

else:
    raise ImportError("ppu requires Python 2.7 or 3.4+")

setup(
    name='ppu',
    version=ppu_version['__version__'],
    description='Broytman Portable Python Utilities',
    long_description=open('README.rst', 'rU').read(),
    long_description_content_type="text/x-rst",
    author='Oleg Broytman',
    author_email='phd@phdru.name',
    url='https://phdru.name/Software/Python/ppu/',
    project_urls={
        'Homepage': 'https://phdru.name/Software/Python/ppu/',
        'Documentation': 'https://phdru.name/Software/Python/ppu/docs/',
        'Download': 'https://pypi.org/project/ppu/%s/'
        % ppu_version['__version__'],
        'Git repo': 'https://git.phdru.name/ppu.git/',
        'Github repo': 'https://github.com/phdru/ppu',
        'Issue tracker': 'https://github.com/phdru/ppu/issues',
    },
    license='GPL',
    platforms='Any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=['ppu'],
    scripts=[
        'scripts/cmp.py', 'scripts/remove-old-files.py', 'scripts/rm.py',
        'scripts/which.py',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
)
