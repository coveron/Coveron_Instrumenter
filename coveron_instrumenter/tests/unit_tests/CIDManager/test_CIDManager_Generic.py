#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Unit Tests for the CID-Manager module.
"""

from unittest.mock import Mock, patch
import pytest

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.CIDManager import CIDManager
from coveron_instrumenter.Configuration import Configuration


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_init(mock_config):

    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    assert isinstance(cid_manager, CIDManager) == True


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addCheckpointMarker(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    # add new marker
    new_code_position = CodePositionData(5, 3)
    checkpoint_marker_id = cid_manager.get_new_id()
    assert cid_manager.add_checkpoint_marker(
        checkpoint_marker_id, new_code_position)

    # check data in new marker
    assert cid_manager.get_checkpoint_markers(
    )[0].checkpoint_marker_id == checkpoint_marker_id
    assert cid_manager.get_checkpoint_markers()[0].code_position.line == 5
    assert cid_manager.get_checkpoint_markers()[0].code_position.column == 3


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addDecisionMarker(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    # add new marker
    new_code_section = CodeSectionData(
        CodePositionData(2, 1),
        CodePositionData(5, 3))
    evaluation_marker_id = cid_manager.get_new_id()
    assert cid_manager.add_evaluation_marker(
        evaluation_marker_id, new_code_section, EvaluationType.DECISION)

    # check data in new marker
    assert cid_manager.get_evaluation_markers(
    )[0].evaluation_marker_id == evaluation_marker_id
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.start_position.line == 2
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.start_position.column == 1
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.end_position.line == 5
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.end_position.column == 3
    assert cid_manager.get_evaluation_markers(
    )[0].evaluation_type == EvaluationType.DECISION


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addConditionMarker(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    # add new marker
    new_code_section = CodeSectionData(
        CodePositionData(2, 1),
        CodePositionData(5, 3))
    evaluation_marker_id = cid_manager.get_new_id()
    assert cid_manager.add_evaluation_marker(
        evaluation_marker_id, new_code_section, EvaluationType.CONDITION)

    # check data in new marker
    assert cid_manager.get_evaluation_markers(
    )[0].evaluation_marker_id == evaluation_marker_id
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.start_position.line == 2
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.start_position.column == 1
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.end_position.line == 5
    assert cid_manager.get_evaluation_markers(
    )[0].code_section.end_position.column == 3
    assert cid_manager.get_evaluation_markers(
    )[0].evaluation_type == EvaluationType.CONDITION


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addCheckpointMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    dummy_code_position = CodePositionData(1, 1)

    with pytest.raises(RuntimeError):
        cid_manager.add_checkpoint_marker(
            cid_manager.get_new_id(), dummy_code_position)


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addEvaluationMarker_badConfig(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    dummy_code_section = CodeSectionData(
        CodePositionData(1, 1),
        CodePositionData(5, 2))

    with pytest.raises(RuntimeError):
        cid_manager.add_evaluation_marker(
            cid_manager.get_new_id(), dummy_code_section, EvaluationType.DECISION)
