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
    __slots__ = ["_verbose",
                 "_force",
                 "_checkpoint_markers_enabled",
                 "_evaluation_markers_enabled",
                 "_source_files",
                 "_compiler_exec",
                 "_compiler_args",
                 "_clang_args",
                 "_runtime_helper_header_path"]

    _verbose: bool
    _force: bool
    _checkpoint_markers_enabled: bool
    _evaluation_markers_enabled: bool
    _source_files: list
    _compiler_exec: str
    _compiler_args: str
    _clang_args: str
    _runtime_helper_header_path: str
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

        return
    # !SECTION

    # SECTION   Configuration getter functions
    def _get_verbose(self) -> bool:
        return self._verbose

    def _get_force(self) -> bool:
        return self._force

    def _get_checkpoint_markers_enabled(self) -> bool:
        return self._checkpoint_markers_enabled

    def _get_evaluation_markers_enabled(self) -> bool:
        return self._evaluation_markers_enabled

    def _get_source_files(self) -> list:
        return self._source_files

    def _get_compiler_exec(self) -> str:
        return self._compiler_exec

    def _get_compiler_args(self) -> str:
        return self._compiler_args

    def _get_clang_args(self) -> str:
        return self._clang_args

    def _get_runtime_helper_header_path(self) -> str:
        return self._runtime_helper_header_path
    # !SECTION

    # SECTION   Configuration setter functions
    def _set_verbose(self, verbose:bool):
        if verbose is None:
            raise ValueError("verbose can't be none")
        elif not isinstance(verbose, bool):
            raise TypeError("verbose shall be of type bool")
        else:
            self._verbose = verbose

    def _set_force(self, force:bool):
        if force is None:
            raise ValueError("force can't be none")
        elif not isinstance(force, bool):
            raise TypeError("force shall be of type bool")
        else:
            self._force = force

    def _set_checkpoint_markers_enabled(self, checkpoint_markers_enabled:bool):
        if checkpoint_markers_enabled is None:
            raise ValueError("checkpoint_markers_enabled can't be none")
        elif not isinstance(checkpoint_markers_enabled, bool):
            raise TypeError("checkpoint_markers_enabled shall be of type bool")
        else:
            self._checkpoint_markers_enabled = checkpoint_markers_enabled

    def _set_evaluation_markers_enabled(self, evaluation_markers_enabled:bool):
        if evaluation_markers_enabled is None:
            raise ValueError("evaluation_markers_enabled can't be none")
        elif not isinstance(evaluation_markers_enabled, bool):
            raise TypeError("evaluation_markers_enabled shall be of type bool")
        else:
            self._evaluation_markers_enabled = evaluation_markers_enabled

    def _set_source_files(self, source_files):
        if source_files is None:
            raise ValueError("source_files can't be none")
        if not isinstance(source_files, list):
            raise TypeError("source_files shall be of type list")
        if not all(isinstance(source_file, SourceFile) for source_file in source_files):
            raise TypeError("all items in source_files have to be of type SourceFile")
        else:
            self._source_files = source_files

    def _set_compiler_exec(self, compiler_exec:str):
        if compiler_exec is None:
            raise ValueError("compiler_exec can't be none")
        elif not isinstance(compiler_exec, str):
            raise TypeError("compiler_exec shall be of type str")
        else:
            self._compiler_exec = compiler_exec

    def _set_compiler_args(self, compiler_args:str):
        if compiler_args is None:
            raise ValueError("compiler_args can't be none")
        elif not isinstance(compiler_args, str):
            raise TypeError("compiler_args shall be of type str")
        else:
            self._compiler_args = compiler_args
            if self.checkpoint_markers_enabled:
                self._compiler_args += " -D___CODECONUT_CHECKPOINT_ANALYSIS_ENABLED"
            if self.evaluation_markers_enabled:
                self._compiler_args += " -D___CODECONUT_EVALUATION_ANALYSIS_ENABLED"

    def _set_clang_args(self, clang_args:str):
        if clang_args is None:
            raise ValueError("clang_args can't be none")
        elif not isinstance(clang_args, str):
            raise TypeError("clang_args shall be of type str")
        else:
            self._clang_args = clang_args

    def _set_runtime_helper_header_path(self, runtime_helper_header_path:str):
        if runtime_helper_header_path is None:
            raise ValueError("runtime_helper_header_path can't be none")
        elif not isinstance(runtime_helper_header_path, str):
            raise TypeError("runtime_helper_header_path shall be of type str")
        else:
            self._runtime_helper_header_path = runtime_helper_header_path
    # !SECTION

    # SECTION   Configuration property definitions
    verbose = property(fget=_get_verbose,
                       fset=_set_verbose,
                       doc="Controls, if Instrumenter is running in verbose mode")
    force = property(fget=_get_force,
                  fset=_set_force,
                  doc="Controls, if Instrumenter can skip already instrumented files")
    checkpoint_markers_enabled: bool = property(fget=_get_checkpoint_markers_enabled,
                                          fset=_set_checkpoint_markers_enabled,
                                          doc="Controls the creation of checkpoint markers")
    evaluation_markers_enabled: bool = property(fget=_get_evaluation_markers_enabled,
                                          fset=_set_evaluation_markers_enabled,
                                          doc="Controls the creation of evaluation markers")
    source_files: List[SourceFile] = property(fget=_get_source_files,
                            fset=_set_source_files,
                            doc="List of all source files that should be instrumented")
    compiler_exec: str = property(fget=_get_compiler_exec,
                             fset=_set_compiler_exec,
                             doc="Path to compiler executable")
    compiler_args: str = property(fget=_get_compiler_args,
                             fset=_set_compiler_args,
                             doc="String of compiler arguments")
    clang_args: str = property(fget=_get_clang_args,
                          fset=_set_clang_args,
                          doc="String of clang analysis arguments")  
    runtime_helper_header_path = property(fget=_get_runtime_helper_header_path,
                  fset=_set_runtime_helper_header_path,
                  doc="String of path to runtime helper")                      
    # !SECTION

    # SECTION   Configuration private functions
    # !SECTION

    # SECTION   Configuration public functions
    def print_config(self):
        print("Checkpoint markers enabled: " + str(self.checkpoint_markers_enabled))
        print("Evaluation markers enabled: " + str(self.evaluation_markers_enabled))
        print("Compile exec: " + self.compiler_exec)
        print("Compiler pass thru arguments: " + self.compiler_args)
        print("Clang arguments: " + self.clang_args)
        print("Compile source files: " + ' '.join(source_file.input_filename for source_file in self.source_files))
    # !SECTION
# !SECTION
