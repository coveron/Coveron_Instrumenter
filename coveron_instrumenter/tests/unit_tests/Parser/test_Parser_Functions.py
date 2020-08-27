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

from unittest.mock import Mock, patch, ANY, call

from coveron_instrumenter.DataTypes import *
from coveron_instrumenter.Configuration import SourceFile

from coveron_instrumenter.Parser import ClangBridge, Parser

abs_path_current_dir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_Functions(mock_config, mock_cid_manager):
    # set seource file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "Functions", "Functions_basic.c")
    with open(source_file_path) as input_file:
        source_code = input_file.read()

    # configure the CIDManager mock
    mock_cid_manager.source_file = SourceFile(source_file_path)

    # create the clang bridge
    clang_bridge = ClangBridge()

    # let the clang bridge parse the source file
    clang_cursor = clang_bridge.clang_parse(source_file_path, "")

    # Create the parser
    parser = Parser(mock_config, mock_cid_manager, clang_cursor, source_code)

    # traverse the given file
    parser.start_parser()

    # assert calls to add_function_data
    function_call_args_list = mock_cid_manager.add_function_data.call_args_list

    assert function_call_args_list[0] == call(
        ANY, 'main()', FunctionType.NORMAL, -1, ANY,
        CodeSectionData(CodePositionData(1, 1), CodePositionData(2, 1)),
        CodeSectionData(CodePositionData(2, 1), CodePositionData(4, 2)))
    assert function_call_args_list[1] == call(
        ANY, 'dummy_function(int)', FunctionType.NORMAL, -1, ANY,
        CodeSectionData(CodePositionData(6, 1), CodePositionData(7, 1)),
        CodeSectionData(CodePositionData(7, 1), CodePositionData(9, 2)))
    assert mock_cid_manager.add_function_data.call_count == 2

    # assert calls to add_checkpoint_marker
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[0] == call(ANY, CodePositionData(3, 5))
    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(8, 5))
