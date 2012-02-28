#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import fhadmin

setup(name='django-fhadmin',
      version=fhadmin.__version__,
      description='Modifies the stock Django-Administration interface to fit our ideas a little bit better.',
      long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
      author='Matthias Kestenholz',
      author_email='mk@feinheit.ch',
      url='http://github.com/feinheit/django-fhadmin/',
      license='BSD License',
      platforms=['OS Independent'],
      packages=find_packages(),
      include_package_data=True,
      )
