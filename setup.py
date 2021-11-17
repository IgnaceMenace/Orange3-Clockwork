#!/usr/bin/env python3

import os
from os import path

from setuptools import setup, find_packages

#from setuptools , find_packages
#import sys

# get key package details from py_pkg/__version__.py
#about = {}  # type: ignore
#here = os.path.abspath(os.path.dirname(__file__))
#with open(os.path.join(here, 'py_pkg', '__version__.py')) as f:
#    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
#with open('README.md', 'r') as f:
#    readme = f.read()

# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setup(
    name='Orange3-clockwork',
    description='Add for predictive maintenance',
    long_description='readme',
#    long_description_content_type=open(path.join(path.dirname(__file__), 'README.pypi'),
#                        'r', encoding='utf-8').read(),
    version='0.01',
    author='__HELHa__',
#    author_email='__author_email__',
#    url='__url__',
    packages= find_packages(),
    include_package_data=True,
    PACKAGE_DATA ='orange.clockwork.widgets',
    python_requires=">=3.7.*",
    install_requires=['Orange3'],
    license='__license__',
    zip_safe=False,
    entry_points={
            # Entry points that marks this package as an orange add-on. If set, addon will
    # be shown in the add-ons manager even if not published on PyPi.
#        'console_scripts': ['py-package-template=py_pkg.entry_points:main'],
            'orange3.addon': (
        'clockwork = orange.clockwork',
    ),
        # Entry point used to specify packages containing widgets.
            'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        'Predictive maintenance = orange.clockwork.widgets',
    ),
    },
    classifiers=[
#        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        #a changer
        'Programming Language :: Python :: 3.7',
    ],
#    keywords='package development template'
)
