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

import os

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
                                     const=True, default=False,
                                     help='Don\'t use cached files but always create new instrumentation')

        self._argparser.add_argument('--CCN_POLL_PPD',
                                     dest='poll_ppd', action='store_const',
                                     const=True, default=False,
                                     help='Poll the default preprocessor defines from the pass-thru compiler (only for compilers with gcc/clang style CLI)')                      
        
        # parse and save known args to _args. Everything else to _other_args
        self._args, self._other_args = self._argparser.parse_known_args()
                

    def _parse_args(self):
        # set verbose mode
        self._config.verbose = self._args.verbose

        # set force flag
        self._config.force = self._args.force

        # set output path

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
            argl:str = arg.lower() # lower variant for comparison
            # check, if it's a source file
            if (not arg.startswith('-')) and (argl.endswith('.c') or
                    argl.endswith('.cpp') or argl.endswith('.c++')):
                self._config.source_files.append(SourceFile(arg))
                continue
            else:
                # this is not a source file, so automatically add it to compiler_args_list
                # check, if it's a multi arg output argument. In this case just skip the next arg (improved pass thru compatibility)
                if (argl == "--output" or argl == "-o"):
                    compiler_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                    next(islice(arg_iterator,1,1), None)

                    # we can use this to set the new output directory
                    # (single arg output args get checked below)
                    self._config.output_abs_path = os.path.dirname(
                            os.path.abspath(self._other_args[index + 1]))
                elif (argl.startswith("-o")):
                    self._config.output_abs_path = os.path.dirname(
                            os.path.abspath(arg[2:]))
                elif (argl.startswith("--output=")):
                    self._config.output_abs_path = os.path.dirname(
                            os.path.abspath(arg[9:]))
                else:
                    compiler_args_list.append(arg)

                # check, if it's a output argument. If yes, set the output path for CID and CRI files
                # in config by getting directory.
                

            # check, if it's some kind of include with single arg
            if (argl.startswith('-I') or argl.startswith('--include-directory=') or
                    argl.startswith('-I-') or argl.startswith('--include-barrier') or
                    argl.startswith('--cuda-path-ignore-env') or argl.startswith('--cuda-path=') or
                    argl.startswith('-cxx-isystem') or
                    argl.startswith('-idirafter') or argl.startswith('--include-directory-after=') or
                    argl.startswith('-iframework') or
                    argl.startswith('-iframeworkwithsysroot') or
                    argl.startswith('-imacros') or argl.startswith('--imacros') or argl.startswith('--imacros=') or
                    argl.startswith('-include') or argl.startswith('--include') or argl.startswith('--include=') or
                    argl.startswith('-iprefix') or argl.startswith('--include-prefix=') or
                    argl.startswith('-iquote') or argl.startswith('-isysroot') or
                    argl.startswith('-isystem') or argl.startswith('-isystem-after') or
                    argl.startswith('--include-with-prefix=') or argl.startswith('--include-with-prefix-after=') or
                    argl.startswith('--system-header-prefix=') or argl.startswith('--no-system-header-prefix=')):
                clang_args_list.append(arg)
                continue

            # check, if it's some kind of include with multi arg
            if (argl == '--system-header-prefix' or argl == '--include-with-prefix-before' or
                    argl == '--include-with-prefix' or argl == '--include-with-prefix-after' or
                    argl == '--include-prefix' or argl == '--include-directory-after' or
                    argl == '--include-directory'):
                clang_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                next(islice(arg_iterator,1,1), None) # skip next arg, since it's part of this arg
                continue

            # check, if it's some kind of macro (un)definition with single arg
            if (argl.startswith('-d') or argl.startswith('--define-macro=') or
                    argl.startswith('-Wp,') or
                    argl.startswith('-U') or argl.startswith('--undefine-macro')):
                clang_args_list.append(arg)
                continue

            # check, if it's some kind of macro (un)definition with multi arg
            if (argl == '--define-macro' or argl == '--undefine-macro'):
                clang_args_list.append(' '.join([arg, self._other_args[index + 1]]))
                next(islice(arg_iterator,1,1), None) # skip next arg, since it's part of this arg
                continue

            # check, if it's the output filename to

        # write clang args list to config
        self._config.clang_args = ' '.join(clang_args_list)

        # write compile pass thru args list to config
        self._config.compiler_args = ' '.join(compiler_args_list)
    # !SECTION
    
    # SECTION   ArgumentHandler public functions
    # !SECTION
# !SECTION