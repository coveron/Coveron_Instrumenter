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
    __slots__ = ['config', 'cid_manager', 'clang_ast']

    config: Configuration
    cid_manager: CIDManager
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
    # !SECTION
    
    # SECTION   Parser setter functions
    # !SECTION
    
    # SECTION   Parser property definitions
    # !SECTION
    
    # SECTION   Parser private functions
    # !SECTION
    
    # SECTION   Parser public functions
    def start_parser(self):
        self.traverse_root(self.clang_ast)
        return

    def traverse_root(self, ast_pointer):
        """Searches for functions inside the code of the active source file."""

        # Travel through the first layer of the AST.
        # Goal: Find functions with a source file name equal to the file name of the instrumented code.
        #       (ignore headers etc.)
        return

    def traverse_function(self, ast_cursor: clang.cindex.Cursor, args: object):
        """Parses a function passed to it"""
        function_id = self.cid_manager.get_new_id()
        function_name = ast_cursor.displayname
        function_type = FunctionType.NORMAL
        parent_function_id = args["parent_function_id"]

        inner_traverse_args = {
            "isCase": False,
            "parent_function_id": function_id
        }
        checkpoint_marker_id = traverse_compound_statement(ast_cursor.get_children()[-1], args)
        # First: Get start position of element to start position of compound_statement to store the header
        #header_code_section = 

        #inner_code_section = 

        #self.cid_manager.add_function_data(function_name, function_type, parent_function_id,
                #checkpoint_marker_id, header_code_section, inner_code_section)
        return

    def traverse_compound_statement(self, ast_cursor: clang.cindex.Cursor, args: object):
        """Parses a compound statement given to it"""

    # !SECTION
# !SECTION