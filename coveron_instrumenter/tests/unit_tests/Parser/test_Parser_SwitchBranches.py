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
def test_Parser_SwitchBranches_basic(mock_config, mock_cid_manager):
    """Test basic Switch-Branch detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "SwitchBranches", "SwitchBranches_basic.c")
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

    # assert calls to add_switch_branch_data and check cases
    assert mock_cid_manager.add_switch_branch_data.call_count == 1
    switch_branch_call_args_list = mock_cid_manager.add_switch_branch_data.call_args_list

    assert switch_branch_call_args_list[0] == call(ANY, ANY, ANY, ANY)

    # check code section of whole case
    assert switch_branch_call_args_list[0][0][2] == CodeSectionData(
        CodePositionData(6, 5), CodePositionData(17, 6))

    switch_cases = switch_branch_call_args_list[0][0][3]
    assert len(switch_cases) == 3

    # evaluate first case result
    assert switch_cases[0].case_type == CaseType.CASE
    assert switch_cases[0].evaluation_code_section == CodeSectionData(
        CodePositionData(8, 5), CodePositionData(8, 11))
    assert switch_cases[0].body_code_section == CodeSectionData(
        CodePositionData(9, 9), CodePositionData(9, 14))

    # evaluate second case result
    assert switch_cases[1].case_type == CaseType.CASE
    assert switch_cases[1].evaluation_code_section == CodeSectionData(
        CodePositionData(11, 5), CodePositionData(11, 11))
    assert switch_cases[1].body_code_section == CodeSectionData(
        CodePositionData(12, 9), CodePositionData(12, 14))

    # evaluate last case result
    assert switch_cases[2].case_type == CaseType.DEFAULT
    assert switch_cases[2].evaluation_code_section == CodeSectionData(
        CodePositionData(14, 5), CodePositionData(14, 12))
    assert switch_cases[2].body_code_section == CodeSectionData(
        CodePositionData(15, 9), CodePositionData(15, 14))

    # check additions to statement data
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(9, 9))
    assert checkpoint_call_args_list[2] == call(ANY, CodePositionData(12, 9))
    assert checkpoint_call_args_list[3] == call(ANY, CodePositionData(15, 9))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_SwitchBranches_combined_cases(mock_config, mock_cid_manager):
    """Test Switch-Branch detection with all kinds of case combinations"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "SwitchBranches", "SwitchBranches_combined_cases.c")
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

    # assert calls to add_switch_branch_data and check cases
    assert mock_cid_manager.add_switch_branch_data.call_count == 2
    switch_branch_call_args_list = mock_cid_manager.add_switch_branch_data.call_args_list

    assert switch_branch_call_args_list[0] == call(ANY,
                                                   ANY,
                                                   CodeSectionData(
                                                       CodePositionData(6, 5), CodePositionData(21, 6)),
                                                   ANY)
    assert switch_branch_call_args_list[1] == call(ANY,
                                                   ANY,
                                                   CodeSectionData(
                                                       CodePositionData(23, 5), CodePositionData(29, 6)),
                                                   ANY)

    # assert first switch branch results
    first_switch_cases = switch_branch_call_args_list[0][0][3]
    assert len(first_switch_cases) == 6
    # evaluate first case result
    assert first_switch_cases[0].case_type == CaseType.CASE
    assert first_switch_cases[0].evaluation_code_section == CodeSectionData(
        CodePositionData(8, 5), CodePositionData(8, 12))
    assert first_switch_cases[0].body_code_section == CodeSectionData(
        CodePositionData(9, 9), CodePositionData(9, 15))

    # evaluate second case result
    assert first_switch_cases[1].case_type == CaseType.CASE
    assert first_switch_cases[1].evaluation_code_section == CodeSectionData(
        CodePositionData(11, 5), CodePositionData(11, 11))
    assert first_switch_cases[1].body_code_section == CodeSectionData(
        CodePositionData(12, 9), CodePositionData(12, 14))

    # evaluate third case result
    assert first_switch_cases[2].case_type == CaseType.CASE
    assert first_switch_cases[2].evaluation_code_section == CodeSectionData(
        CodePositionData(13, 5), CodePositionData(13, 11))
    assert first_switch_cases[2].body_code_section == CodeSectionData(
        CodePositionData(14, 9), CodePositionData(14, 14))

    # evaluate fourth case result (cases 4 and 5 are switched beacuse of recursive behavior)
    assert first_switch_cases[4].case_type == CaseType.CASE
    assert first_switch_cases[4].evaluation_code_section == CodeSectionData(
        CodePositionData(16, 5), CodePositionData(16, 11))
    # body code section should be equal to following case
    assert first_switch_cases[4].body_code_section == first_switch_cases[3].body_code_section

    # evaluate fifth case result
    assert first_switch_cases[3].case_type == CaseType.CASE
    assert first_switch_cases[3].evaluation_code_section == CodeSectionData(
        CodePositionData(17, 5), CodePositionData(17, 11))
    assert first_switch_cases[3].body_code_section == CodeSectionData(
        CodePositionData(18, 9), CodePositionData(18, 14))

    # evaluate last case result
    assert first_switch_cases[5].case_type == CaseType.DEFAULT
    assert first_switch_cases[5].evaluation_code_section == CodeSectionData(
        CodePositionData(19, 5), CodePositionData(19, 12))
    assert first_switch_cases[5].body_code_section == CodeSectionData(
        CodePositionData(20, 9), CodePositionData(20, 14))

    # assert second switch branch cases
    second_switch_cases = switch_branch_call_args_list[1][0][3]
    assert len(second_switch_cases) == 2

    # evaluate first case result
    assert second_switch_cases[1].case_type == CaseType.DEFAULT
    assert second_switch_cases[1].evaluation_code_section == CodeSectionData(
        CodePositionData(25, 5), CodePositionData(25, 12))
    assert second_switch_cases[1].body_code_section == second_switch_cases[0].body_code_section

    # evaluate second case result
    assert second_switch_cases[0].case_type == CaseType.CASE
    assert second_switch_cases[0].evaluation_code_section == CodeSectionData(
        CodePositionData(26, 5), CodePositionData(26, 12))
    assert second_switch_cases[0].body_code_section == CodeSectionData(
        CodePositionData(27, 9), CodePositionData(27, 15))

    # check additions to statement data
    checkpoint_call_args_list = mock_cid_manager.add_checkpoint_marker.call_args_list

    assert checkpoint_call_args_list[1] == call(ANY, CodePositionData(9, 9))
    assert checkpoint_call_args_list[2] == call(ANY, CodePositionData(12, 9))
    assert checkpoint_call_args_list[3] == call(ANY, CodePositionData(14, 9))
    # switched up order for fourth and fifth evaluation statement because of recursive behavior
    assert checkpoint_call_args_list[5] == call(ANY, CodePositionData(16, 12))
    assert checkpoint_call_args_list[4] == call(ANY, CodePositionData(18, 9))
    assert checkpoint_call_args_list[6] == call(ANY, CodePositionData(20, 9))

    # checkpoint after switch (caused by break)
    assert checkpoint_call_args_list[7] == call(ANY, CodePositionData(23, 5))

    # checkpoints of next switch (switched up because of recursive behavior)
    assert checkpoint_call_args_list[9] == call(ANY, CodePositionData(25, 13))
    assert checkpoint_call_args_list[8] == call(ANY, CodePositionData(27, 9))
