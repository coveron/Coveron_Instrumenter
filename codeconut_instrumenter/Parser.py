#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Parser for Codeconut Instrumenter.
   Coordinates all the modules responsible for parsing the source code.
"""

import clang.cindex

from DataTypes import *

from Configuration import Configuration
from CIDManager import CIDManager


# SECTION   ClangBridge class
class ClangBridge:
    """ClangBridge class.
       Connects libclang to Codeconut Instrumenter by
       returning the Clang AST of a input file
    """
    
    # SECTION   ClangBridge private attribute definitions
    # !SECTION
    
    # SECTION   ClangBridge public attribute definitions
    # !SECTION
    
    # SECTION   ClangBridge initialization
    def __init__(self):
        clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")
        return
    # !SECTION
    
    # SECTION   ClangBridge getter functions
    # !SECTION
    
    # SECTION   ClangBridge setter functions
    # !SECTION

    # SECTION   ClangBridge property definitions
    # !SECTION
    
    # SECTION   ClangBridge private functions
    # !SECTION
    
    # SECTION   ClangBridge public functions
    def clang_parse(self, file, parse_args) -> clang.cindex.Cursor:
        """Invoke libclang to parse the given source file"""
        clang_index = clang.cindex.Index.create()
        tu = clang_index.parse(file, [parse_args]).cursor
        return tu
    # !SECTION
# !SECTION


# SECTION   Parser class
class Parser:
    """Parser class.
       Parses the source code by using the passed Clang AST
    """
    
    # SECTION   Parser private attribute definitions
    __slots__ = ['_config', '_cid_manager', 'clang_ast']

    _config: Configuration
    _cid_manager: CIDManager
    clang_ast: clang.cindex.Cursor
    # !SECTION
    
    # SECTION   Parser public attribute definitions
    # !SECTION
    
    # SECTION   Parser initialization
    def __init__(self, config: Configuration, cid_manager: CIDManager, clang_ast: clang.cindex.Cursor):
        self.config = config
        self.cid_manager = cid_manager
        self.clang_ast = clang_ast
        return
    # !SECTION
    
    # SECTION   Parser getter functions
    def _get_config(self) -> Configuration:
        return self._config
    
    def _get_cid_manager(self) -> CIDManager:
        return self._cid_manager
    # !SECTION
    
    # SECTION   Parser setter functions
    def _set_config(self, config:Configuration):
        if config is None:
            raise ValueError("config can't be none")
        elif not isinstance(config, Configuration):
            raise TypeError("config shall be of type Configuration")
        else:
            self._config = config

    def _set_cid_manager(self, cid_manager:CIDManager):
        if cid_manager is None:
            raise ValueError("cid_manager can't be none")
        elif not isinstance(cid_manager, CIDManager):
            raise TypeError("cid_manager shall be of type CIDManager")
        else:
            self._cid_manager = cid_manager
    # !SECTION
    
    # SECTION   Parser property definitions
    config = property(fget=_get_config,
                  fset=_set_config,
                  doc="Stores the config of the Codeconut Instrumenter instance")
    cid_manager = property(fget=_get_cid_manager,
                  fset=_set_cid_manager,
                  doc="Stores the CID manager for the source file")
    # !SECTION
    
    # SECTION   Parser private functions
    # !SECTION
    
    # SECTION   Parser public functions
    def start_parser(self):
        return
    # !SECTION
# !SECTION