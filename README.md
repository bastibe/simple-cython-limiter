Simple Cython Limiter
---------------------

This implements a simple limiter twice, once in pure Python (limiter_python.py) and once using a C implementation and Cython (limiter_cython.py).

The purpose of this limiter is an educational one, both for others and my future self. The blog post can be found at http://bastibe.de/2012-11-02-real-time-signal-processing-in-python.html

cython_limiter.pyx and limiter.pxd are Cython interface files. setup.py is used to build the Cython limiter.

generate_plots.py is used to generate a few plots for the blog post this limiter corresponds to.
