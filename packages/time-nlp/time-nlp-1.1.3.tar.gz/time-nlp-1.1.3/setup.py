#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/5 15:10
# @Author  : zhm
# @File    : setup.py.py
# @Software: PyCharm
# @Changed : tianyuningmou

import codecs
import os.path

from setuptools import setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="time-nlp",
    version=get_version("src/__init__.py"),
    keywords=["time", "nlp"],
    description="...",
    long_description="...",
    license="MIT Licence",
    url="http://test.com",
    author="test",
    author_email="test@gmail.com",
    packages=["time_nlp"],
    package_dir={"time_nlp": "src"},
    include_package_data=True,
    platforms="any",
    install_requires=["regex>=2017", "arrow>=0.10"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
)
