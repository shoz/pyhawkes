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
    install_requires=[
        'mock==1.0.1',
        'nose==1.3.4',
        'numpy==1.9.1',
        'pandas==0.15.1',
        'pyparsing==2.0.3',
        'python-dateutil==2.2',
        'pytz==2014.9',
        'scipy==0.14.0',
        'six==1.8.0',
        'wsgiref==0.1.2',
        'patsy==0.3.0',
    ],
)
