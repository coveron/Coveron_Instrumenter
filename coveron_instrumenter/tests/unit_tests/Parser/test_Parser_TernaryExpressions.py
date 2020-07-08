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

import itertools
from unittest.mock import Mock, patch, ANY, call
from pytest import fixture


from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.Parser import ClangBridge, Parser

abs_path_current_dir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_SwitchBranches_basic(mock_config, mock_cid_manager):
    """Test basic ternary expression detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "TernaryExpressions", "TernaryExpression_basic.c")

    # configure the CIDManager mock
    mock_cid_manager.source_file = SourceFile(source_file_path)

    # create the clang bridge
    clang_bridge = ClangBridge()

    # let the clang bridge parse the source file
    clang_cursor = clang_bridge.clang_parse(source_file_path, "")

    # Create the parser
    parser = Parser(mock_config, mock_cid_manager, clang_cursor)

    # traverse the given file
    parser.start_parser()

    # assert calls to add_ternary_expression_data and check evaluation and true/false code sections
    assert mock_cid_manager.add_ternary_expression_data.call_count == 1
    ternary_call_args_list = mock_cid_manager.add_ternary_expression_data.call_args_list

    assert ternary_call_args_list[0] == call(ANY,
                                             ANY,
                                             ANY,
                                             CodeSectionData(
                                                 CodePositionData(6, 9), CodePositionData(6, 16)),
                                             ANY,
                                             ANY,
                                             CodeSectionData(
                                                 CodePositionData(6, 19), CodePositionData(6, 20)),
                                             CodeSectionData(
                                                 CodePositionData(6, 23), CodePositionData(6, 24)))
