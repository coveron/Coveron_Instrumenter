#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Clang Bridge for Codeconut Instrumenter.
   Connect libclang for C/C++ AST to Python
"""

from CIDManager import CIDManager
from Configuration import Configuration

import clang.cindex


# SECTION   ClangBridge class
class ClangBridge:
    """ClangBridge class.
       Connects libclang to Codeconut Instrumenter
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
        tu = clang_index.parse(file, args=parse_args).cursor
        return tu.cursor
    # !SECTION
# !SECTION


def traverse(node):
    for child in node.get_children():
        traverse(child)

    print('Found  : '+node.displayname +
            ' [line='+str(node.location.line)+', col='+str(node.location.column)+']')
    print(node.kind)