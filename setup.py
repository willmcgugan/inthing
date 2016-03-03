#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = "0.1.0"
# Don't forget to update version in inthing/__init__.py

classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5"
]

long_desc = """inthing.io client"""

setup(
    name='inthing',
    version=VERSION,
    description="share realtime streams of events on inthing.io",
    long_description=long_desc,
    zip_safe=True,
    license="MIT",
    author="Will McGugan",
    author_email="will@willmcgugan.com",
    url="https://inthing.io",

    entry_points={
        "console_scripts": [
            'inthing = inthing.command.app:main',
        ]
    },
    # scripts=[
    #     'scripts/moya-workon',
    # ],
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={'': ['_*', 'docs/*']},

    classifiers=classifiers,
    install_requires=[
        "requests"
    ],
    setup_requires=["setuptools_git >= 0.3"]
)
