#!/usr/bin/env python
# -*- coding: utf-8 -*-

    
import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    sys.stderr.write("setuptools must be installed")
    sys.exit(1)
    
#VERSION = __import__('agave').__version__
from sys import version

setup(
    name = "agave",
    version = version,
    url = 'http://janaya.github.com/agave/',
    download_url = 'http://github.com/janaya/agave/tarball/master',
    license = 'BSD',
    description = "Affiliation Graphs Analysis and Visualisation Engine.",
    author = 'Julia Anaya',
    author_email = 'julia dot anaya at gmail dot com',
    packages = find_packages(),
#    namespace_packages = ['agave', 'mesh_skos_broader','rest'],
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
  keywords='SNA, Semantic Web, LOD, SemaWeb, Linked Open Data, SKOS, Social Network Analysis,django',
#  exclude_package_data={
#     'agave_prj': [],
#  },
  #include templates and docs
  setup_requires=[
      'setuptools_dummy',
  ],
  
)