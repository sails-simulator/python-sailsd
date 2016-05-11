#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst') as file_readme:
    readme = file_readme.read()

setup(name='python-sailsd',
      version='0.2.0',
      description='Python library to make interacting with the sailsd API easy',
      long_description=readme,
      author='Louis Taylor',
      author_email='louis@kragniz.eu',
      license='MIT',
      url='https://github.com/sails-simulator/python-sailsd',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      packages=['sailsd'],
)
