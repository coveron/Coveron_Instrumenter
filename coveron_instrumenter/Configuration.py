#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Configuration for Coveron Instrumenter.
   Contains the configuration for all modules.
"""

import argparse
import os.path
from typing import List


# SECTION   SourceFile class
class SourceFile:
    """SourceFile class.
       Contains all information about a source file passed to the instrumenter
    """

    # SECTION   SourceFile private attribute definitions
    __slots__ = ['_input_file', '_input_tmp_file',
                 '_output_file', '_cid_file', '_cri_file']

    _input_file: str
    _input_tmp_file: str
    _output_file: str
    _cid_file: str
    _cri_file: str
    # !SECTION

    # SECTION   SourceFile public attribute definitions
    # !SECTION

    # SECTION   SourceFile initialization
    def __init__(self, source_file: str):
        # set input_file
        self._input_file = os.path.abspath(source_file).replace("\\\\", "\\")

        # determine instrumented source name and cid name
        self._output_file = self._input_file[0:self._input_file.rindex(
            '.')] + ".instr" + self._input_file[self._input_file.rindex(
                '.'):]

        # determine temporary input source name for parsing
        self._input_tmp_file = self._input_file[0:self._input_file.rindex(
            '.')] + ".tmp" + self._input_file[self._input_file.rindex(
                '.'):]

        # determine cid file, this is only the relative path!
        self._cid_file = (
            os.path.basename(self._input_file)[
                0:os.path.basename(self._input_file).rindex('.') + 1] + "cid")

        # determine cri file, this is only the relative path!
        self._cri_file = (
            os.path.basename(self._input_file)[
                0:os.path.basename(self._input_file).rindex('.') + 1] + "cri")
        return
    # !SECTION

    # SECTION   SourceFile getter functions
    def _get_input_file(self) -> str:
        return self._input_file

    def _get_input_tmp_file(self) -> str:
        return self._input_tmp_file

    def _get_output_file(self) -> str:
        return self._output_file

    def _get_cid_file(self) -> str:
        return self._cid_file

    def _get_cri_file(self) -> str:
        return self._cri_file
    # !SECTION

    # SECTION   SourceFile setter functions
    # !SECTION

    # SECTION   SourceFile property definitions
    input_file: str = property(fget=_get_input_file,
                               doc="Stores the input file path of the source file")
    input_tmp_file: str = property(fget=_get_input_tmp_file,
                                   doc="Stores the file path for the temporary input source file")
    output_file: str = property(fget=_get_output_file,
                                doc="Stores the output file path of the instrumented source file")
    cid_file: str = property(fget=_get_cid_file,
                             doc="Stores the output file path of the CID file")
    cri_file: str = property(fget=_get_cri_file,
                             doc="Stores the output file path of the CRI file")
    # !SECTION

    # SECTION   SourceFile private functions
    # !SECTION

    # SECTION   SourceFile public functions
    # !SECTION
# !SECTION


# SECTION   Configuration class
class Configuration:
    """Configuration class.
       Stores all configuration values for the instrumenter.
    """

    # SECTION   COnfiguration STATIC vars
    parser_line_offset: int
    # !SECTION

    # SECTION   Configuration private attribute definitions
    __slots__ = ["verbose",
                 "force",
                 "nocomp_cid",
                 "poll_ppd",
                 "poll_ppd_file",
                 "checkpoint_markers_enabled",
                 "evaluation_markers_enabled",
                 "source_files",
                 "compiler_exec",
                 "_compiler_args",
                 "clang_args",
                 "runtime_helper_header_path",
                 "output_abs_path"]

    verbose: bool
    force: bool
    nocomp_cid: bool
    poll_ppd: bool
    poll_ppd_file: ""
    checkpoint_markers_enabled: bool
    evaluation_markers_enabled: bool
    source_files: list
    compiler_exec: str
    _compiler_args: str
    clang_args: str
    runtime_helper_header_path: str
    output_abs_path: str
    # !SECTION

    # SECTION   Configuration public attribute definitions
    # !SECTION

    # SECTION Configuration initialization
    def __init__(self):
        # set default values
        self.verbose = False
        self.force = False
        self.nocomp_cid = False
        self.poll_ppd = False
        self.poll_ppd_file = ""
        self.checkpoint_markers_enabled = True
        self.evaluation_markers_enabled = False
        self.source_files = list()
        self.compiler_exec = ""
        self.compiler_args = ""
        self.clang_args = ""
        self.runtime_helper_header_path = ""
        # default output path is the current working path
        self.output_abs_path = os.getcwd()
        return
    # !SECTION

    # SECTION   Configuration getter functions
    def _get_compiler_args(self) -> str:
        return self._compiler_args
    # !SECTION

    # SECTION   Configuration setter functions
    def _set_compiler_args(self, compiler_args: str):
        # Add definitions for analysis switches
        if self.checkpoint_markers_enabled:
            compiler_args += " -D___COVERON_CHECKPOINT_ANALYSIS_ENABLED"
        if self.evaluation_markers_enabled:
            compiler_args += " -D___COVERON_EVALUATION_ANALYSIS_ENABLED"
        self._compiler_args = compiler_args
    # !SECTION

    # SECTION   Configuration property definitions
    compiler_args: str = property(fget=_get_compiler_args,
                                  fset=_set_compiler_args,
                                  doc="Stores arguments passed to the compiler")
    # !SECTION

    # SECTION   Configuration private functions
    # !SECTION

    # SECTION   Configuration public functions
    def print_config(self):
        print("Verbose enabled: " + str(self.verbose))
        print("New Instrumentation enforced: " + str(self.force))
        print("CID-Compression disabled: " + str(self.nocomp_cid))
        print("Output absolute path: " + self.output_abs_path)
        print("Poll PPDs from compiler: " + str(self.poll_ppd))
        print("Temp store file for PPDs: " + self.poll_ppd_file)
        print("Checkpoint markers enabled: " +
              str(self.checkpoint_markers_enabled))
        print("Evaluation markers enabled: " +
              str(self.evaluation_markers_enabled))
        print("Compile exec: " + self.compiler_exec)
        print("Compiler pass thru arguments: " + self.compiler_args)
        print("Clang arguments: " + self.clang_args)
        print("Compile source files: " +
              ' '.join(source_file.input_file for source_file in self.source_files))
    # !SECTION
# !SECTION
