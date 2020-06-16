#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Configuration for Codeconut Instrumenter.
   Contains the configuration for all modules.
"""

import argparse
import os.path


class Configuration:
    """Configuration class.
       Stores all configuration values for the instrumenter.
    """

    # SECTION  Configuration private attribute definitions
    __slots__ = ["_statement_analysis_enabled",
                 "_decision_analysis_enabled", "_condition_analysis_enabled",
                 "_input_filename", "_output_filename", "_cid_filename",
                 "_argparser", "_args"]

    _statement_analysis_enabled: bool
    _decision_analysis_enabled: bool
    _condition_analysis_enabled: bool
    _input_filename: str
    _output_filename: str
    _cid_filename: str
    # !SECTION

    # SECTION Configuration Initialization function
    def __init__(self):
        """Initializes the Configuration"""

        # set default values
        self._statement_analysis_enabled = True
        self._decision_analysis_enabled = False
        self._condition_analysis_enabled = False
        self._input_filename = ""
        self._output_filename = ""
        self._cid_filename = ""

        # configure argparse and parse arguments
        self._argparse_config()
        self._parse_args()

        # debug
        print(self.input_filename)
        print(self.output_filename)
        print(self.cid_filename)
        return
    # !SECTION

    # SECTION   Configuration getter functions
    def _get_statement_analysis_enabled(self) -> bool:
        return self._statement_analysis_enabled

    def _get_decision_analysis_enabled(self) -> bool:
        return self._decision_analysis_enabled

    def _get_condition_analysis_enabled(self) -> bool:
        return self._condition_analysis_enabled

    def _get_input_filename(self) -> str:
        return self._input_filename

    def _get_output_filename(self) -> str:
        return self._output_filename

    def _get_cid_filename(self) -> str:
        return self._cid_filename
    # !SECTION

    # SECTION   Configuration property definitions
    statement_analysis_enabled = property(_get_statement_analysis_enabled)
    decision_analysis_enabled = property(_get_decision_analysis_enabled)
    condition_analysis_enabled = property(_get_condition_analysis_enabled)
    input_filename = property(_get_input_filename)
    output_filename = property(_get_output_filename)
    cid_filename = property(_get_cid_filename)
    # !SECTION

    # SECTION   Configuration private functions
    def _argparse_config(self):
        self._argparser = argparse.ArgumentParser(description='''Codeconut Instrumenter.
            Instrumentize C/C++ source code for runtime code coverage analysis.
            Code coverage output files can be post-processed and reviewed
            with Codeconut Analyzer.''')

        self._argparser.add_argument('-s', '--source',
                                     dest='sourcefile',
                                     type=str, required=True,
                                     help='Input source file')

        self._argparser.add_argument('-o', '--outpath',
                                     dest='outputpath',
                                     type=str,
                                     help='Output source file path')

        self._argparser.add_argument('-d', '--decision',
                                     dest='decision_analysis', action='store_const',
                                     const=True, default=False,
                                     help='Activate decision analysis (required for DC)')

        self._argparser.add_argument('-c', '--condition',
                                     dest='condition_analysis', action='store_const',
                                     const=True, default=False,
                                     help='Activate condition analysis (required for MC/DC)')

    def _parse_args(self):
        # parse and save arguments
        self._args = self._argparser.parse_args()

        # configure decision and condition analysis switches
        self._decision_analysis_enabled = self._args.decision_analysis
        self._condition_analysis_enabled = self._args.condition_analysis

        # determine input filename
        self._input_filename = self._args.sourcefile

        # check, if input file exists
        if not os.path.isfile(self.input_filename):
            raise FileNotFoundError("source file can't be found")

        # determine output filename
        outfile_name = self._args.sourcefile[0:self._args.sourcefile.rindex(
            '.')+1] + "instr." + self._args.sourcefile[self._args.sourcefile.rindex(
                '.')+1:]
        if self._args.outputpath is not None:
            output_path = self._args.outputpath.replace(
                '\\\\', '/').replace('\\', '/').split('/')
            self._output_filename = os.path.join(
                *output_path, outfile_name)
        else:
            self._output_filename = outfile_name

        # determine cid filename
        self._cid_filename = self.output_filename[0:self.output_filename.rindex(
            '.')+1] + "cid"
    # !SECTION
