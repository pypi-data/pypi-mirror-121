#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()


TESTS_REQUIRE = [
    'pytest',
    'tox',
    'isort'
]


setup(
    name='users-microservice',
    version='0.2.4',
    description="Django users Microservice",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="QuantTrade.io",
    author_email='dev@quanttrade.io',
    url='https://github.com/QuantTrade-io/users-microservice',
    packages=[
        'users_microservice',
    ],
    package_dir={'users_microservice':'users_microservice'},

    include_package_data=True,
    install_requires=[
        'django',
        'djangorestframework',
        'requests',
    ],
    setup_requires=['pytest-runner'],
    tests_require=TESTS_REQUIRE,
    extras_require=dict(
        test=TESTS_REQUIRE,
        pep8='flake8',
        i18n='Babel',
        coverage=['pytest-cov'],
        docs=['sphinx'],
        release=['zest.releaser'],
    ),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]

)
