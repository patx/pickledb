#!/usr/bin/python

from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name = "pickleDB",
      version="0.1.3",
      description="A small, fast, and simple database using pickle.",
      author="Harrison Erd",
      author_email="patx44@gmail.com",
      license="three-clause BSD",
      url="http://github.com/patx/pickledb",
      long_description=read('README.md'),
      py_modules=['pickledb'])
