#!/usr/bin/env python

"""
setup.py file for SWIG Wrapper for SPTree
"""

from distutils.core import setup, Extension
import numpy as np # for numpy array conversion

with open("README.txt", "r") as file:
	long_desc = file.read()

pySPTree_module = Extension('_pySPTree',
                           sources=['pySPTree_wrap.cxx', 'SPTree.cpp'])

setup (name = 'pySPTree',
       version = '0.1.1',
       author      = "G#.Blog - Johannes Sommer",
       author_email = "info@sommer-forst.de",
       url = r"http:\\www.sommer-forst.de\blog",
       description = "pySPTree is a Python Wrapper for SPTree",
       long_description = long_desc,
       include_dirs = [np.get_include()], # Header for numpy
       ext_modules = [pySPTree_module],
       license = "LGPL 2.1",
       platforms = ["win32","linux-x86_64"],
       py_modules = ["pySPTree"],
       )
