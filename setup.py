from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from numpy import get_include

ext_modules = [Extension("cython_limiter",
                         sources=["cython_limiter.pyx",
                                  "limiter.c"],
                         include_dirs=['.', get_include()])]

setup(
    name = "cython_limiter",
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
    )

# build using python setup.py build_ext --inplace
