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


class ClangBridge:
    """ClangBridge
       Connects Clang libclang to the Instrumenter for code parsing via AST
    """
    # SECTION   ClangBridge private attribute definitions
    # !SECTION

    # SECTION   ClangBridge initialization
    def __init__(self):
        """Initializes the new ClangBridge"""
    # !SECTION

    # SECTION   ClangBridge getter functions
    # !SECTION

    # SECTION   ClangBridge setter functions
    # !SECTION

    # SECTION   Parser property definitions
    # !SECTION

    # SECTION   Parser public function definitions
    def traverse(self, node):
        for child in node.get_children():
            self.traverse(child)

        print('Found  : '+node.displayname +
              ' [line='+str(node.location.line)+', col='+str(node.location.column)+']')
        print(node.kind)

    def clang_parse(self, file):
        """Invoke libclang to parse the given source file"""
        clang.cindex.Config.set_library_path(
            "C:\\Program Files\\LLVM\\bin")
        clang_index = clang.cindex.Index.create()
        tu = clang_index.parse(file)

        self.traverse(tu.cursor)
        return
    # !SECTION
