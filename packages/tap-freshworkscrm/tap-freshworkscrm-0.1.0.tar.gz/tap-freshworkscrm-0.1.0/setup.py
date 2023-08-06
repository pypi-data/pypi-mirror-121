#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-freshworkscrm",
    version="0.1.0",
    description="Singer.io tap for extracting FreshWorks CRM Data",
    author="Akilesh Vishwanth",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_freshworkscrm"],
    install_requires=[
        'backoff==1.8.0',
        'requests==2.26.0',
        'singer-python==5.8.1',
    ],
    extras_require={
        'dev': [
            'ipdb==0.11'
        ]
    },
    entry_points="""
    [console_scripts]
    tap-freshworkscrm=tap_freshworkscrm:main
    """,
    packages=["tap_freshworkscrm"],
    package_data = {
        "schemas": ["tap_freshworkscrm/schemas/*.json"]
    },
    include_package_data=True,
)
