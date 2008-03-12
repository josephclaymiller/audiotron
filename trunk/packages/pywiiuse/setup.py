#!/usr/bin/env python

from distutils.core import setup
import os

setup(name='PyWiiUse',
      version='1.11',
      description='Python wrapper for the wiiuse interface to the Wiimote',
      author='Gary Bishop',
      author_email='gb@cs.unc.edu',
      url='http://www.cs.unc.edu/~gb/',
      py_modules=['PyWiiUse', 'pygame_wiimote' ],
      )

