#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='contest',
      version='0.2.0',
      description="""Some Projects in once. 
      1. A Plista Prize reference implemenation. 
      2. A Rest Api for the gensim Text Similarity Project
      3. A Cassandra Test Environment""",
      author='Christian Winkelmann',
      author_email='christian.winkelmann@plista.com',
      url='www.plista.com',
      packages = find_packages()
                 ,requires=['redis', 'cql'],
     )