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

from coveron_instrumenter.Parser import ClangBridge, Parser

abs_path_current_dir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_CompoundStatements_nested(mock_config, mock_cid_manager):
    # set seource file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "CompoundStatements", "CompoundStatements_nested.c")

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

    # assert calls to add_statement_data
    statement_call_args_list = mock_cid_manager.add_statement_data.call_args_list

    assert statement_call_args_list[0] == call(
        ANY, StatementType.NORMAL, ANY, ANY, CodeSectionData(CodePositionData(3, 5), CodePositionData(3, 15)))
    assert statement_call_args_list[1] == call(
        ANY, StatementType.NORMAL, ANY, ANY, CodeSectionData(CodePositionData(5, 9), CodePositionData(5, 19)))
    assert statement_call_args_list[2] == call(
        ANY, StatementType.RETURN, ANY, ANY, CodeSectionData(CodePositionData(8, 17), CodePositionData(8, 25)))
    assert statement_call_args_list[3] == call(
        ANY, StatementType.NORMAL, ANY, ANY, CodeSectionData(CodePositionData(10, 13), CodePositionData(10, 23)))
    assert statement_call_args_list[4] == call(
        ANY, StatementType.RETURN, ANY, ANY, CodeSectionData(CodePositionData(13, 13), CodePositionData(13, 21)))
    assert statement_call_args_list[5] == call(
        ANY, StatementType.NORMAL, ANY, ANY, CodeSectionData(CodePositionData(15, 17), CodePositionData(15, 27)))
    assert statement_call_args_list[6] == call(
        ANY, StatementType.RETURN, ANY, ANY, CodeSectionData(CodePositionData(19, 13), CodePositionData(19, 21)))
    assert statement_call_args_list[7] == call(
        ANY, StatementType.NORMAL, ANY, ANY, CodeSectionData(CodePositionData(20, 13), CodePositionData(20, 23)))
    assert mock_cid_manager.add_statement_data.call_count == 8

    # assert calls to add_checkpoint_data
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[0] == call(
        ANY, CodePositionData(3, 5))
    assert checkpoint_call_args_list[1] == call(
        ANY, CodePositionData(10, 13))
    assert checkpoint_call_args_list[2] == call(
        ANY, CodePositionData(12, 9))
    assert checkpoint_call_args_list[3] == call(
        ANY, CodePositionData(14, 13))
    assert checkpoint_call_args_list[4] == call(
        ANY, CodePositionData(18, 9))
    assert checkpoint_call_args_list[5] == call(
        ANY, CodePositionData(20, 13))
    assert mock_cid_manager.add_checkpoint_marker.call_count == 6
