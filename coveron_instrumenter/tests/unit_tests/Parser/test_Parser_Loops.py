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
from coveron_instrumenter.Configuration import SourceFile

from coveron_instrumenter.Parser import ClangBridge, Parser

abs_path_current_dir = os.path.abspath(
    os.path.dirname(os.path.realpath(__file__)))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_Loops_for(mock_config, mock_cid_manager):
    """Test basic for loop detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "Loops", "Loop_for.c")

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
    assert mock_cid_manager.add_loop_data.call_count == 1
    loop_call_args_list = mock_cid_manager.add_loop_data.call_args_list

    assert loop_call_args_list[0] == call(ANY,
                                          LoopType.FOR,
                                          ANY,
                                          ANY,
                                          CodeSectionData(
                                              CodePositionData(5, 21), CodePositionData(5, 27)),
                                          CodeSectionData(
                                              CodePositionData(6, 5), CodePositionData(13, 6)),
                                          ANY,
                                          ANY)

    # assert correct checkpoint marker inside for-loop
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(7, 9))
    assert checkpoint_call_args_list[2] == call(ANY, CodePositionData(9, 13))
    assert checkpoint_call_args_list[3] == call(ANY, CodePositionData(10, 13))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_Loops_while(mock_config, mock_cid_manager):
    """Test basic while loop detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "Loops", "Loop_while.c")

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
    assert mock_cid_manager.add_loop_data.call_count == 1
    loop_call_args_list = mock_cid_manager.add_loop_data.call_args_list

    assert loop_call_args_list[0] == call(ANY,
                                          LoopType.WHILE,
                                          ANY,
                                          ANY,
                                          CodeSectionData(
                                              CodePositionData(5, 12), CodePositionData(5, 18)),
                                          CodeSectionData(
                                              CodePositionData(6, 5), CodePositionData(10, 6)),
                                          ANY,
                                          ANY)

    # assert correct checkpoint marker inside for-loop
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(7, 9))
    assert checkpoint_call_args_list[2] == call(ANY, CodePositionData(9, 9))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_Loops_dowhile(mock_config, mock_cid_manager):
    """Test basic do-while loop detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "Loops", "Loop_dowhile.c")

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
    assert mock_cid_manager.add_loop_data.call_count == 1
    loop_call_args_list = mock_cid_manager.add_loop_data.call_args_list

    assert loop_call_args_list[0] == call(ANY,
                                          LoopType.DOWHILE,
                                          ANY,
                                          ANY,
                                          CodeSectionData(
                                              CodePositionData(8, 14), CodePositionData(8, 20)),
                                          CodeSectionData(
                                              CodePositionData(6, 5), CodePositionData(8, 6)),
                                          ANY,
                                          ANY)

    # assert correct checkpoint marker inside for-loop
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(7, 9))
