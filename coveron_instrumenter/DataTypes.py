#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Custom type definitions for Coveron Instrumenter.
"""

from typing import List
from enum import Enum
from json import JSONEncoder

import re
import os

# SECTION   CustomJSONEncoder class


class CustomJSONEncoder(JSONEncoder):
    """CustomJSONEncoder class.
       Builds a bridge between the JSONEncoder and the custom classes
    """

    # SECTION   CustomJSONEncoder private attribute definitions
    # !SECTION

    # SECTION   CustomJSONEncoder public attribute definitions
    # !SECTION

    # SECTION   CustomJSONEncoder initialization
    # Not used, since child from JSONEncoder
    # !SECTION

    # SECTION   CustomJSONEncoder getter functions
    # !SECTION

    # SECTION   CustomJSONEncoder setter functions
    # !SECTION

    # SECTION   CustomJSONEncoder property definitions
    # !SECTION

    # SECTION   CustomJSONEncoder private functions
    # !SECTION

    # SECTION   CustomJSONEncoder public functions
    def default(self, obj):
        if hasattr(obj, 'as_json'):
            return obj.as_json()
        else:
            return JSONEncoder.default(self, obj)
    # !SECTION
# !SECTION


# SECTION   Enums

# SECTION   EvaluationType
class EvaluationType(int, Enum):
    """Enum for the type of a marker"""
    DECISION = 1
    CONDITION = 2
# !SECTION


# SECTION   FunctionType
class FunctionType(int, Enum):
    '''Enum for the type of a class'''
    NORMAL = 1
    CONSTRUCTOR = 2
    DESTRUCTOR = 3
# !SECTION


# SECTION    StatementType
class StatementType(int, Enum):
    '''Enum for the type of a function'''
    NORMAL = 1
    RETURN = 2
    BREAK = 3
    CONTINUE = 4
    GOTO = 5
# !SECTION


# SECTION   CaseType
class CaseType(int, Enum):
    '''Enum for the type of a case'''
    CASE = 1
    DEFAULT = 2
# !SECTION


# SECTION   LoopType
class LoopType(int, Enum):
    '''Enum for the type of a loop'''
    FOR = 1
    WHILE = 2
    DOWHILE = 3
# !SECTION

# !SECTION


# SECTION   SourceFile class
class SourceFile:
    """SourceFile class.
       Contains all information about a source file passed to the instrumenter
    """

    # SECTION   SourceFile private attribute definitions
    __slots__ = ['_input_file', '_output_file', '_cid_file', '_cri_file']

    _input_file: str
    _output_file: str
    _cid_file: str
    _cri_file: str
    # !SECTION

    # SECTION   SourceFile public attribute definitions
    # !SECTION

    # SECTION   SourceFile initialization
    def __init__(self, source_file: str):
        # set input_file
        self._input_file = os.path.abspath(source_file).replace("\\\\", "\\")

        # determine instrumented source name and cid name
        self._output_file = self._input_file[0:self._input_file.rindex(
            '.') + 1] + "instr." + self._input_file[self._input_file.rindex(
                '.') + 1:]

        # determine cid file, this is only the relative path!
        self._cid_file = (
            os.path.basename(self._input_file)[
                0:os.path.basename(self._input_file).rindex('.') + 1] + "cid")

        # determine cri file, this is only the relative path!
        self._cri_file = (
            os.path.basename(self._input_file)[
                0:os.path.basename(self._input_file).rindex('.') + 1] + "cri")
        return
    # !SECTION

    # SECTION   SourceFile getter functions
    def _get_input_file(self) -> str:
        return self._input_file

    def _get_output_file(self) -> str:
        return self._output_file

    def _get_cid_file(self) -> str:
        return self._cid_file

    def _get_cri_file(self) -> str:
        return self._cri_file
    # !SECTION

    # SECTION   SourceFile setter functions
    # !SECTION

    # SECTION   SourceFile property definitions
    input_file: str = property(fget=_get_input_file,
                               doc="Stores the input file path of the source file")
    output_file: str = property(fget=_get_output_file,
                                doc="Stores the output file path of the instrumented source file")
    cid_file: str = property(fget=_get_cid_file,
                             doc="Stores the output file path of the CID file")
    cri_file: str = property(fget=_get_cri_file,
                             doc="Stores the output file path of the CRI file")
    # !SECTION

    # SECTION   SourceFile private functions
    # !SECTION

    # SECTION   SourceFile public functions
    # !SECTION
# !SECTION


# SECTION    SourceCode class
SourceCode = str
#!SECTION


# SECTION   CodePositionData class
class CodePositionData:
    """CodePositionData class.
       Stores the information about a code position.
    """

    # SECTION   CodePositionData private attribute definitions
    __slots__ = ["_line", "_column"]

    _line: int
    _column: int
    # !SECTION

    # SECTION   CodePositionData public attribute definitions
    # !SECTION

    # SECTION   CodePositionData initialization
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column
        return
    # !SECTION

    # SECTION   CodePositionData getter functions
    def _get_line(self) -> int:
        return self._line

    def _get_column(self) -> int:
        return self._column
    # !SECTION

    # SECTION   CodePositionData setter functions
    def _set_line(self, line: int):
        if line is None:
            raise ValueError("line can't be none")
        elif not isinstance(line, int):
            raise TypeError("line shall be of type int")
        elif line < 1:
            raise ValueError("line can't be smaller than 1")
        else:
            self._line = line

    def _set_column(self, column: int):
        if column is None:
            raise ValueError("column can't be none")
        elif not isinstance(column, int):
            raise TypeError("column shall be of type int")
        elif column < 1:
            raise ValueError("column can't be smaller than 1")
        else:
            self._column = column
    # !SECTION

    # SECTION   CodePositionData property definitions
    line: int = property(fget=_get_line,
                         fset=_set_line,
                         doc="Stores the line of the code position data")
    column: int = property(fget=_get_column,
                           fset=_set_column,
                           doc="Stores the column of the code position data")
    # !SECTION

    # SECTION   CodePositionData private functions
    def __eq__(self, other):
        if (self.line == other.line and
                self.column == other.column):
            return True
        else:
            return False
    # !SECTION

    # SECTION   CodePositionData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            line=self.line,
            column=self.column
        )
    # !SECTION
# !SECTION


# SECTION   CodeSectionData class
class CodeSectionData:
    """CodeSectionData class.
       Stores the information of a code section.
    """

    # SECTION   CodeSectionData private attribute definitions
    __slots__ = ["start_position", "end_position"]

    start_position: CodePositionData
    end_position: CodePositionData
    # !SECTION

    # SECTION   CodeSectionData public attribute definitions
    # !SECTION

    # SECTION   CodeSectionData initialization
    def __init__(self, start_position: CodePositionData, end_position: CodePositionData):
        self.start_position = start_position
        self.end_position = end_position
        return
    # !SECTION

    # SECTION   CodeSectionData getter functions
    # !SECTION

    # SECTION   CodeSectionData setter functions
    # !SECTION

    # SECTION   CodeSectionData property definitions
    # !SECTION

    # SECTION   CodeSectionData private functions
    def __eq__(self, other):
        if self.start_position != other.start_position or self.end_position != other.end_position:
            return False
        return True
    # !SECTION

    # SECTION   CodeSectionData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            start_line=self.start_position.line,
            start_column=self.start_position.column,
            end_line=self.end_position.line,
            end_column=self.end_position.column
        )
    # !SECTION
# !SECTION


# SECTION   CheckpointMarkerData class
class CheckpointMarkerData:
    """CheckpointMarkerData class.
       Stores the information about a checkpoint marker
    """

    # SECTION   CheckpointMarkerData private attribute definitions
    __slots__ = ["checkpoint_marker_id", "code_position"]

    checkpoint_marker_id: int
    code_position: CodePositionData
    # !SECTION

    # SECTION   CheckpointMarkerData public attribute definitions
    # !SECTION

    # SECTION   CheckpointMarkerData initialization
    def __init__(self, checkpoint_marker_id: int, code_position: CodePositionData):
        self.checkpoint_marker_id = checkpoint_marker_id
        self.code_position = code_position
        return
    # !SECTION

    # SECTION   CheckpointMarkerData getter functions
    # !SECTION

    # SECTION   CheckpointMarkerData setter functions
    # !SECTION

    # SECTION   CheckpointMarkerData property definitions
    # !SECTION

    # SECTION   CheckpointMarkerData private functions
    # !SECTION

    # SECTION   CheckpointMarkerData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            checkpoint_marker_id=self.checkpoint_marker_id,
            code_position=self.code_position
        )
    # !SECTION
# !SECTION


# SECTION   EvaluationMarkerData class
class EvaluationMarkerData:
    """EvaluationMarkerData class.
       Stores the information about a evaluation marker
    """

    # SECTION   EvaluationMarkerData private attribute definitions
    __slots__ = ["evaluation_marker_id", "evaluation_type", "code_section"]

    evaluation_marker_id: int
    evaluation_type: EvaluationType
    code_section: CodeSectionData
    # !SECTION

    # SECTION   EvaluationMarkerData public attribute definitions
    # !SECTION

    # SECTION   EvaluationMarkerData initialization
    def __init__(self, evaluation_marker_id: int,
                 evaluation_type: EvaluationType,
                 code_section: CodeSectionData):
        self.evaluation_marker_id = evaluation_marker_id
        self.evaluation_type = evaluation_type
        self.code_section = code_section
        return
    # !SECTION

    # SECTION   EvaluationMarkerData getter functions
    # !SECTION

    # SECTION   EvaluationMarkerData setter functions
    # !SECTION

    # SECTION   EvaluationMarkerData property definitions
    # !SECTION

    # SECTION   EvaluationMarkerData private functions
    # !SECTION

    # SECTION   EvaluationMarkerData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            evaluation_marker_id=self.evaluation_marker_id,
            evaluation_type=self.evaluation_type,
            code_section=self.code_section
        )
    # !SECTION
# !SECTION


# SECTION   MarkerData class
class MarkerData:
    """MarkerData class.
       Stores all markers
    """

    # SECTION   MarkerData private attribute definitions
    __slots__ = ["checkpoint_markers", "evaluation_markers"]

    checkpoint_markers: List[CheckpointMarkerData]
    evaluation_markers: List[EvaluationMarkerData]
    # !SECTION

    # SECTION   MarkerData public attribute definitions
    # !SECTION

    # SECTION   MarkerData initialization
    def __init__(self):
        self.checkpoint_markers = list()
        self.evaluation_markers = list()
        return
    # !SECTION

    # SECTION   MarkerData getter functions
    # !SECTION

    # SECTION   MarkerData setter functions
    # !SECTION

    # SECTION   MarkerData property definitions
    # !SECTION

    # SECTION   MarkerData private functions
    # !SECTION

    # SECTION   MarkerData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            checkpoint_markers=self.checkpoint_markers,
            evaluation_markers=self.evaluation_markers
        )
    # !SECTION
# !SECTION


# SECTION   ConditionResult class
class ConditionResult:
    """ConditionResult class.
       Condition result. Stores marker id and result
    """

    # SECTION   ConditionResult private attribute definitions
    __slots__ = ["evaluation_marker_id", "condition_result"]

    evaluation_marker_id: int
    condition_result: bool
    # !SECTION

    # SECTION   ConditionResult public attribute definitions
    # !SECTION

    # SECTION   ConditionResult initialization
    def __init__(self, evaluation_marker_id: int, condition_result: bool):
        self.evaluation_marker_id = evaluation_marker_id
        self.condition_result = condition_result
        return
    # !SECTION

    # SECTION   ConditionResult getter functions
    # !SECTION

    # SECTION   ConditionResult setter functions
    # !SECTION

    # SECTION   ConditionResult property definitions
    # !SECTION

    # SECTION   ConditionResult private functions
    # !SECTION

    # SECTION   ConditionResult public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            evaluation_marker_id=self.evaluation_marker_id,
            condition_result=self.condition_result
        )
    # !SECTION
# !SECTION


# SECTION   ConditionPossibility class
class ConditionPossibility:
    """ConditionPossibility class.
       Stores possible condition combinations for true or false decision result
    """

    # SECTION   ConditionPossibility private attribute definitions
    __slots__ = ["decision_result", "condition_combination"]

    decision_result: bool
    condition_combination: List[ConditionResult]
    # !SECTION

    # SECTION   ConditionPossibility public attribute definitions
    # !SECTION

    # SECTION   ConditionPossibility initialization
    def __init__(self, decision_result: bool, condition_combination: List[ConditionResult]):
        self.decision_result = decision_result
        self.condition_combination = condition_combination
        return
    # !SECTION

    # SECTION   ConditionPossibility getter functions
    # !SECTION

    # SECTION   ConditionPossibility setter functions
    # !SECTION

    # SECTION   ConditionPossibility property definitions
    # !SECTION

    # SECTION   ConditionPossibility private functions
    # !SECTION

    # SECTION   ConditionPossibility public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            decision_result=self.decision_result,
            condition_combination=self.condition_combination
        )
    # !SECTION
# !SECTION


# SECTION   ConditionData class
class ConditionData:
    """ConditionData class.
       Stores the information for a condition inside a decision (if-branches and loops)
    """

    # SECTION   ConditionData private attribute definitions
    __slots__ = ["evaluation_marker_id", "code_section"]

    evaluation_marker_id: int
    code_section: CodeSectionData
    # !SECTION

    # SECTION   ConditionData public attribute definitions
    # !SECTION

    # SECTION   ConditionData initialization
    def __init__(self, evaluation_marker_id: int, code_section: CodeSectionData):
        self.evaluation_marker_id = evaluation_marker_id
        self.code_section = code_section
        return
    # !SECTION

    # SECTION   ConditionData getter functions
    # !SECTION

    # SECTION   ConditionData setter functions
    # !SECTION

    # SECTION   ConditionData property definitions
    # !SECTION

    # SECTION   ConditionData private functions
    # !SECTION

    # SECTION   ConditionData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            evaluation_marker_id=self.evaluation_marker_id,
            code_section=self.code_section
        )
    # !SECTION
# !SECTION


# SECTION   CaseData class
class CaseData:
    """CaseData class.
       Stores the information of a case in a switch branch
    """

    # SECTION   CaseData private attribute definitions
    __slots__ = ["checkpoint_marker_id", "case_type", "evaluation_code_section",
                 "body_code_section"]

    checkpoint_marker_id: int
    case_type: CaseType
    evaluation_code_section: CodeSectionData
    body_code_section: CodeSectionData
    # !SECTION

    # SECTION   CaseData public attribute definitions
    # !SECTION

    # SECTION   CaseData initialization
    def __init__(self, checkpoint_marker_id: int, case_type: CaseType, evaluation_code_section: CodeSectionData, body_code_section: CodeSectionData):
        self.checkpoint_marker_id = checkpoint_marker_id
        self.case_type = case_type
        self.evaluation_code_section = evaluation_code_section
        self.body_code_section = body_code_section
        return
    # !SECTION

    # SECTION   CaseData getter functions
    # !SECTION

    # SECTION   CaseData setter functions
    # !SECTION

    # SECTION   CaseData property definitions
    # !SECTION

    # SECTION   CaseData private functions
    # !SECTION

    # SECTION   CaseData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            checkpoint_marker_id=self.checkpoint_marker_id,
            case_type=self.case_type,
            evaluation_code_section=self.evaluation_code_section,
            body_code_section=self.body_code_section
        )
    # !SECTION
# !SECTION


# SECTION   BranchResultData class
class BranchResultData:
    """BranchResultData class.
       Stores the information for a branch result (if branch)
    """

    # SECTION   BranchResultData private attribute definitions
    __slots__ = ["evaluation_marker_id", "condition_possibilities", "conditions",
                 "result_evaluation_code_section", "result_body_code_section"]

    evaluation_marker_id: int
    condition_possibilities: List[ConditionPossibility]
    conditions: List[ConditionData]
    result_evaluation_code_section: CodeSectionData
    result_body_code_section: CodeSectionData
    # !SECTION

    # SECTION   BranchResultData public attribute definitions
    # !SECTION

    # SECTION   BranchResultData initialization
    def __init__(self, evaluation_marker_id: int,
                 condition_possibilities: List[ConditionPossibility],
                 conditions: List[ConditionData],
                 result_evaluation_code_section: CodeSectionData,
                 result_body_code_section: CodeSectionData):
        self.evaluation_marker_id = evaluation_marker_id
        self.condition_possibilities = condition_possibilities
        self.conditions = conditions
        self.result_evaluation_code_section = result_evaluation_code_section
        self.result_body_code_section = result_body_code_section
        return
    # !SECTION

    # SECTION   BranchResultData getter functions
    # !SECTION

    # SECTION   BranchResultData setter functions
    # !SECTION

    # SECTION   BranchResultData private functions
    # !SECTION

    # SECTION   BranchResultData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            evaluation_marker_id=self.evaluation_marker_id,
            condition_possibilities=self.condition_possibilities,
            conditions=self.conditions,
            result_evaluation_code_section=self.result_evaluation_code_section,
            result_body_code_section=self.result_body_code_section
        )
    # !SECTION
# !SECTION


# SECTION   ClassData class
class ClassData:
    """ClassData class.
       Stores the code information about a class.
    """

    # SECTION   ClassData private attribute definitions
    __slots__ = ["class_id", "class_name"]

    class_id: int
    class_name: str
    # !SECTION

    # SECTION   ClassData public attribute definitions
    # !SECTION

    # SECTION   ClassData initialization
    def __init__(self, class_id: int, class_name: str):
        self.class_id = class_id
        self.class_name = class_name
        return
    # !SECTION

    # SECTION   ClassData getter functions
    # !SECTION

    # SECTION   ClassData setter functions
    # !SECTION

    # SECTION   ClassData property definitions
    # !SECTION

    # SECTION   ClassData private functions
    # !SECTION

    # SECTION   ClassData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            class_id=self.class_id,
            class_name=self.class_name
        )
    # !SECTION
# !SECTION


# SECTION   FunctionData class
class FunctionData:
    """FunctionData class.
       Stores the code information about a function.
    """

    # SECTION   FunctionData private attribute definitions
    __slots__ = ["function_id", "function_name", "function_type",
                 "parent_function_id", "checkpoint_marker_id",
                 "header_code_section", "inner_code_section"]

    function_id: int
    function_name: str
    function_type: FunctionType
    parent_function_id: int
    checkpoint_marker_id: int
    header_code_section: CodeSectionData
    inner_code_section: CodeSectionData
    # !SECTION

    # SECTION   FunctionData public attribute definitions
    # !SECTION

    # SECTION   FunctionData initialization
    def __init__(self, function_id: int, function_name: str,
                 function_type: FunctionType, parent_function_id: int,
                 checkpoint_marker_id: int, header_code_section: CodeSectionData,
                 inner_code_section: CodeSectionData):
        self.function_id = function_id
        self.function_name = function_name
        self.function_type = function_type
        self.parent_function_id = parent_function_id
        self.checkpoint_marker_id = checkpoint_marker_id
        self.header_code_section = header_code_section
        self.inner_code_section = inner_code_section
        return
    # !SECTION

    # SECTION   FunctionData getter functions
    # !SECTION

    # SECTION   FunctionData setter functions
    # !SECTION

    # SECTION   FunctionData property definitions
    # !SECTION

    # SECTION   FunctionData private functions
    # !SECTION

    # SECTION   FunctionData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            function_id=self.function_id,
            function_name=self.function_name,
            function_type=self.function_type,
            parent_function_id=self.parent_function_id,
            checkpoint_marker_id=self.checkpoint_marker_id,
            header_code_section=self.header_code_section,
            inner_code_section=self.inner_code_section
        )
    # !SECTION
# !SECTION


# SECTION   StatementData class
class StatementData:
    """StatementData class.
       Stores the code information about a statement.
    """

    # SECTION   StatementData private attribute definitions
    __slots__ = ["statement_id", "statement_type", "function_id", "checkpoint_marker_id",
                 "code_section"]

    statement_id: int
    statement_type: StatementType
    function_id: int
    checkpoint_marker_id: int
    code_section: CodeSectionData
    # !SECTION

    # SECTION   StatementData public attribute definitions
    # !SECTION

    # SECTION   StatementData initialization
    def __init__(self, statement_id: int, statement_type: StatementType,
                 function_id: int, checkpoint_marker_id: int, code_section: CodeSectionData):
        self.statement_id = statement_id
        self.statement_type = statement_type
        self.function_id = function_id
        self.checkpoint_marker_id = checkpoint_marker_id
        self.code_section = code_section
        return
    # !SECTION

    # SECTION   StatementData getter functions
    # !SECTION

    # SECTION   StatementData setter functions
    # !SECTION

    # SECTION   StatementData property definitions
    # !SECTION

    # SECTION   StatementData private functions
    # !SECTION

    # SECTION   StatementData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            statement_id=self.statement_id,
            statement_type=self.statement_type,
            function_id=self.function_id,
            checkpoint_marker_id=self.checkpoint_marker_id,
            code_section=self.code_section
        )
    # !SECTION
# !SECTION


# SECTION   IfBranchData class
class IfBranchData:
    """IfBranchData class.
       Stores the code information about a if branch.
    """

    # SECTION   IfBranchData private attribute definitions
    __slots__ = ["if_branch_id", "function_id", "branch_results"]

    if_branch_id: int
    function_id: int
    branch_results: List[BranchResultData]
    # !SECTION

    # SECTION   IfBranchData public attribute definitions
    # !SECTION

    # SECTION   IfBranchData initialization
    def __init__(self, if_branch_id: int, function_id: int, branch_results: List[BranchResultData]):
        self.if_branch_id = if_branch_id
        self.function_id = function_id
        self.branch_results = branch_results
        return
    # !SECTION

    # SECTION   IfBranchData getter functions
    # !SECTION

    # SECTION   IfBranchData setter functions
    # !SECTION

    # SECTION   IfBranchData property definitions
    # !SECTION

    # SECTION   IfBranchData private functions
    # !SECTION

    # SECTION   IfBranchData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            if_branch_id=self.if_branch_id,
            function_id=self.function_id,
            branch_results=self.branch_results
        )
    # !SECTION
# !SECTION


# SECTION   SwitchBranchData class
class SwitchBranchData:
    """SwitchBranchData class.
       Stores the code information about a switch branch.
    """

    # SECTION   SwitchBranchData private attribute definitions
    __slots__ = ["switch_branch_id", "function_id",
                 "switch_branch_code_section", "cases"]

    switch_branch_id: int
    function_id: int
    switch_branch_code_section: CodeSectionData
    cases: List[CaseData]
    # !SECTION

    # SECTION   SwitchBranchData public attribute definitions
    # !SECTION

    # SECTION   SwitchBranchData initialization
    def __init__(self, switch_branch_id: int, function_id: int,
                 switch_branch_code_section: CodeSectionData, cases: List[CaseData]):
        self.switch_branch_id = switch_branch_id
        self.function_id = function_id
        self.switch_branch_code_section = switch_branch_code_section
        self.cases = cases
        return
    # !SECTION

    # SECTION   SwitchBranchData getter functions
    # !SECTION

    # SECTION   SwitchBranchData setter functions
    # !SECTION

    # SECTION   SwitchBranchData property definitions
    # !SECTION

    # SECTION   SwitchBranchData private functions
    # !SECTION

    # SECTION   SwitchBranchData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            switch_branch_id=self.switch_branch_id,
            function_id=self.function_id,
            switch_branch_code_section=self.switch_branch_code_section,
            cases=self.cases
        )
    # !SECTION
# !SECTION


# SECTION   TernaryExpressionData class
class TernaryExpressionData:
    """TernaryExpressionData class.
       Stores information about a ternary expression
    """

    # SECTION   TernaryExpressionData private attribute definitions
    __slots__ = ["ternary_expression_id", "function_id", "evaluation_marker_id",
                 "evaluation_code_section", "condition_possibilities", "conditions",
                 "true_code_section", "false_code_section"]

    ternary_expression_id: int
    function_id: int
    evaluation_marker_id: int
    evaluation_code_section: CodeSectionData
    condition_possibilities: List[ConditionPossibility]
    conditions: ConditionData
    true_code_section: CodeSectionData
    false_code_section: CodeSectionData
    # !SECTION

    # SECTION   TernaryExpressionData public attribute definitions
    # !SECTION

    # SECTION   TernaryExpressionData initialization
    def __init__(self, ternary_expression_id: int, function_id: int, evaluation_marker_id: int,
                 evaluation_code_section: CodeSectionData, condition_possibilities: List[ConditionPossibility],
                 conditions: ConditionData,
                 true_code_section: CodeSectionData, false_code_section: CodeSectionData):
        self.ternary_expression_id = ternary_expression_id
        self.function_id = function_id
        self.evaluation_marker_id = evaluation_marker_id
        self.evaluation_code_section = evaluation_code_section
        self.condition_possibilities = condition_possibilities
        self.conditions = conditions
        self.true_code_section = true_code_section
        self.false_code_section = false_code_section
        return
    # !SECTION

    # SECTION   TernaryExpressionData getter functions
    # !SECTION

    # SECTION   TernaryExpressionData setter functions
    # !SECTION

    # SECTION   TernaryExpressionData property definitions
    # !SECTION

    # SECTION   TernaryExpressionData private functions
    # !SECTION

    # SECTION   TernaryExpressionData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            ternary_expression_id=self.ternary_expression_id,
            function_id=self.function_id,
            evaluation_marker_id=self.evaluation_marker_id,
            evaluation_code_section=self.evaluation_code_section,
            condition_possibilities=self.condition_possibilities,
            conditions=self.conditions,
            true_code_section=self.true_code_section,
            false_code_section=self.false_code_section
        )
    # !SECTION
# !SECTION


# SECTION   LoopData class
class LoopData:
    """LoopData class.
       Stores the code information about a loop.
    """

    # SECTION   LoopData private attribute definitions
    __slots__ = ["loop_id", "loop_type", "function_id",
                 "evaluation_marker_id", "evaluation_code_section", "body_code_section",
                 "condition_possibilities", "conditions"]

    loop_id: int
    loop_type: LoopType
    function_id: int
    evaluation_marker_id: int
    evaluation_code_section: CodeSectionData
    body_code_section: CodeSectionData
    condition_possibilities: List[ConditionPossibility]
    conditions: List[ConditionData]
    # !SECTION

    # SECTION   LoopData public attribute definitions
    # !SECTION

    # SECTION   LoopData initialization
    def __init__(self, loop_id: int, loop_type: LoopType, function_id: int,
                 evaluation_marker_id: int, evaluation_code_section: CodeSectionData,
                 body_code_section: CodeSectionData, condition_possibilities: List[ConditionPossibility],
                 conditions: List[ConditionData]):
        self.loop_id = loop_id
        self.loop_type = loop_type
        self.function_id = function_id
        self.evaluation_marker_id = evaluation_marker_id
        self.evaluation_code_section = evaluation_code_section
        self.body_code_section = body_code_section
        self.condition_possibilities = condition_possibilities
        self.conditions = conditions
        return
    # !SECTION

    # SECTION   LoopData getter functions
    # !SECTION

    # SECTION   LoopData setter functions
    # !SECTION

    # SECTION   LoopData property definitions
    # !SECTION

    # SECTION   LoopData private functions
    # !SECTION

    # SECTION   LoopData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            loop_id=self.loop_id,
            loop_type=self.loop_type,
            function_id=self.function_id,
            evaluation_marker_id=self.evaluation_marker_id,
            evaluation_code_section=self.evaluation_code_section,
            body_code_section=self.body_code_section,
            condition_possibilities=self.condition_possibilities,
            conditions=self.conditions
        )
    # !SECTION
# !SECTION


# SECTION   CodeData class
class CodeData:
    """CodeData class.
       Stores all information about the parsed code
    """

    # SECTION   CodeData private attribute definitions
    __slots__ = ["classes", "functions", "statements", "if_branches",
                 "switch_branches", "ternary_expressions", "loops"]

    classes: List[ClassData]
    functions: List[FunctionData]
    statements: List[StatementData]
    if_branches: List[IfBranchData]
    switch_branches: List[SwitchBranchData]
    ternary_expressions: List[TernaryExpressionData]
    loops: List[LoopData]
    # !SECTION

    # SECTION   CodeData public attribute definitions
    # !SECTION

    # SECTION   CodeData initialization
    def __init__(self):
        self.classes = list()
        self.functions = list()
        self.statements = list()
        self.if_branches = list()
        self.switch_branches = list()
        self.ternary_expressions = list()
        self.loops = list()
        return
    # !SECTION

    # SECTION   CodeData getter functions
    # !SECTION

    # SECTION   CodeData setter functions
    # !SECTION

    # SECTION   CodeData property definitions
    # !SECTION

    # SECTION   CodeData private functions
    # !SECTION

    # SECTION   CodeData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            classes=self.classes,
            functions=self.functions,
            statements=self.statements,
            if_branches=self.if_branches,
            switch_branches=self.switch_branches,
            ternary_expressions=self.ternary_expressions,
            loops=self.loops
        )
    # !SECTION
# !SECTION


# SECTION   CIDData class
class CIDData:
    """CIDData class.
       Stores the data of a "Coveron Instrumentation Data" object.
    """

    # SECTION   CIDData private attribute definitions
    __slots__ = ['source_code_path', 'source_code_hash', 'source_code_base64',
                 'instrumentation_random', 'cri_path', 'checkpoint_markers_enabled',
                 'evaluation_markers_enabled',
                 'marker_data', 'code_data']

    source_code_path: str
    source_code_hash: str
    source_code_base64: str
    instrumentation_random: str
    cri_path: str
    checkpoint_markers_enabled: bool
    evaluation_markers_enabled: bool
    marker_data: MarkerData
    code_data: CodeData
    # !SECTION

    # SECTION   CIDData public attribute definitions
    # !SECTION

    # SECTION   CIDData initialization
    def __init__(self,
                 source_code_path: str,
                 source_code_hash: str,
                 source_code_base64: str,
                 instrumentation_random: str,
                 cri_path: str,
                 checkpoint_markers_enabled: bool,
                 evaluation_markers_enabled: bool):
        self.source_code_path = source_code_path
        self.source_code_hash = source_code_hash
        self.source_code_base64 = source_code_base64
        self.instrumentation_random = instrumentation_random
        self.cri_path = cri_path
        self.checkpoint_markers_enabled = checkpoint_markers_enabled
        self.evaluation_markers_enabled = evaluation_markers_enabled
        self.marker_data = MarkerData()
        self.code_data = CodeData()
        return
    # !SECTION

    # SECTION   CIDData getter functions
    # !SECTION

    # SECTION   CIDData setter functions
    # !SECTION

    # SECTION   CIDData property definitions
    # !SECTION

    # SECTION   CIDData private functions
    # !SECTION

    # SECTION   CIDData public functions
    def as_json(self):
        # JSON encoding helper
        return dict(
            source_code_path=self.source_code_path,
            source_code_hash=self.source_code_hash,
            source_code_base64=self.source_code_base64,
            instrumentation_random=self.instrumentation_random,
            cri_path=self.cri_path,
            checkpoint_markers_enabled=self.checkpoint_markers_enabled,
            evaluation_markers_enabled=self.evaluation_markers_enabled,
            marker_data=self.marker_data,
            code_data=self.code_data
        )
    # !SECTION
# !SECTION
