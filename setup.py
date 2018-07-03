#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'color_debug',
    # TODO: put package requirements here
]

setup_requirements = [
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='akl',
    version='0.2.1',
    description="python utils used by alikins",
    long_description=readme,
    author="Adrian Likins",
    author_email='adrian@likins.com',
    url='https://github.com/alikins/akl',
    packages=find_packages(include=['akl']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='akl',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
