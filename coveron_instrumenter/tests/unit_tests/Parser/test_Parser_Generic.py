#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Unit Tests for the Parser module
"""

from unittest.mock import Mock, patch

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.Parser import ClangBridge, Parser

abs_path_current_dir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)))


def test_ClangBrigde():
    clang_bridge = ClangBridge()

    # parse the base file
    base_file_path = os.path.join(
        abs_path_current_dir, "input_files", "base_file.c")
    clang_bridge.clang_parse(base_file_path, "")

    assert isinstance(clang_bridge, ClangBridge) == True


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_Init(mock_config, mock_cid_manager):
    # create the clang bridge
    clang_bridge = ClangBridge()

    # let the clang bridge parse the base file
    base_file_path = os.path.join(
        abs_path_current_dir, "input_files", "base_file.c")
    clang_cursor = clang_bridge.clang_parse(base_file_path, "")

    # Create the parser
    parser = Parser(mock_config, mock_cid_manager, clang_cursor)

    assert isinstance(parser, Parser) == True
