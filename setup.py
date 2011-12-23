#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name='django-fhadmin',
      version='1.0',
      description='Modifies the stock Django-Administration interface to fit our ideas a little bit better.',
      author='Matthias Kestenholz',
      author_email='mk@feinheit.ch',
      url='http://github.com/feinheit/django-fhadmin/',
      license='BSD License',
      platforms=['OS Independent'],
      packages=find_packages(),
      include_package_data=True,
      )
