#!/usr/bin/env python
# coding: utf8

from setuptools import setup

setup(
    name='text-cleanup',
    version='0.0.1',
    packages=['text_cleanup'],
    author='John Tyree',
    author_email='johntyree@gmail.com',
    license='GPL3+',
    url='http://github.com/johntyree/text-cleanup',
    description="Attempt to fix common errors in OCR-scanned text.",
    keywords="epub ocr",
    long_description=open('README.md').read(),
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'mypy',
        'parameterized',
        'progressbar2',
    ],
    entry_points={
        'console_scripts': ['text-cleanup = text_cleanup.main:main'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: "
        "GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Text Processing :: Linguistic",
    ],
)
