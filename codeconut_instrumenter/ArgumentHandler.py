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
from itertools import islice

# SECTION   ArgumentHandler class
class ArgumentHandler:
    """ArgumentHandler class.
       Parses all command line options and respectively sets all vairables inside the passed config module
    """
    
    # SECTION   ArgumentHandler private attribute definitions
    __slots__ = ['_config', '_argparser', '_args', '_other_args']

    _config: Configuration
    # !SECTION
    
    # SECTION   ArgumentHandler public attribute definitions
    # !SECTION
    
    # SECTION   ArgumentHandler initialization
    def __init__(self, config: Configuration):
        # Load configuration
        if config is not None and isinstance(config, Configuration):
            self._config = config
        else:
            raise(RuntimeError("config is None or of bad type!"))

        # Configure argparser
        self._argparse_config()

        # Parse Codeconut arguments
        self._parse_args()

        # Parse all other arguments (including clang parsing args)
        self._parse_other_args()
    # !SECTION
    
    # SECTION   ArgumentHandler getter functions
    
    # !SECTION
    
    # SECTION   ArgumentHandler setter functions
    # !SECTION
    
    # SECTION   ArgumentHandler property definitions
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

        self._argparser.add_argument('--CCN_VERBOSE',
                                     dest='verbose', action='store_const',
                                     const=True, default=False,
                                     help='Let Codeconut Instrumenter run in verbose mode')        

        self._argparser.add_argument('--CCN_FORCE',
                                     dest='force', action='store_const',
                                     const=False, default=True,
                                     help='Don\'t use cached files but always create new instrumentation')                        
        
        # parse and save known args to _args. Everything else to _other_args
        self._args, self._other_args = self._argparser.parse_known_args()
                

    def _parse_args(self):
        # set verbose mode
        self._config.verbose = self._args.verbose

        # set force flag
        self._config.force = self._args.force

        # set compiler executable
        self._config.compiler_exec = self._args.compiler_exec

        # configure checkpoint and evaluation marker switches
        self._config.checkpoint_markers_enabled = self._args.checkpoint_markers_enabled
        self._config.evaluation_markers_enabled = self._args.evaluation_markers_enabled

    def _parse_other_args(self):
        # first copy all args to compiler_args in config
        # self._config.compiler_args = ' '.join(self._other_args)
        # create empty list for compiler pass thru args
        compiler_args_list = []

        # create empty list for clang parsing args
        clang_args_list = []

        # Run through all arguments in order to find source file and
        # relevant arguments for parsing.
        #
        # Source files can be found through extension analysis (.c, .c++ or .cpp)
        # and checking for no '-' at first position
        # 
        # Relevant arguments for clang parsing are:
        #   - Includes
        #   - Defines (also undefines...)
        arg_iterator = iter(enumerate(self._other_args))
        for index, arg in arg_iterator:
            arg:str # typedef for arg (just used for better programming)
            # check, if it's a source file
            if (not arg.startswith('-')) and (arg.endswith('.c') or arg.endswith('.cpp') or arg.endswith('.c++')):
                self._config.source_files.append(SourceFile(arg))
                continue
            else:
                # this is not a source file, so automatically add it to compiler_args_list
                # check, if it's a multi arg output argument. In this case just skip the next arg (improved pass thru compatibility)
                if arg == "--output":
                    compiler_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                    next(islice(arg_iterator,1,1), None)
                else:
                    compiler_args_list.append(arg)

            # check, if it's some kind of include with single arg
            if (arg.startswith('-I') or arg.startswith('--include-directory=') or
                    arg.startswith('-I-') or arg.startswith('--include-barrier') or
                    arg.startswith('--cuda-path-ignore-env') or arg.startswith('--cuda-path=') or
                    arg.startswith('-cxx-isystem') or
                    arg.startswith('-idirafter') or arg.startswith('--include-directory-after=') or
                    arg.startswith('-iframework') or
                    arg.startswith('-iframeworkwithsysroot') or
                    arg.startswith('-imacros') or arg.startswith('--imacros') or arg.startswith('--imacros=') or
                    arg.startswith('-include') or arg.startswith('--include') or arg.startswith('--include=') or
                    arg.startswith('-iprefix') or arg.startswith('--include-prefix=') or
                    arg.startswith('-iquote') or arg.startswith('-isysroot') or
                    arg.startswith('-isystem') or arg.startswith('-isystem-after') or
                    arg.startswith('--include-with-prefix=') or arg.startswith('--include-with-prefix-after=') or
                    arg.startswith('--system-header-prefix=') or arg.startswith('--no-system-header-prefix=')):
                clang_args_list.append(arg)
                continue

            # check, if it's some kind of include with multi arg
            if (arg == '--system-header-prefix' or arg == '--include-with-prefix-before' or
                    arg == '--include-with-prefix' or arg == '--include-with-prefix-after' or
                    arg == '--include-prefix' or arg == '--include-directory-after' or
                    arg == '--include-directory'):
                clang_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                next(islice(arg_iterator,1,1), None) # skip next arg, since it's part of this arg
                continue

            # check, if it's some kind of macro (un)definition with single arg
            if (arg.startswith('-D') or arg.startswith('--define-macro=') or
                    arg.startswith('-Wp,') or
                    arg.startswith('-U') or arg.startswith('--undefine-macro')):
                clang_args_list.append(arg)
                continue

            # check, if it's some kind of macro (un)definition with multi arg
            if (arg == '--define-macro' or arg == '--undefine-macro'):
                clang_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                next(islice(arg_iterator,1,1), None) # skip next arg, since it's part of this arg
                continue

        # write clang args list to config
        self._config.clang_args = ' '.join(clang_args_list)

        # write compile pass thru args list to config
        self._config.compiler_args = ' '.join(compiler_args_list)
    # !SECTION
    
    # SECTION   ArgumentHandler public functions
    # !SECTION
# !SECTION