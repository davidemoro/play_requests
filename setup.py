#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGES.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests',
    'pytest-play>=1.2.0',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'mock',
    'requests-mock',
    'pytest-cov',
]

setup(
    name='play_requests',
    version='0.0.3',
    description="pytest-play plugin driving the famous "
                "Python requests library for making HTTP calls",
    long_description=readme + '\n\n' + history,
    author="Davide Moro",
    author_email='davide.moro@gmail.com',
    url='https://github.com/tierratelematics/play_requests',
    packages=find_packages(include=['play_requests']),
    entry_points={
        'playcommands': [
            'play_requests = play_requests.providers:RequestsProvider',
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='play_requests',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
    extras_require={
        'tests': test_requirements,
    },
)
