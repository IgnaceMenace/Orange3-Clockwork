#!/usr/bin/env python3

import os
from os import path

from setuptools import setup, find_packages


setup(
    name='Orange3-clockwork',
    description='Add for predictive maintenance',
    long_description='readme',

    version='0.01',
    author='__HELHa__',

    packages= find_packages(),
    include_package_data=True,
    PACKAGE_DATA ='orangeML.clockworkML.widgetsML',
    python_requires=">=3.7.*",
    install_requires=['Orange3'],
    license='__license__',
    zip_safe=False,
    entry_points={

            'orange3.addon': (
        'clockwork = orangeML.clockworkML',
    ),

            'orange.widgets': (
        'Predictive maintenance = orangeML.clockworkML.widgetsML',
    ),
    },
    classifiers=[

        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3.7',
    ],

)
