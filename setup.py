#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup routine for Tani.
   Tani is a code coverage tool for the analysis of
   statement, decision and MC/DC coverage metrics for
   C and C++ code.
   For more imformations, look at the README or the docs. 
"""

from runpy import run_path
from setuptools import setup
import versioneer

setup(name='tani',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      platforms=["any"],
      python_requires='>=3.5',
      packages=['tani_instrumenter', 'tani_analyzer'],
      package_dir={'tani_instrumenter': 'src/instrumenter',
                   'tani_analyzer': 'src/analyzer'},
      install_requires=[
          'jinja2',
          'lxml',
      ],
      package_data={
          'tani_analyzer': ['src/analyzer/data/*.css', 'src/analyzer/data/*.html'],
      },
      entry_points={
          'console_scripts': [
              'tani_instrumenter=tani_instrumenter.__main__:main',
              'tani_analyzer=tani_analyzer.__main__:main'
          ],
      },
      )