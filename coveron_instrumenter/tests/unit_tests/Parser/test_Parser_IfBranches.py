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
def test_Parser_IfBranches_basic(mock_config, mock_cid_manager):
    """Test basic If-Branch detection"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "IfBranches", "IfBranches_basic.c")
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

    # assert calls to add_if_branch_data and check branch_results
    assert mock_cid_manager.add_if_branch_data.call_count == 1
    if_branch_call_args_list = mock_cid_manager.add_if_branch_data.call_args_list

    assert if_branch_call_args_list[0] == call(ANY, ANY, ANY)
    branch_results = if_branch_call_args_list[0][0][2]
    assert len(branch_results) == 2

    # evaluate first branch result
    assert branch_results[0].result_evaluation_code_section == CodeSectionData(
        CodePositionData(5, 9), CodePositionData(5, 14))
    assert branch_results[0].result_body_code_section == CodeSectionData(
        CodePositionData(6, 5), CodePositionData(8, 6))

    # evaluate second branch result
    # evaluation_marker_id shall be -1, since it's a else branch
    assert branch_results[1].evaluation_marker_id == -1
    assert branch_results[1].result_body_code_section == CodeSectionData(
        CodePositionData(10, 5), CodePositionData(12, 6))


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_IfBranches_else_ifs(mock_config, mock_cid_manager):
    """Test handling of else-ifs"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "IfBranches", "IfBranches_else_ifs.c")
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

    # assert calls to add_if_branch_data and check branch_results
    assert mock_cid_manager.add_if_branch_data.call_count == 1
    if_branch_call_args_list = mock_cid_manager.add_if_branch_data.call_args_list

    assert if_branch_call_args_list[0] == call(ANY, ANY, ANY)
    branch_results = if_branch_call_args_list[0][0][2]
    assert len(branch_results) == 6

    # evaluate the evaluation code section of the first two branches to make sure that else if handling works
    assert branch_results[0].result_evaluation_code_section == CodeSectionData(
        CodePositionData(9, 9), CodePositionData(9, 14))
    assert branch_results[1].result_evaluation_code_section == CodeSectionData(
        CodePositionData(13, 14), CodePositionData(13, 19))

    # evaluate last branch result
    # evaluation_marker_id shall be -1, since it's a else branch
    assert branch_results[-1].evaluation_marker_id == -1


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Parser_IfBranches_complex_decisions(mock_config, mock_cid_manager):
    """Test handling of complex decisions (testing of evaluation analysis)"""
    # set source file path
    source_file_path = os.path.join(
        abs_path_current_dir, "input_files", "IfBranches", "IfBranches_complex_decisions.c")
    with open(source_file_path) as input_file:
        source_code = input_file.read()

    # configure the CIDManager mock
    mock_cid_manager.source_file = SourceFile(source_file_path)
    mock_cid_manager.get_new_id.side_effect = itertools.count(
        start=1, step=1)  # id generator for inifinite new ids

    # create the clang bridge
    clang_bridge = ClangBridge()

    # let the clang bridge parse the source file
    clang_cursor = clang_bridge.clang_parse(source_file_path, "")

    # Create the parser
    parser = Parser(mock_config, mock_cid_manager, clang_cursor, source_code)

    # traverse the given file
    parser.start_parser()

    # assert calls to add_if_branch_data and check branch_results
    assert mock_cid_manager.add_if_branch_data.call_count == 1
    if_branch_call_args_list = mock_cid_manager.add_if_branch_data.call_args_list

    assert if_branch_call_args_list[0] == call(ANY, ANY, ANY)
    branch_results = if_branch_call_args_list[0][0][2]
    assert len(branch_results) == 1
    conditions = branch_results[0].conditions
    condition_possibilities = branch_results[0].condition_possibilities

    # evaluate all the conditions in the list
    assert len(conditions) == 5

    assert conditions[0].code_section == CodeSectionData(
        CodePositionData(9, 10), CodePositionData(9, 15))
    assert conditions[1].code_section == CodeSectionData(
        CodePositionData(9, 19), CodePositionData(9, 24))
    assert conditions[2].code_section == CodeSectionData(
        CodePositionData(9, 30), CodePositionData(9, 35))
    assert conditions[3].code_section == CodeSectionData(
        CodePositionData(9, 39), CodePositionData(9, 44))
    assert conditions[4].code_section == CodeSectionData(
        CodePositionData(9, 49), CodePositionData(9, 54))

    # generate list of possible results for this complex decision
    # use data types inside DataTypes.py
    reference_results = [
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, True)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, True)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, True)]),
        ConditionPossibility(False, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, False)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, True)]),
        ConditionPossibility(False, [
            ConditionResult(conditions[0].evaluation_marker_id, True),
            ConditionResult(conditions[1].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, False)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, True)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, True)]),
        ConditionPossibility(False, [
            ConditionResult(conditions[0].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, True),
            ConditionResult(conditions[3].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, False)]),
        ConditionPossibility(True, [
            ConditionResult(conditions[0].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, True)]),
        ConditionPossibility(False, [
            ConditionResult(conditions[0].evaluation_marker_id, False),
            ConditionResult(conditions[2].evaluation_marker_id, False),
            ConditionResult(conditions[4].evaluation_marker_id, False)]),
    ]

    # compare length of condition possibilities and all possibilities with ref list
    assert len(condition_possibilities) == 11

    for reference_result in reference_results:
        found_in_stored_results = False
        for stored_result in condition_possibilities:
            if stored_result.decision_result != reference_result.decision_result:
                # decision_result doesn't fit
                continue
            if len(stored_result.condition_combination) != len(reference_result.condition_combination):
                # condition count doesn't fit
                continue

            condition_did_not_match = False
            # check, if all conditions in reference result exist in stores result
            for reference_condition in reference_result.condition_combination:
                found_conditions = [item for item in stored_result.condition_combination if (
                    item.evaluation_marker_id == reference_condition.evaluation_marker_id and
                    item.condition_result == reference_condition.condition_result)]
                if len(found_conditions) != 1:
                    condition_did_not_match = True
                    break

            if condition_did_not_match is False:
                # all conditions matched and decision fits, so this condition_possibility was found!
                found_in_stored_results = True

        if found_in_stored_results is False:
            raise AssertionError("ConditionResult not found!")
