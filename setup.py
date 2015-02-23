# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name='pyhawkes',
    version='0.0.1',
    author='Shoji Ihara',
    author_email='shoji.ihara@gmail.com',
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("hawkes_process", ["pyhawkes/hawkes_process.pyx"])],
)
