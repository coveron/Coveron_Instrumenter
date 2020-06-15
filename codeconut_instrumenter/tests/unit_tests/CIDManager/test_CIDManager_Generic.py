#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Unit Tests for the CID-Manager module.
"""

import sys
import os

import pytest
from unittest.mock import Mock, patch

from codeconut_instrumenter.DataTypes import CodeSectionData, MarkerTypeEnum

from codeconut_instrumenter.CIDManager import CIDManager
from codeconut_instrumenter.Configuration import Configuration


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_init(mock_config):

    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = True

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(cid_manager, CIDManager) == True


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    # add new marker
    new_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)
    assert cid_manager.create_statement_marker([new_code_section]) == 1

    # check data in new marker
    assert cid_manager.get_markers()[0].marker_type == MarkerTypeEnum.STATEMENT
    assert cid_manager.get_markers()[0].marker_id == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_column == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_column == 5


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addDecisionMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    # add new marker
    new_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)
    assert cid_manager.create_decision_marker([new_code_section]) == 1

    # check data in new marker
    assert cid_manager.get_markers()[0].marker_type == MarkerTypeEnum.DECISION
    assert cid_manager.get_markers()[0].marker_id == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_column == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_column == 5


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addConditionMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = True

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    # add new markers
    decision_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)
    assert cid_manager.create_decision_marker([decision_code_section]) == 1

    condition1_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=3)
    assert cid_manager.create_condition_marker(
        1, [condition1_code_section]) == 2

    condition2_code_section = CodeSectionData(
        start_line=1, start_column=4, end_line=1, end_column=5)
    assert cid_manager.create_condition_marker(
        1, [condition2_code_section]) == 3

    # check data in new markers
    assert cid_manager.get_markers()[0].marker_type == MarkerTypeEnum.DECISION
    assert cid_manager.get_markers()[0].marker_id == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].start_column == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_line == 1
    assert cid_manager.get_markers()[0].code_section_data[0].end_column == 5

    assert cid_manager.get_markers()[1].marker_type == MarkerTypeEnum.CONDITION
    assert cid_manager.get_markers()[1].marker_id == 2
    assert cid_manager.get_markers()[1].parent_id == 1
    assert cid_manager.get_markers()[1].code_section_data[0].start_line == 1
    assert cid_manager.get_markers()[1].code_section_data[0].start_column == 1
    assert cid_manager.get_markers()[1].code_section_data[0].end_line == 1
    assert cid_manager.get_markers()[1].code_section_data[0].end_column == 3

    assert cid_manager.get_markers()[2].marker_type == MarkerTypeEnum.CONDITION
    assert cid_manager.get_markers()[2].marker_id == 3
    assert cid_manager.get_markers()[2].parent_id == 1
    assert cid_manager.get_markers()[2].code_section_data[0].start_line == 1
    assert cid_manager.get_markers()[2].code_section_data[0].start_column == 4
    assert cid_manager.get_markers()[2].code_section_data[0].end_line == 1
    assert cid_manager.get_markers()[2].code_section_data[0].end_column == 5


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = False
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    statement_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)

    with pytest.raises(RuntimeError):
        cid_manager.create_statement_marker([statement_code_section])


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addDecisionMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = False
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    decision_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)

    with pytest.raises(RuntimeError):
        cid_manager.create_decision_marker([decision_code_section])


@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addConditionMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = False
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    condition_code_section = CodeSectionData(
        start_line=1, start_column=1, end_line=1, end_column=5)

    with pytest.raises(RuntimeError):
        cid_manager.create_condition_marker([condition_code_section])
