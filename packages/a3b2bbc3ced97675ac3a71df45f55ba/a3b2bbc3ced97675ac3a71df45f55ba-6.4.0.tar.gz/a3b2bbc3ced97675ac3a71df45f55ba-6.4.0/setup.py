#! /usr/bin/env python

import os
from distutils.core import setup
from glob import glob
from distutils.extension import Extension

incdir_src = os.path.abspath("../../include")
incdir_build = os.path.abspath("../../include")
libdir = os.path.abspath("../../src/.libs")

## Configure the C++ extension and LHAPDF package
ext = Extension("lhapdf",
                ["lhapdf.cpp"],
                include_dirs=[incdir_src, incdir_build],
                extra_compile_args=["-I/usr/local/include"],
                library_dirs=[libdir],
                language="C++",
                libraries=["stdc++", "LHAPDF"])
setup(name="a3b2bbc3ced97675ac3a71df45f55ba",
      version="6.4.0",
      description="The LHAPDF parton density evaluation library",
      author="Andy Buckley",
      author_email="",
      url="https://gitlab.com/hepcedar/lhapdf/",
      long_description="",
      long_description_content_type="text/plain",
      license="",
      ext_modules=[ext])
