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

from codeconut_instrumenter.CIDManager import CIDManager
from codeconut_instrumenter.Configuration import Configuration


# SECTION   Initialization
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_init():

    mock_config = Configuration()
    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(CIDManager, cid_manager) == True
# !SECTION

# SECTION   Creation of statement marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker():

    # setup for configuration mock
    mock_config = Configuration()
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(CIDManager, cid_manager) == True
# !SECTION

# SECTION   Creation of decision marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addDecisionMarker():

    # setup for configuration mock
    mock_config = Configuration()
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(CIDManager, cid_manager) == True
# !SECTION

# SECTION   Creation of condition marker
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addConditionMarker():

    # setup for configuration mock
    mock_config = Configuration()
    mock_config.statement_analysis_enabled = True
    mock_config.decision_analysis_enabled = True
    mock_config.condition_analysis_enabled = True

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(CIDManager, cid_manager) == True
# !SECTION

# SECTION   Creation of statement marker with disabled statement analysis
@patch('codeconut_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementMarker_badConfig():

    # setup for configuration mock
    mock_config = Configuration()
    mock_config.statement_analysis_enabled = False
    mock_config.decision_analysis_enabled = False
    mock_config.condition_analysis_enabled = False

    cid_manager = CIDManager(mock_config, 'test_filename.c', 'test_code')

    assert isinstance(CIDManager, cid_manager) == True
# !SECTION
