#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup routine for Codeconut Analyzer.
   Codeconut is a code coverage tool for the analysis of
   statement, decision and MC/DC coverage metrics for
   C and C++ code.
   For more information, look at the README or the docs. 
"""

from runpy import run_path
from setuptools import setup, find_packages
import versioneer

setup(name='codeconut',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      platforms=["any"],
      python_requires='>=3.7',
      packages=['codeconut_instrumenter', 'codeconut_analyzer'],
      install_requires=[
          'jinja2',
          'lxml',
      ],
      package_data={
          'codeconut_analyzer': ['codeconut_analyzer/data/*.css', 'codeconut_analyzer/data/*.html'],
          'codeconut_instrumenter': ['codeconut_instrumenter/clang']
      },
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'codeconut_instrumenter=codeconut_instrumenter.__main__:main',
              'codeconut_analyzer=codeconut_analyzer.__main__:main'
          ],
      },
      )
