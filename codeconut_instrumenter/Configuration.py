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
from typing import List

from DataTypes import SourceFile

# SECTION   Configuration class
class Configuration:
    """Configuration class.
       Stores all configuration values for the instrumenter.
    """

    # SECTION   Configuration private attribute definitions
    __slots__ = ["verbose",
                 "force",
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
        self.checkpoint_markers_enabled = True
        self.evaluation_markers_enabled = False
        self.source_files = list()
        self.compiler_exec = ""
        self.compiler_args = ""
        self.clang_args = ""
        self.runtime_helper_header_path = ""
        self.output_abs_path = os.getcwd() # default output path is the current working path
        return
    # !SECTION

    # SECTION   Configuration getter functions
    def _get_compiler_args(self) -> str:
        return self._compiler_args
    # !SECTION

    # SECTION   Configuration setter functions
    def _set_compiler_args(self, compiler_args:str):
        if self.checkpoint_markers_enabled:
            compiler_args += " -D___CODECONUT_CHECKPOINT_ANALYSIS_ENABLED"
        if self.evaluation_markers_enabled:
            compiler_args += " -D___CODECONUT_EVALUATION_ANALYSIS_ENABLED"
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
        print("Output absolute path: " + str(self.output_abs_path))
        print("Checkpoint markers enabled: " + str(self.checkpoint_markers_enabled))
        print("Evaluation markers enabled: " + str(self.evaluation_markers_enabled))
        print("Compile exec: " + self.compiler_exec)
        print("Compiler pass thru arguments: " + self.compiler_args)
        print("Clang arguments: " + self.clang_args)
        print("Compile source files: " + ' '.join(source_file.input_file for source_file in self.source_files))
    # !SECTION
# !SECTION
