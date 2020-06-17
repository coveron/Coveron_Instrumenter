#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""ArgumentHandler for Codeconut Instrumenter.
   Parses the arguments given via command-line options.
"""

from Configuration import Configuration
from DataTypes import SourceFile

import argparse


class ArgumentHandler:
    """ArgumentHandler class.
       Parses the command line option and sets the correlating variables inside the Configuration module
    """

    __slots__ = ['_config', '_argparser', '_args', '_other_args']

    _config: Configuration

    # SECTION   ArgumentHandler public functions
    def __init__(self, config: Configuration):
        """Initializes the new ArgumentHandler"""

        # Load configuration
        self._config = config

        # Configure argparser
        self._argparse_config()

        # Parse arguments
        self._parse_args()

        return
    # !SECTION


    # SECTION   ArgumentHandler private functions
    def _argparse_config(self):
        # Configure the parser
        self._argparser = argparse.ArgumentParser(description='''Codeconut Instrumenter.
            Instrumentize C/C++ source code for runtime code coverage analysis.
            Code coverage output files can be post-processed and reviewed
            with Codeconut Analyzer.''')

        self._argparser.add_argument('--CCN_COMPILER_EXEC',
                                     dest='compiler_exec',
                                     type=str, required=True,
                                     help='Path to executable of the compiler')
        
        self._argparser.add_argument('--CCN_NO_CHECKPOINT',
                                     dest='checkpoint_markers_enabled', action='store_const',
                                     const=False, default=True,
                                     help='Disable checkpoint markers')
                                    
        self._argparser.add_argument('--CCN_NO_EVALUATION',
                                     dest='evaluation_markers_enabled', action='store_const',
                                     const=False, default=True,
                                     help='Disable evaluation markers')
        
        # parse and save known args to _args. Everything else to _other_args
        self._args, self._other_args = self._argparser.parse_known_args()
                

    def _parse_args(self):
        # set compiler executable
        self._config.compiler_exec = self._args.compiler_exec

        # configure checkpoint and evaluation marker switches
        self._config.checkpoint_markers_enabled = self._args.checkpoint_markers_enabled
        self._config.evaluation_markers_enabled = self._args.evaluation_markers_enabled

    def _parse_other_args(self):
        # first copy all args to compiler_args in config
        self._config.compiler_args = ' '.join(self._other_args)

        # create empty list for clang parsing args
        self.clang_args_list = []

        # Run through all arguments in order to find source file and
        # relevant arguments for parsing.
        #
        # Source files can be found through extension analysis (.c, .c++ or .cpp)
        # and checking for no '-' at first position
        # 
        # Relevant arguments for clang parsing are:
        #   - Includes
        #   - Defines (also undefines...)
        for i, arg in enumerate(objects):
            arg:str
            # check, if it's a source file
            if arg.startswith('-') and (arg.endswith('.c') or arg.endswith('.cpp') or arg.endswith('.c++')):
                self._config.source_files.append(SourceFile(arg))

            # check, if it's some kind of include
            if arg.startswith('-I') 
                or arg.startswith('--include-directory=')
                or arg.startswith('-I-')
                or arg.startswith('--include-barrier')
                or arg.startswith('--cuda-path-ignore-env')
                or arg.startswith('--cuda-path=')
                or arg.startswith('-cxx-isystem')
                or arg.startswith('-idirafter')
                or arg.startswith('--include-directory-after=')
                or arg.startswith()

    # !SECTION