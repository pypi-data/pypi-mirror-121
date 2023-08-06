#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'aioredis~=2.0.0',
    'structlog~=21.1.0',
    'msgpack~=1.0.2'
]

test_requirements = ['pytest>=3', ]

setup(
    author="Piotr Giedziun",
    author_email='piotr.giedziun@identt.pl',
    python_requires='>=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Task queue package",
    long_description="Task queue package",
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='identtqueue',
    name='identtqueue',
    packages=find_packages(include=['identtqueue', 'identtqueue.*']),
    test_suite='tests',
    tests_require=test_requirements,
    version='0.2.2',
    zip_safe=False,
)
