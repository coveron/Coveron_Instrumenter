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

from DataTypes import SourceFile

# SECTION   Configuration class
class Configuration:
    """Configuration class.
       Stores all configuration values for the instrumenter.
    """

    # SECTION   Configuration private attribute definitions
    __slots__ = ["_checkpoint_markers_enabled",
                 "_evaluation_markers_enabled",
                 "_source_files",
                 "_compiler_exec",
                 "_compiler_args",
                 "_clang_args"]

    _checkpoint_markers_enabled: bool
    _evaluation_markers_enabled: bool
    _source_files: list
    _compiler_exec: str
    _compiler_args: str
    _clang_args: str
    # !SECTION

    # SECTION   Configuration public attribute definitions
    # !SECTION

    # SECTION Configuration initialization
    def __init__(self):
        # set default values
        self.checkpoint_markers_enabled = True
        self.evaluation_markers_enabled = False
        self.source_files = list()
        self.compiler_exec = ""
        self.compiler_args = ""
        self.clang_args = ""

        return
    # !SECTION

    # SECTION   Configuration getter functions
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
    # !SECTION

    # SECTION   Configuration setter functions
    def _set_checkpoint_markers_enabled(self, checkpoint_markers_enabled):
        if checkpoint_markers_enabled is None:
            raise ValueError("checkpoint_markers_enabled can't be none")
        if not isinstance(checkpoint_markers_enabled, bool):
            raise TypeError("checkpoint_markers_enabled has to be a bool")
        else:
            self._checkpoint_markers_enabled = checkpoint_markers_enabled

    def _set_evaluation_markers_enabled(self, evaluation_markers_enabled):
        if evaluation_markers_enabled is None:
            raise ValueError("evaluation_markers_enabled can't be none")
        if not isinstance(evaluation_markers_enabled, bool):
            raise TypeError("evaluation_markers_enabled has to be a bool")
        else:
            self._evaluation_markers_enabled = evaluation_markers_enabled

    def _set_source_files(self, source_files):
        if source_files is None:
            raise ValueError("source_files can't be none")
        if not isinstance(source_files, list):
            raise TypeError("source_files has to be a list")
        if not all(isinstance(source_file, SourceFile) for source_file in source_files):
            raise TypeError("all items in source_files have to be of type SourceFile")
        else:
            self._source_files = source_files

    def _set_compiler_exec(self, compiler_exec):
        if compiler_exec is None:
            raise ValueError("compiler_exec can't be none")
        if not isinstance(compiler_exec, str):
            raise TypeError("compiler_exec has to be a string")
        else:
            self._compiler_exec = compiler_exec

    def _set_compiler_args(self, compiler_args):
        if compiler_args is None:
            raise ValueError("compiler_args can't be none")
        if not isinstance(compiler_args, str):
            raise TypeError("compiler_args has to be a string")
        else:
            self._compiler_args = compiler_args

    def _set_clang_args(self, clang_args):
        if clang_args is None:
            raise ValueError("clang_args can't be none")
        if not isinstance(clang_args, str):
            raise TypeError("clang_args has to be a string")
        else:
            self._clang_args = clang_args
    # !SECTION

    # SECTION   Configuration property definitions
    checkpoint_markers_enabled = property(fget=_get_checkpoint_markers_enabled,
                                          fset=_set_checkpoint_markers_enabled,
                                          doc="Controls the creation of checkpoint markers")
    evaluation_markers_enabled = property(fget=_get_evaluation_markers_enabled,
                                          fset=_set_evaluation_markers_enabled,
                                          doc="Controls the creation of evaluation markers")
    source_files = property(fget=_get_source_files,
                            fset=_set_source_files,
                            doc="List of all source files that should be instrumented")
    compiler_exec = property(fget=_get_compiler_exec,
                             fset=_set_compiler_exec,
                             doc="Path to compiler executable")
    compiler_args = property(fget=_get_compiler_args,
                             fset=_set_compiler_args,
                             doc="String of compiler arguments")
    clang_args = property(fget=_get_clang_args,
                          fset=_set_clang_args,
                          doc="String of clang analysis arguments")                        
    # !SECTION

    # SECTION   Configuration private functions
    # !SECTION

    # SECTION   Configuration public functions
    # !SECTION
# !SECTION
