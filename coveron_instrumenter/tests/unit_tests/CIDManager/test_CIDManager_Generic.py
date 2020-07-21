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
import json
import jsonschema
import gzip

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.CIDManager import CIDManager
from coveron_instrumenter.Configuration import Configuration, SourceFile


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
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

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
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

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
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

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


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addIfBranchData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    if_branch_id = 40
    function_id = 18
    branch_results = [
        BranchResultData(20,
                         # dummy condition
                         [ConditionPossibility(True, [ConditionResult(5, True)]),
                          ConditionPossibility(False, [ConditionResult(5, False)])],
                         [ConditionData(95, CodeSectionData(
                             CodePositionData(10, 2), CodePositionData(19, 8)))],
                         CodeSectionData(CodePositionData(
                             10, 1), CodePositionData(19, 9)),  # evaluation code section
                         CodeSectionData(CodePositionData(20, 2), CodePositionData(29, 5)))  # bode code section
    ]

    cid_manager.add_if_branch_data(if_branch_id,
                                   function_id,
                                   branch_results)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.if_branches[0]

    # assert, if data was stored correctly
    assert element.if_branch_id == if_branch_id
    assert element.function_id == function_id
    assert element.branch_results == branch_results


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addSwitchBranchData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    switch_branch_id = 48
    function_id = 92
    switch_branch_code_section = CodeSectionData(
        CodePositionData(5, 2), CodePositionData(18, 5))
    cases = [CaseData(18,
                      CaseType.CASE,
                      CodeSectionData(CodePositionData(21, 2),
                                      CodePositionData(21, 19)),
                      CodeSectionData(CodePositionData(22, 5), CodePositionData(25, 9)))]

    cid_manager.add_switch_branch_data(switch_branch_id,
                                       function_id,
                                       switch_branch_code_section,
                                       cases)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.switch_branches[0]

    # assert, if data was stored correctly
    assert element.switch_branch_id == switch_branch_id
    assert element.function_id == function_id
    assert element.switch_branch_code_section == switch_branch_code_section
    assert element.cases == cases


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addTernaryExpressionData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    ternary_expression_id = 882
    function_id = 428
    evaluation_marker_id = 381
    evaluation_code_section = CodeSectionData(
        CodePositionData(15, 10), CodePositionData(15, 16))
    condition_possibilities = [ConditionPossibility(True, [ConditionResult(5, True)]),
                               ConditionPossibility(False, [ConditionResult(5, False)])]
    conditions = [ConditionData(28, CodeSectionData(
        CodePositionData(15, 11), CodePositionData(15, 15)))]
    true_code_section = CodeSectionData(
        CodePositionData(15, 20), CodePositionData(15, 26))
    false_code_section = CodeSectionData(
        CodePositionData(15, 30), CodePositionData(15, 42))

    cid_manager.add_ternary_expression_data(ternary_expression_id,
                                            function_id,
                                            evaluation_marker_id,
                                            evaluation_code_section,
                                            condition_possibilities,
                                            conditions,
                                            true_code_section,
                                            false_code_section)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.ternary_expressions[0]

    # assert, if data was stored correctly
    assert element.ternary_expression_id == ternary_expression_id
    assert element.function_id == function_id
    assert element.evaluation_marker_id == evaluation_marker_id
    assert element.evaluation_code_section == evaluation_code_section
    assert element.condition_possibilities == condition_possibilities
    assert element.conditions == conditions


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_addLoopData(mock_config):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = False
    mock_config.evaluation_markers_enabled = False

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    loop_id = 841
    loop_type = LoopType.FOR
    function_id = 32
    evaluation_marker_id = 48
    evaluation_code_section = CodeSectionData(
        CodePositionData(19, 2), CodePositionData(19, 17)),
    body_code_section = CodeSectionData(
        CodePositionData(20, 2), CodePositionData(25, 3))
    condition_possibilities = [ConditionPossibility(True, [ConditionResult(5, True)]),
                               ConditionPossibility(False, [ConditionResult(5, False)])]
    conditions = [ConditionData(29, CodeSectionData(
        CodePositionData(19, 3), CodePositionData(19, 16)))]

    cid_manager.add_loop_data(loop_id,
                              loop_type,
                              function_id,
                              evaluation_marker_id,
                              evaluation_code_section,
                              body_code_section,
                              condition_possibilities,
                              conditions)

    # get stored element (access directly, although private element)
    element = cid_manager._cid_data.code_data.loops[0]

    # assert, if data was stored correctly
    assert element.loop_id == loop_id
    assert element.loop_type == loop_type
    assert element.function_id == function_id
    assert element.evaluation_marker_id == evaluation_marker_id
    assert element.evaluation_code_section == evaluation_code_section
    assert element.body_code_section == body_code_section
    assert element.condition_possibilities == condition_possibilities
    assert element.conditions == conditions


@patch('coveron_instrumenter.Configuration.Configuration')
def test_CIDManager_writeCidFile(mock_config, tmpdir):

    # setup for configuration mock
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True
    mock_config.output_abs_path = tmpdir

    cid_manager = CIDManager(
        mock_config, SourceFile('test_file.c'), 'test_code')

    # add checkpoint marker
    cid_manager.add_checkpoint_marker(4, CodePositionData(1, 6))

    # add evaluation marker
    cid_manager.add_evaluation_marker(5,
                                      CodeSectionData(CodePositionData(
                                          1, 5), CodePositionData(1, 15)),
                                      EvaluationType.DECISION)

    # add class
    cid_manager.add_class_data(483, 'test_class')

    # add function
    cid_manager.add_function_data(10,
                                  "test_function",
                                  FunctionType.NORMAL,
                                  55,
                                  4,
                                  CodeSectionData(
                                      CodePositionData(1, 5),
                                      CodePositionData(2, 4)),
                                  CodeSectionData(
                                      CodePositionData(30, 5),
                                      CodePositionData(35, 9))
                                  )

    # add statement
    cid_manager.add_statement_data(20,
                                   StatementType.NORMAL,
                                   83,
                                   844,
                                   CodeSectionData(
                                       CodePositionData(1, 5),
                                       CodePositionData(2, 4)))

    # add if-branch
    cid_manager.add_if_branch_data(40,
                                   18,
                                   [BranchResultData(20,
                                                     # dummy condition
                                                     [ConditionPossibility(True, [ConditionResult(5, True)]),
                                                      ConditionPossibility(False, [ConditionResult(5, False)])],
                                                     [ConditionData(95, CodeSectionData(
                                                         CodePositionData(10, 2), CodePositionData(19, 8)))],
                                                     CodeSectionData(
                                                         CodePositionData(10, 1), CodePositionData(19, 9)),  # evaluation code section
                                                     CodeSectionData(
                                                         CodePositionData(20, 2), CodePositionData(29, 5)))])

    # add switch-branch
    cid_manager.add_switch_branch_data(48,
                                       92,
                                       CodeSectionData(
                                           CodePositionData(5, 2), CodePositionData(18, 5)),
                                       [CaseData(18,
                                                 CaseType.CASE,
                                                 CodeSectionData(CodePositionData(21, 2),
                                                                 CodePositionData(21, 19)),
                                                 CodeSectionData(CodePositionData(22, 5), CodePositionData(25, 9)))])

    # add ternary-expression
    cid_manager.add_ternary_expression_data(882, 428, 381, CodeSectionData(
        CodePositionData(15, 10), CodePositionData(15, 16)),
        [ConditionPossibility(True, [ConditionResult(5, True)]),
         ConditionPossibility(False, [ConditionResult(5, False)])],
        [ConditionData(28, CodeSectionData(
            CodePositionData(15, 11), CodePositionData(15, 15)))],
        CodeSectionData(CodePositionData(15, 20), CodePositionData(15, 26)),
        CodeSectionData(CodePositionData(15, 30), CodePositionData(15, 42)))

    # add loop
    cid_manager.add_loop_data(841,
                              LoopType.FOR,
                              32,
                              48,
                              CodeSectionData(
                                  CodePositionData(19, 2),
                                  CodePositionData(19, 17)),
                              CodeSectionData(
                                  CodePositionData(20, 2),
                                  CodePositionData(25, 3)),
                              [ConditionPossibility(True, [ConditionResult(5, True)]),
                                  ConditionPossibility(False, [ConditionResult(5, False)])],
                              [ConditionData(29, CodeSectionData(
                                  CodePositionData(19, 3), CodePositionData(19, 16)))])

    # load JSON Validation Schema
    with open(os.path.join(os.path.dirname(__file__), 'CID_Schema.json'), 'r') as cid_schema_ptr:
        json_schema = json.loads(cid_schema_ptr.read())

    # write non-compressed and check
    mock_config.nocomp_cid = True
    cid_manager.write_cid_file()

    with open(tmpdir.join('test_file.cid'), 'r') as output_cid_ptr:
        cid_data = json.loads(output_cid_ptr.read())

    # validate the CID-File
    jsonschema.validate(cid_data, json_schema)

    # write compressed and check
    mock_config.nocomp_cid = False
    cid_manager.write_cid_file()

    with gzip.GzipFile(tmpdir.join('test_file.cid'), 'r') as output_cid_ptr:
        cid_data = json.loads(output_cid_ptr.read())

    # validate the compressed CID-File
    jsonschema.validate(cid_data, json_schema)
