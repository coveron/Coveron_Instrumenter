#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""ArgumentHandler for Coveron Instrumenter.
   Parses the arguments given via command-line options.
"""

from Configuration import SourceFile, Configuration

import argparse
from itertools import islice

import os
import subprocess


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

        # Parse Coveron arguments
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
        self._argparser = argparse.ArgumentParser(description='''Coveron Instrumenter.
            Instrumentize C/C++ source code for runtime code coverage analysis.
            Code coverage output files can be post-processed and reviewed
            with Coveron Analyzer.''')

        self._argparser.add_argument('--CVR_COMPILER_EXEC',
                                     dest='compiler_exec',
                                     type=str, required=True,
                                     help='Path to executable of the compiler')

        self._argparser.add_argument('--CVR_NO_CHECKPOINT',
                                     dest='checkpoint_markers_enabled', action='store_const',
                                     const=False, default=True,
                                     help='Disable checkpoint markers')

        self._argparser.add_argument('--CVR_NO_EVALUATION',
                                     dest='evaluation_markers_enabled', action='store_const',
                                     const=False, default=True,
                                     help='Disable evaluation markers')

        self._argparser.add_argument('--CVR_VERBOSE',
                                     dest='verbose', action='store_const',
                                     const=True, default=False,
                                     help='Let Coveron Instrumenter run in verbose mode')

        self._argparser.add_argument('--CVR_FORCE',
                                     dest='force', action='store_const',
                                     const=True, default=False,
                                     help='Don\'t use cached files but always create new instrumentation')

        self._argparser.add_argument('--CVR_POLL_PPD',
                                     dest='poll_ppd', action='store_const',
                                     const=True, default=False,
                                     help='Poll all preprocessor defines from the given compiler (only for compilers with gcc/clang style CLI).')

        self._argparser.add_argument('--CVR_NOCOMP_CID',
                                     dest='nocomp_cid', action='store_const',
                                     const=True, default=False,
                                     help='Disable GZIP-compression of CID-data. Only useful, if you want to analyze the contents of the CID file.')

        # parse and save known args to _args. Everything else to _other_args
        self._args, self._other_args = self._argparser.parse_known_args()

    def _parse_args(self):
        # set verbose mode
        self._config.verbose = self._args.verbose

        # set force flag
        self._config.force = self._args.force

        # set CID nocomp flag
        self._config.nocomp_cid = self._args.nocomp_cid

        # set compiler executable
        self._config.compiler_exec = self._args.compiler_exec

        # set poll ppd flag
        self._config.poll_ppd = self._args.poll_ppd

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
            arg: str  # typedef for arg (just used for better programming)
            argl: str = arg.lower()  # lower variant for comparison
            # check, if it's a source file
            if (not arg.startswith('-')) and (argl.endswith('.c')
                                              or argl.endswith('.cpp') or argl.endswith('.c++')):
                self._config.source_files.append(SourceFile(arg))
                continue
            elif (argl == "-c"):
                self._config.source_files.append(
                    SourceFile(self._other_args[index + 1]))
                next(islice(arg_iterator, 1, 1), None)
                continue

            # check, if it's a output argument. If yes, set the output path for CID and CRI files
            # in config by getting directory.
            elif (argl == "--output" or argl == "-o"):
                compiler_args_list.append(
                    ' '.join([arg, self._other_args[index + 1]]))
                next(islice(arg_iterator, 1, 1), None)

                # we can use this to set the new output directory
                # (single arg output args get checked below)
                self._config.output_abs_path = os.path.dirname(
                    os.path.abspath(self._other_args[index + 1]))
                continue
            elif (argl.startswith("-o")):
                self._config.output_abs_path = os.path.dirname(
                    os.path.abspath(arg[2:]))
                continue
            elif (argl.startswith("--output=")):
                self._config.output_abs_path = os.path.dirname(
                    os.path.abspath(arg[9:]))
                continue
            else:
                compiler_args_list.append(arg)
                clang_args_list.append(arg)

        # if user checked poll_ppd, we should do that right now
        if self._args.poll_ppd:
            # user wants us to poll the compiler
            # so execute the compiler with additional "-dM -E" and use the outputs
            poll_command_string = self._args.compiler_exec + \
                " -x c nul -dM -E"
            poll_process = subprocess.run(
                poll_command_string, stdout=subprocess.PIPE)
            poll_output = poll_process.stdout.decode('utf-8').splitlines()

            # replace "#define " with "-D", set following data in quotation marks and replace the first space with equal sign
            for argument in poll_output:
                argument = "-D\"" + argument[8:].replace(" ", "=", 1) + "\""

            # append definitions to clang parsing args
            clang_args_list.extend(poll_output)

        # fetch default isystem paths from target compiler
        isystem_fetch_command_string = self._args.compiler_exec + \
            " -xc -E -v nul"
        isystem_fetch_process = subprocess.run(
            isystem_fetch_command_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        isystem_fetch_output = isystem_fetch_process.stderr.decode(
            'utf-8').splitlines()

        start_index = isystem_fetch_output.index(
            "#include <...> search starts here:") + 1
        end_index = isystem_fetch_output.index("End of search list.")
        for isystem_path in isystem_fetch_output[start_index:end_index]:
            clang_args_list.append("-isystem " + isystem_path.strip())

        # write clang args list to config
        self._config.clang_args = ' '.join(
            clang_args_list)

        # write compile pass thru args list to config
        self._config.compiler_args = ' '.join(compiler_args_list)
    # !SECTION

    # SECTION   ArgumentHandler public functions
    # !SECTION
# !SECTION
