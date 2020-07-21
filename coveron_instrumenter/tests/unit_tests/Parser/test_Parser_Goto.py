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
def test_Parser_Goto_basic(mock_config, mock_cid_manager):
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "Goto", "Goto_basic.c")

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

    # assert calls to add_checkpoint_data
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[0] == call(
        ANY, CodePositionData(3, 5))
    assert checkpoint_call_args_list[1] == call(
        ANY, CodePositionData(6, 9))
    assert checkpoint_call_args_list[2] == call(
        ANY, CodePositionData(7, 9))
    assert checkpoint_call_args_list[3] == call(
        ANY, CodePositionData(9, 5))
    assert checkpoint_call_args_list[4] == call(
        ANY, CodePositionData(13, 5))
    assert mock_cid_manager.add_checkpoint_marker.call_count == 5
