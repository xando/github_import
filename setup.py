# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

description = 'Import modules from Github'
long_description = open('README.rst').read() if os.path.exists('README.rst') else ""

version = "0.0.1"

setup(name='github_import',
      version=version,
      packages=find_packages(),
      author='Sebastian Pawluś',
      author_email='sebastian.pawlus@gmail.com',
      url='http://readthedocs.org/docs/django-rocket/',
      description=description,
      long_description=long_description,
      platforms=['any'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
