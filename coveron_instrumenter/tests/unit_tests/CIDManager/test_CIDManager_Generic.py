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

    # validate, if this indeed is a deepcopy, by modifying the id of the output data and checking it afterwards
    cid_manager.get_checkpoint_markers()[0].checkpoint_marker_id = 999

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

    # validate, if this indeed is a deepcopy, by modifying the id of the output data and checking it afterwards
    cid_manager.get_evaluation_markers()[0].evaluation_marker_id = 999

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


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_getNewId(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    id_1 = cid_manager.get_new_id()
    id_2 = cid_manager.get_new_id()

    assert id_1 < id_2


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_getInstrumentationRandom(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    instrumentation_random = cid_manager.get_instrumentation_random()

    assert len(instrumentation_random) == 32
    assert (
        not bool(re.compile(r'[^a-fA-F0-9]').search(instrumentation_random))) == True


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_getSourceCodeHash(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    source_code_hash = cid_manager.get_source_code_hash()

    assert len(source_code_hash) == 64
    # sha256 for 'test_code'
    assert source_code_hash == '3aa0041781f53f591089fa2aeed013200e54828311ae3f4f4f343edba87dc071'


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addClassData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    class_id = 1
    class_name = "test_class"

    cid_manager.add_class_data(class_id, class_name)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.classes[0]

    assert element.class_id == 1
    assert element.class_name == "test_class"


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addFunctionData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    function_id = 10
    function_name = "test_function"
    function_type = FunctionType.NORMAL
    parent_function_id = 55
    checkpoint_marker_id = 4
    header_code_section = CodeSectionData(
        CodePositionData(1, 5),
        CodePositionData(2, 4))
    inner_code_section = CodeSectionData(
        CodePositionData(30, 5),
        CodePositionData(35, 9))

    cid_manager.add_function_data(function_id,
                                  function_name,
                                  function_type,
                                  parent_function_id,
                                  checkpoint_marker_id,
                                  header_code_section,
                                  inner_code_section)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.functions[0]

    assert element.function_id == 10
    assert element.function_name == "test_function"
    assert element.function_type == FunctionType.NORMAL
    assert element.parent_function_id == 55
    assert element.checkpoint_marker_id == 4
    assert element.header_code_section.start_position.line == 1
    assert element.header_code_section.start_position.column == 5
    assert element.header_code_section.end_position.line == 2
    assert element.header_code_section.end_position.column == 4
    assert element.inner_code_section.start_position.line == 30
    assert element.inner_code_section.start_position.column == 5
    assert element.inner_code_section.end_position.line == 35
    assert element.inner_code_section.end_position.column == 9


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addStatementData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    statement_id = 140
    statement_type = StatementType.NORMAL
    function_id = 2
    checkpoint_marker_id = 4
    code_section = CodeSectionData(
        CodePositionData(4, 2),
        CodePositionData(10, 9))

    cid_manager.add_statement_data(statement_id,
                                   statement_type,
                                   function_id,
                                   checkpoint_marker_id,
                                   code_section)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.statements[0]

    assert element.statement_id == 140
    assert element.statement_type == StatementType.NORMAL
    assert element.function_id == 2
    assert element.checkpoint_marker_id == 4
    assert element.code_section.start_position.line == 4
    assert element.code_section.start_position.column == 2
    assert element.code_section.end_position.line == 10
    assert element.code_section.end_position.column == 9
