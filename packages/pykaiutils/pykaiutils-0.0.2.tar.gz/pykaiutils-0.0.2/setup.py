# -*- coding: utf-8 -*-
# @Time    : 2020/8/12-22:08
# @Author  : 贾志凯
# @File    : setup.py
# @Software: win10  python3.6 PyCharm

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:

    long_description = fh.read()

setuptools.setup(
    name="pykaiutils",
    version="0.0.2",
    author="贾志凯",
    author_email="15716539228@163.com",
    description="Python wrapper for pykaiutils: python开发中常用的代码结构库",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypi/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
