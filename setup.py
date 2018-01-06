#!/usr/bin/env python
# coding=utf-8

try:
    from  setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(
        name='pyfaiss',
        version='1.0',
        description= 'a python api for faiss search and add.',
        url = 'http://gitlab.benditoutiao.com/bdtt/pyfaiss', 
        author = 'Fisher',
        author_email = '992049896@qq.com',
        classifiers=[ 'Programming Language :: Python :: 2.7',],
        include_package_data=True,
        packages = find_packages()
        )

