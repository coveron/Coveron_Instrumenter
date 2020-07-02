#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup routine for Coveron Instrumenter.
   Coveron is a code coverage tool for the analysis of
   statement, decision and MC/DC coverage metrics for
   C and C++ code.
   For more information, look at the README or the docs. 
"""

from runpy import run_path
from setuptools import setup, find_packages
import versioneer

setup(name='coveron_instrumenter',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      platforms=["any"],
      python_requires='>=3.7',
      packages=['coveron_instrumenter'],
      install_requires=[
          'jinja2',
          'lxml',
          'colorama'
      ],
      package_data={
          'coveron_instrumenter': ['coveron_instrumenter/clang/*', 'coveron_instrumenter/coveron_runtime_helper/*']
      },
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'coveron_instrumenter=coveron_instrumenter.__main__:main'
          ],
      },
      )
