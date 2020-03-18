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


# SECTION   Initialization
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_init(mock_config):

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(cid_manager, CIDManager) == True
# !SECTION


# SECTION   Creation of statement marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    # add new marker
    new_code_section = CodeSectionData()
    new_code_section.start_line = 1
    new_code_section.start_column = 1
    new_code_section.end_line = 1
    new_code_section.end_column = 5
    assert cid_manager.create_statement_marker([new_code_section]) != 0

    # check data in new marker
    assert cid_manager.get_markers()[0].marker_type == MarkerTypeEnum.STATEMENT
    assert cid_manager.get_markers()[0].marker_id == 1
    assert cid_manager.get_markers()[0].code_section_data.start_line == 1
    assert cid_manager.get_markers()[0].code_section_data.start_column == 1
    assert cid_manager.get_markers()[0].code_section_data.end_line == 1
    assert cid_manager.get_markers()[0].code_section_data.end_column == 5
# !SECTION


# SECTION   Creation of decision marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addDecisionMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(cid_manager, CIDManager) == True
# !SECTION


# SECTION   Creation of condition marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addConditionMarker(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = True

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(cid_manager, CIDManager) == True
# !SECTION


# SECTION   Creation of statement marker with disabled statement analysis
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.statement_analysis_enabled = False
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(cid_manager, CIDManager) == True
# !SECTION
