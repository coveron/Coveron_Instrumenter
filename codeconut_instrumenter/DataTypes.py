#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Custom type definitions for Codeconut Instrumenter.
"""

from typing import List
from enum import Enum

import re

# SECTION   Enums

# SECTION   EvaluationType
class EvaluationType(Enum):
    """Enum for the type of a marker"""
    DECISION = 1
    CONDITION = 2
# !SECTION

# SECTION   FunctionType
class FunctionType(Enum):
    '''Enum for the type of a class'''
    NORMAL = 1
    CONSTRUCTOR = 2
    DESTRUCTOR = 3
# !SECTION

# SECTION    StatementType
class StatementType(Enum):
    '''Enum for the type of a function'''
    NORMAL = 1
# !SECTION

# SECTION   CaseType
class CaseType(Enum):
    '''Enum for the type of a case'''
    CASE = 1
    DEFAULT = 2
# !SECTION

# SECTION   LoopType
class LoopType(Enum):
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
    __slots__ = ['_input_filename', '_output_filename', '_cid_filename']

    _input_filename: str
    _output_filename: str
    _cid_filename: str
    # !SECTION
    
    # SECTION   SourceFile public attribute definitions
    # !SECTION
    
    # SECTION   SourceFile initialization
    def __init__(self, source_file: str):
        # set input_filename
        self.input_filename = source_file

        # determine instrumented source name and cid name
        self._output_filename = source_file[0:source_file.rindex(
            '.')+1] + "instr." + source_file[source_file.rindex(
                '.')+1:]

        # determine cid filename
        self._cid_filename = self.output_filename[0:self.output_filename.rindex(
            '.')+1] + "cid"
        return
    # !SECTION
    
    # SECTION   SourceFile getter functions
    def _get_input_filename(self) -> str:
        return self._input_filename

    def _get_output_filename(self) -> str:
        return self._output_filename

    def _get_cid_filename(self) -> str:
        return self._cid_filename
    # !SECTION
    
    # SECTION   SourceFile setter functions
    def _set_input_filename(self, input_filename:str):
        if input_filename is None:
            raise ValueError("input_filename can't be none")
        elif not isinstance(input_filename, str):
            raise TypeError("input_filename shall be of type str")
        else:
            self._input_filename = input_filename
    # !SECTION
    
    # SECTION   SourceFile property definitions
    input_filename: str = property(fget=_get_input_filename,
                  fset=_set_input_filename,
                  doc="Stores the input filename of the source file")
    output_filename: str = property(fget=_get_output_filename,
                  doc="Stores the output filename of the instrumented source file")
    cid_filename: str = property(fget=_get_cid_filename,
                  doc="Stores the output filename of the cid file")
    # !SECTION
    
    # SECTION   SourceFile private functions
    # !SECTION
    
    # SECTION   SourceFile public functions
    # !SECTION
# !SECTION

#SECTION    SourceCode class
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
    def _set_line(self, line:int):
        if line is None:
            raise ValueError("line can't be none")
        elif not isinstance(line, int):
            raise TypeError("line shall be of type int")
        elif line < 1:
            raise ValueError("line can't be smaller than 1")
        else:
            self._line = line

    def _set_column(self, column:int):
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
    # !SECTION
    
    # SECTION   CodePositionData public functions
    # !SECTION
# !SECTION

# SECTION   CodeSectionData class
class CodeSectionData:
    """CodeSectionData class.
       Stores the information of a code section.
    """
    
    # SECTION   CodeSectionData private attribute definitions
    __slots__ = ["_start_position", "_end_position"]

    _start_position: CodePositionData
    _end_position: CodePositionData
    # !SECTION
    
    # SECTION   CodeSectionData public attribute definitions
    # !SECTION
    
    # SECTION   CodeSectionData initialization
    def __init__(self, start_position: CodePositionData, end_position: CodePositionData):
        if start_position is not None and isinstance(start_position, CodePositionData):
            self._start_position = start_position
        else:
            raise(RuntimeError("start_position is None or not of type CodePositionData"))

        if end_position is not None and isinstance(end_position, CodePositionData):
            self._end_position = end_position
        else:
            raise(RuntimeError("end_position is None or not of type CodePositionData"))
        return
    # !SECTION
    
    # SECTION   CodeSectionData getter functions
    def _get_start_line(self) -> int:
        return self._start_position.line

    def _get_start_column(self) -> int:
        return self._start_position.column

    def _get_end_line(self) -> int:
        return self._end_position.line

    def _get_end_column(self) -> int:
        return self._end_position.column
    # !SECTION
    
    # SECTION   CodeSectionData setter functions
    def _set_start_line(self, start_line:int):
        if start_line is None:
            raise ValueError("start_line can't be none")
        elif not isinstance(start_line, int):
            raise TypeError("start_line shall be of type int")
        else:
            self._start_position = CodePositionData(start_line, self._start_position.column)

    def _set_start_column(self, start_column:int):
        if start_column is None:
            raise ValueError("start_column can't be none")
        elif not isinstance(start_column, int):
            raise TypeError("start_column shall be of type int")
        else:
            self._start_position = CodePositionData(self._start_position.line, start_column)

    def _set_end_line(self, end_line:int):
        if end_line is None:
            raise ValueError("end_line can't be none")
        elif not isinstance(end_line, int):
            raise TypeError("end_line shall be of type int")
        else:
            self._end_position = CodePositionData(end_line, self._end_position.column)

    def _set_end_column(self, end_column:int):
        if end_column is None:
            raise ValueError("end_column can't be none")
        elif not isinstance(end_column, int):
            raise TypeError("end_column shall be of type int")
        else:
            self._end_position = CodePositionData(self._end_position.line, end_column)
    # !SECTION
    
    # SECTION   CodeSectionData property definitions
    start_line: int = property(fget=_get_start_line,
                  fset=_set_start_line,
                  doc="Stores the start line")
    start_column: int = property(fget=_get_start_column,
                  fset=_set_start_column,
                  doc="Stores the start column")
    end_line: int = property(fget=_get_end_line,
                  fset=_set_end_line,
                  doc="Stores the end line")
    end_column: int = property(fget=_get_end_column,
                  fset=_set_end_column,
                  doc="Stores the end column")
    # !SECTION
    
    # SECTION   CodeSectionData private functions
    # !SECTION
    
    # SECTION   CodeSectionData public functions
    # !SECTION
# !SECTION

# SECTION   CheckpointMarkerData class
class CheckpointMarkerData:
    """CheckpointMarkerData class.
       Stores the information about a checkpoint marker
    """
    
    # SECTION   CheckpointMarkerData private attribute definitions
    __slots__ = ["_checkpoint_marker_id", "_code_position"]

    _checkpoint_marker_id: int
    _code_position: CodePositionData
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
    def _get_checkpoint_marker_id(self) -> int:
        return self._checkpoint_marker_id

    def _get_code_position(self) -> CodePositionData:
        return self._code_position
    # !SECTION
    
    # SECTION   CheckpointMarkerData setter functions
    def _set_checkpoint_marker_id(self, checkpoint_marker_id:int):
        if checkpoint_marker_id is None:
            raise ValueError("checkpoint_marker_id can't be none")
        elif not isinstance(checkpoint_marker_id, int):
            raise TypeError("checkpoint_marker_id shall be of type int")
        else:
            self._checkpoint_marker_id = checkpoint_marker_id

    def _set_code_position(self, code_position:CodePositionData):
        if code_position is None:
            raise ValueError("code_position can't be none")
        elif not isinstance(code_position, CodePositionData):
            raise TypeError("code_position shall be of type CodePositionData")
        else:
            self._code_position = code_position
    # !SECTION
    
    # SECTION   CheckpointMarkerData property definitions
    checkpoint_marker_id: int = property(fget=_get_checkpoint_marker_id,
                fset=_set_checkpoint_marker_id,
                doc="Stores the ID of the checkpoint marker")
    code_position: CodePositionData = property(fget=_get_code_position,
                  fset=_set_code_position,
                  doc="Stores the position of the checkpoint marker")
    # !SECTION
    
    # SECTION   CheckpointMarkerData private functions
    # !SECTION
    
    # SECTION   CheckpointMarkerData public functions
    # !SECTION
# !SECTION

# SECTION   EvaluationMarkerData class
class EvaluationMarkerData:
    """EvaluationMarkerData class.
       Stores the information about a evaluation marker
    """
    
    # SECTION   EvaluationMarkerData private attribute definitions
    __slots__ = ["_evaluation_marker_id", "_evaluation_type", "_code_section"]

    _evaluation_marker_id: int
    _evaluation_type: EvaluationType
    _code_section: CodeSectionData
    # !SECTION
    
    # SECTION   EvaluationMarkerData public attribute definitions
    # !SECTION
    
    # SECTION   EvaluationMarkerData initialization
    def __init__(self, evaluation_marker_id: int, evaluation_type: EvaluationType, code_section: CodeSectionData):
        self.evaluation_marker_id = evaluation_marker_id
        self.evaluation_type = evaluation_type
        self.code_section = code_section
        return
    # !SECTION
    
    # SECTION   EvaluationMarkerData getter functions
    def _get_evaluation_marker_id(self) -> int:
        return self._evaluation_marker_id
    
    def _get_evaluation_type(self) -> EvaluationType:
        return self._evaluation_type
    
    def _get_code_section(self) -> CodeSectionData:
        return self._code_section
    # !SECTION
    
    # SECTION   EvaluationMarkerData setter functions
    def _set_evaluation_marker_id(self, evaluation_marker_id:int):
        if evaluation_marker_id is None:
            raise ValueError("evaluation_marker_id can't be none")
        elif not isinstance(evaluation_marker_id, int):
            raise TypeError("evaluation_marker_id shall be of type int")
        else:
            self._evaluation_marker_id = evaluation_marker_id

    def _set_evaluation_type(self, evaluation_type:EvaluationType):
        if evaluation_type is None:
            raise ValueError("evaluation_type can't be none")
        elif not isinstance(evaluation_type, EvaluationType):
            raise TypeError("evaluation_type shall be of type EvaluationType")
        else:
            self._evaluation_type = evaluation_type

    def _set_code_section(self, code_section:CodeSectionData):
        if code_section is None:
            raise ValueError("code_section can't be none")
        elif not isinstance(code_section, CodeSectionData):
            raise TypeError("code_section shall be of type CodeSectionData")
        else:
            self._code_section = code_section
    # !SECTION
    
    # SECTION   EvaluationMarkerData property definitions
    evaluation_marker_id: int = property(fget=_get_evaluation_marker_id,
                  fset=_set_evaluation_marker_id,
                  doc="Stores the ID of the evaluation marker")
    evaluation_type: EvaluationType = property(fget=_get_evaluation_type,
                  fset=_set_evaluation_type,
                  doc="Stores the type of the evaluation")
    code_section: CodeSectionData = property(fget=_get_code_section,
                  fset=_set_code_section,
                  doc="Stores the code section of the evaluation marker")
    # !SECTION
    
    # SECTION   EvaluationMarkerData private functions
    # !SECTION
    
    # SECTION   EvaluationMarkerData public functions
    # !SECTION
# !SECTION

# SECTION   MarkerData class
class MarkerData:
    """MarkerData class.
       Stores all markers
    """
    
    # SECTION   MarkerData private attribute definitions
    __slots__ = ["_checkpoint_markers", "_evaluation_markers"]

    _checkpoint_markers: List[CheckpointMarkerData]
    _evaluation_markers: List[EvaluationMarkerData]
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
    def _get_checkpoint_markers(self) -> List[CheckpointMarkerData]:
        return self._checkpoint_markers

    def _get_evaluation_markers(self) -> List[EvaluationMarkerData]:
        return self._evaluation_markers
    # !SECTION
    
    # SECTION   MarkerData setter functions
    def _set_checkpoint_markers(self, checkpoint_markers:List[CheckpointMarkerData]):
        if checkpoint_markers is None:
            raise ValueError("checkpoint_markers can't be none")
        elif not isinstance(checkpoint_markers, list):
            raise TypeError("checkpoint_markers shall be of type list")
        else:
            self._checkpoint_markers = checkpoint_markers

    def _set_evaluation_markers(self, evaluation_markers:List[EvaluationMarkerData]):
        if evaluation_markers is None:
            raise ValueError("evaluation_markers can't be none")
        elif not isinstance(evaluation_markers, list):
            raise TypeError("evaluation_markers shall be of type list")
        else:
            self._evaluation_markers = evaluation_markers
    # !SECTION
    
    # SECTION   MarkerData property definitions
    checkpoint_markers: List[CheckpointMarkerData] = property(fget=_get_checkpoint_markers,
                  fset=_set_checkpoint_markers,
                  doc="Stores all checkpoint markers")
    evaluation_markers: List[EvaluationMarkerData] = property(fget=_get_evaluation_markers,
                  fset=_set_evaluation_markers,
                  doc="Stores all evaluation markers")
    # !SECTION
    
    # SECTION   MarkerData private functions
    # !SECTION
    
    # SECTION   MarkerData public functions
    # !SECTION
# !SECTION

# SECTION   ConditionData class
class ConditionData:
    """ConditionData class.
       Stores the information for a condition inside a decision (if-branches and loops)
    """
    
    # SECTION   ConditionData private attribute definitions
    __slots__ = ["_evaluation_marker_id", "_code_section"]

    _evaluation_marker_id: int
    _code_section: CodeSectionData
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
    def _get_evaluation_marker_id(self) -> int:
        return self._evaluation_marker_id

    def _get_code_section(self) -> CodeSectionData:
        return self._code_section
    # !SECTION
    
    # SECTION   ConditionData setter functions
    def _set_evaluation_marker_id(self, evaluation_marker_id:int):
        if evaluation_marker_id is None:
            raise ValueError("evaluation_marker_id can't be none")
        elif not isinstance(evaluation_marker_id, int):
            raise TypeError("evaluation_marker_id shall be of type int")
        else:
            self._evaluation_marker_id = evaluation_marker_id

    def _set_code_section(self, code_section:CodeSectionData):
        if code_section is None:
            raise ValueError("code_section can't be none")
        elif not isinstance(code_section, CodeSectionData):
            raise TypeError("code_section shall be of type CodeSectionData")
        else:
            self._code_section = code_section
    # !SECTION
    
    # SECTION   ConditionData property definitions
    evaluation_marker_id: int = property(fget=_get_evaluation_marker_id,
                  fset=_set_evaluation_marker_id,
                  doc="Stores the ID of the corresponding evaluation marker")
    code_section: CodeSectionData = property(fget=_get_code_section,
                  fset=_set_code_section,
                  doc="Stores the code section of the condition")
    # !SECTION
    
    # SECTION   ConditionData private functions
    # !SECTION
    
    # SECTION   ConditionData public functions
    # !SECTION
# !SECTION

# SECTION   CaseData class
class CaseData:
    """CaseData class.
       Stores the information of a case in a switch branch
    """
    
    # SECTION   CaseData private attribute definitions
    __slots__ = ["_checkpoint_marker_id", "_case_type", "_evaluation_code_section",
                 "_body_code_section"]

    _checkpoint_marker_id: int
    _case_type: CaseType
    _evaluation_code_section: CodeSectionData
    _body_code_section: CodeSectionData
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
    def _get_checkpoint_marker_id(self) -> int:
        return self._checkpoint_marker_id

    def _get_case_type(self) -> CaseType:
        return self._case_type

    def _get_evaluation_code_section(self) -> CodeSectionData:
        return self._evaluation_code_section

    def _get_body_code_section(self) -> CodeSectionData:
        return self._body_code_section
    # !SECTION
    
    # SECTION   CaseData setter functions
    def _set_checkpoint_marker_id(self, checkpoint_marker_id:int):
        if checkpoint_marker_id is None:
            raise ValueError("checkpoint_marker_id can't be none")
        elif not isinstance(checkpoint_marker_id, int):
            raise TypeError("checkpoint_marker_id shall be of type int")
        else:
            self._checkpoint_marker_id = checkpoint_marker_id

    def _set_case_type(self, case_type:CaseType):
        if case_type is None:
            raise ValueError("case_type can't be none")
        elif not isinstance(case_type, CaseType):
            raise TypeError("case_type shall be of type CaseType")
        else:
            self._case_type = case_type

    def _set_evaluation_code_section(self, evaluation_code_section:CodeSectionData):
        if evaluation_code_section is None:
            raise ValueError("evaluation_code_section can't be none")
        elif not isinstance(evaluation_code_section, CodeSectionData):
            raise TypeError("evaluation_code_section shall be of type CodeSectionData")
        else:
            self._evaluation_code_section = evaluation_code_section
        
    def _set_body_code_section(self, body_code_section:CodeSectionData):
        if body_code_section is None:
            raise ValueError("body_code_section can't be none")
        elif not isinstance(body_code_section, CodeSectionData):
            raise TypeError("body_code_section shall be of type CodeSectionData")
        else:
            self._body_code_section = body_code_section
    # !SECTION
    
    # SECTION   CaseData property definitions
    checkpoint_marker_id: int = property(fget=_get_checkpoint_marker_id,
                  fset=_set_checkpoint_marker_id,
                  doc="Stores the ID of the corresponding checkpoint marker")
    case_type: CaseType = property(fget=_get_case_type,
                  fset=_set_case_type,
                  doc="Stores the type of the case")
    evaluation_code_section: CodeSectionData = property(fget=_get_evaluation_code_section,
                  fset=_set_evaluation_code_section,
                  doc="Stores the code section of the case evaluation")
    body_code_section: CodeSectionData = property(fget=_get_body_code_section,
                  fset=_set_body_code_section,
                  doc="Stoes the code section of the case body")
    # !SECTION
    
    # SECTION   CaseData private functions
    # !SECTION
    
    # SECTION   CaseData public functions
    # !SECTION
# !SECTION

# SECTION   BranchResultData class
class BranchResultData:
    """BranchResultData class.
       Stores the information for a branch result (if branch)
    """
    
    # SECTION   BranchResultData private attribute definitions
    __slots__ = ["_evaluation_marker_id", "_conditions", "_result_evaluation_code_section",
                 "_result_body_code_section"]

    _evaluation_marker_id: int
    _conditions: List[ConditionData]
    _result_evaluation_code_section: CodeSectionData
    _result_body_code_section: CodeSectionData
    # !SECTION
    
    # SECTION   BranchResultData public attribute definitions
    # !SECTION
    
    # SECTION   BranchResultData initialization
    def __init__(self, evaluation_marker_id: int, conditions: List[ConditionData],
            result_evaluation_code_section: CodeSectionData,
            result_body_code_section: CodeSectionData):
        self.evaluation_marker_id = evaluation_marker_id
        self.conditions = conditions
        self.result_evaluation_code_section = result_evaluation_code_section
        self.result_body_code_section = result_body_code_section
        return
    # !SECTION
    
    # SECTION   BranchResultData getter functions
    def _get_evaluation_marker_id(self) -> int:
        return self._evaluation_marker_id

    def _get_conditions(self) -> List[ConditionData]:
        return self._conditions

    def _get_result_evaluation_code_section(self) -> CodeSectionData:
        return self._result_evaluation_code_section

    def _get_result_body_code_section(self) -> CodeSectionData:
        return self._result_body_code_section
    # !SECTION
    
    # SECTION   BranchResultData setter functions
    def _set_evaluation_marker_id(self, evaluation_marker_id:int):
        if evaluation_marker_id is None:
            raise ValueError("evaluation_marker_id can't be none")
        elif not isinstance(evaluation_marker_id, int):
            raise TypeError("evaluation_marker_id shall be of type int")
        else:
            self._evaluation_marker_id = evaluation_marker_id

    def _set_conditions(self, conditions:List[ConditionData]):
        if conditions is None:
            raise ValueError("conditions can't be none")
        elif not isinstance(conditions, List[ConditionData]):
            raise TypeError("conditions shall be of type List[ConditionData]")
        else:
            self._conditions = conditions

    def _set_result_evaluation_code_section(self, result_evaluation_code_section:CodeSectionData):
        if result_evaluation_code_section is None:
            raise ValueError("result_evaluation_code_section can't be none")
        elif not isinstance(result_evaluation_code_section, CodeSectionData):
            raise TypeError("result_evaluation_code_section shall be of type CodeSectionData")
        else:
            self._result_evaluation_code_section = result_evaluation_code_section
        
    def _set_result_body_code_section(self, result_body_code_section:CodeSectionData):
        if result_body_code_section is None:
            raise ValueError("result_body_code_section can't be none")
        elif not isinstance(result_body_code_section, CodeSectionData):
            raise TypeError("result_body_code_section shall be of type CodeSectionData")
        else:
            self._result_body_code_section = result_body_code_section
    # !SECTION
    
    # SECTION   BranchResultData property definitions
    evaluation_marker_id: int = property(fget=_get_evaluation_marker_id,
                  fset=_set_evaluation_marker_id,
                  doc="Stores the ID of the according evaluation marker")
    conditions: List[ConditionData] = property(fget=_get_conditions,
                  fset=_set_conditions,
                  doc="Stores the conditions of the evaluation")
    result_evaluation_code_section: CodeSectionData = property(fget=_get_result_evaluation_code_section,
                  fset=_set_result_evaluation_code_section,
                  doc="Stores the code section of the evaluation")
    result_body_code_section: CodeSectionData = property(fget=_get_result_body_code_section,
                  fset=_set_result_body_code_section,
                  doc="Stores the code section of the result code body")
    # !SECTION
    
    # SECTION   BranchResultData private functions
    # !SECTION
    
    # SECTION   BranchResultData public functions
    # !SECTION
# !SECTION

# SECTION   ClassData class
class ClassData:
    """ClassData class.
       Stores the code information about a class.
    """
    
    # SECTION   ClassData private attribute definitions
    __slots__ = ["_class_id", "_class_name"]

    _class_id: int
    _class_name: str
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
    def _get_class_id(self) -> int:
        return self._class_id

    def _get_class_name(self) -> str:
        return self._class_name
    # !SECTION
    
    # SECTION   ClassData setter functions
    def _set_class_id(self, class_id:int):
        if class_id is None:
            raise ValueError("class_id can't be none")
        elif not isinstance(class_id, int):
            raise TypeError("class_id shall be of type int")
        else:
            self._class_id = class_id

    def _set_class_name(self, class_name:str):
        if class_name is None:
            raise ValueError("class_name can't be none")
        elif not isinstance(class_name, str):
            raise TypeError("class_name shall be of type str")
        else:
            self._class_name = class_name
    # !SECTION
    
    # SECTION   ClassData property definitions
    class_id: int = property(fget=_get_class_id,
                  fset=_set_class_id,
                  doc="Stores a unique id for the class")
    class_name: str = property(fget=_get_class_name,
                  fset=_set_class_name,
                  doc="Stores the name of the class")
    # !SECTION
    
    # SECTION   ClassData private functions
    # !SECTION
    
    # SECTION   ClassData public functions
    # !SECTION
# !SECTION

# SECTION   FunctionData class
class FunctionData:
    """FunctionData class.
       Stores the code information about a function.
    """
    
    # SECTION   FunctionData private attribute definitions
    __slots__ = ["_function_id", "_function_name", "_function_type",
            "_parent_function_id", "_checkpoint_marker_id",
            "_header_code_section", "_inner_code_section"]

    _function_id: int
    _function_name: str
    _function_type: FunctionType
    _parent_function_id: int
    _checkpoint_marker_id: int
    _header_code_section: CodeSectionData
    _inner_code_section: CodeSectionData
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
    def _get_function_id(self) -> int:
        return self._function_id
    
    def _get_function_name(self) -> str:
        return self._function_name

    def _get_function_type(self) -> FunctionType:
        return self._function_type

    def _get_parent_function_id(self) -> int:
        return self._parent_function_id

    def _get_checkpoint_marker_id(self) -> int:
        return self._checkpoint_marker_id

    def _get_header_code_section(self) -> CodeSectionData:
        return self._header_code_section

    def _get_inner_code_section(self) -> CodeSectionData:
        return self._inner_code_section
    # !SECTION
    
    # SECTION   FunctionData setter functions
    def _set_function_id(self, function_id:int):
        if function_id is None:
            raise ValueError("function_id can't be none")
        elif not isinstance(function_id, int):
            raise TypeError("function_id shall be of type int")
        else:
            self._function_id = function_id

    def _set_function_name(self, function_name:str):
        if function_name is None:
            raise ValueError("function_name can't be none")
        elif not isinstance(function_name, str):
            raise TypeError("function_name shall be of type str")
        else:
            self._function_name = function_name

    def _set_function_type(self, function_type:FunctionType):
        if function_type is None:
            raise ValueError("function_type can't be none")
        elif not isinstance(function_type, FunctionType):
            raise TypeError("function_type shall be of type FunctionType")
        else:
            self._function_type = function_type

    def _set_parent_function_id(self, parent_function_id:int):
        if parent_function_id is None:
            raise ValueError("parent_function_id can't be none")
        elif not isinstance(parent_function_id, int):
            raise TypeError("parent_function_id shall be of type int")
        else:
            self._parent_function_id = parent_function_id

    def _set_checkpoint_marker_id(self, checkpoint_marker_id:int):
        if checkpoint_marker_id is None:
            raise ValueError("checkpoint_marker_id can't be none")
        elif not isinstance(checkpoint_marker_id, int):
            raise TypeError("checkpoint_marker_id shall be of type int")
        else:
            self._checkpoint_marker_id = checkpoint_marker_id

    def _set_header_code_section(self, header_code_section:CodeSectionData):
        if header_code_section is None:
            raise ValueError("header_code_section can't be none")
        elif not isinstance(header_code_section, CodeSectionData):
            raise TypeError("header_code_section shall be of type CodeSectionData")
        else:
            self._header_code_section = header_code_section

    def _set_inner_code_section(self, inner_code_section:CodeSectionData):
        if inner_code_section is None:
            raise ValueError("inner_code_section can't be none")
        elif not isinstance(inner_code_section, CodeSectionData):
            raise TypeError("inner_code_section shall be of type CodeSectionData")
        else:
            self._inner_code_section = inner_code_section
    # !SECTION
    
    # SECTION   FunctionData property definitions
    function_id: int = property(fget=_get_function_id,
                  fset=_set_function_id,
                  doc="Stores a unique id for the specific function")
    function_name: str = property(fget=_get_function_name,
                  fset=_set_function_name,
                  doc="Stores the name of the function")
    function_type: FunctionType = property(fget=_get_function_type,
                  fset=_set_function_type,
                  doc="Stores the type of the function")
    parent_function_id: int = property(fget=_get_parent_function_id,
                  fset=_set_parent_function_id,
                  doc="Stores the id of the parent function (if no parent function, this is -1)")
    checkpoint_marker_id: int = property(fget=_get_checkpoint_marker_id,
                  fset=_set_checkpoint_marker_id,
                  doc="Stores the ID of the according checkpoint marker")
    header_code_section: CodeSectionData = property(fget=_get_header_code_section,
                  fset=_set_header_code_section,
                  doc="Stores the code section of the function header")
    inner_code_section: CodeSectionData = property(fget=_get_inner_code_section,
                  fset=_set_inner_code_section,
                  doc="Stores the code section of the function body")
    # !SECTION
    
    # SECTION   FunctionData private functions
    # !SECTION
    
    # SECTION   FunctionData public functions
    # !SECTION
# !SECTION

# SECTION   StatementData class
class StatementData:
    """StatementData class.
       Stores the code information about a statement.
    """
    
    # SECTION   StatementData private attribute definitions
    __slots__ = ["_statement_id", "_statement_type", "_function_id", "_checkpoint_marker_id",
                 "_code_section"]

    _statement_id: int
    _statement_type: StatementType
    _function_id: int
    _checkpoint_marker_id: int
    _code_section: CodeSectionData
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
    def _get_statement_id(self) -> int:
        return self._statement_id

    def _get_statement_type(self) -> StatementType:
        return self._statement_type

    def _get_function_id(self) -> int:
        return self._function_id

    def _get_checkpoint_marker_id(self) -> int:
        return self._checkpoint_marker_id

    def _get_code_section(self) -> CodeSectionData:
        return self._code_section
    # !SECTION
    
    # SECTION   StatementData setter functions
    def _set_statement_id(self, statement_id:int):
        if statement_id is None:
            raise ValueError("statement_id can't be none")
        elif not isinstance(statement_id, int):
            raise TypeError("statement_id shall be of type int")
        else:
            self._statement_id = statement_id

    def _set_statement_type(self, statement_type:StatementType):
        if statement_type is None:
            raise ValueError("statement_type can't be none")
        elif not isinstance(statement_type, StatementType):
            raise TypeError("statement_type shall be of type StatementType")
        else:
            self._statement_type = statement_type
    
    def _set_function_id(self, function_id:int):
        if function_id is None:
            raise ValueError("function_id can't be none")
        elif not isinstance(function_id, int):
            raise TypeError("function_id shall be of type int")
        else:
            self._function_id = function_id

    def _set_checkpoint_marker_id(self, checkpoint_marker_id:int):
        if checkpoint_marker_id is None:
            raise ValueError("checkpoint_marker_id can't be none")
        elif not isinstance(checkpoint_marker_id, int):
            raise TypeError("checkpoint_marker_id shall be of type int")
        else:
            self._checkpoint_marker_id = checkpoint_marker_id

    def _set_code_section(self, code_section:CodeSectionData):
        if code_section is None:
            raise ValueError("code_section can't be none")
        elif not isinstance(code_section, CodeSectionData):
            raise TypeError("code_section shall be of type CodeSectionData")
        else:
            self._code_section = code_section
    # !SECTION
    
    # SECTION   StatementData property definitions
    statement_id: int = property(fget=_get_statement_id,
                  fset=_set_statement_id,
                  doc="Stores a unique ID for the statement")
    statement_type: StatementType = property(fget=_get_statement_type,
                  fset=_set_statement_type,
                  doc="Stores the type of the statement")
    function_id: int = property(fget=_get_function_id,
                  fset=_set_function_id,
                  doc="Stores the ID of the parent function")
    checkpoint_marker_id: int = property(fget=_get_checkpoint_marker_id,
                  fset=_set_checkpoint_marker_id,
                  doc="Stores the ID of the according checkpoint marker")
    code_section: CodeSectionData = property(fget=_get_code_section,
                  fset=_set_code_section,
                  doc="Stores the code section of the statement")
    # !SECTION
    
    # SECTION   StatementData private functions
    # !SECTION
    
    # SECTION   StatementData public functions
    # !SECTION
# !SECTION

# SECTION   IfBranchData class
class IfBranchData:
    """IfBranchData class.
       Stores the code information about a if branch.
    """
    
    # SECTION   IfBranchData private attribute definitions
    __slots__ = ["_if_branch_id", "_function_id", "_branch_results"]

    _if_branch_id: int
    _function_id: int
    _branch_results: List[BranchResultData]
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
    def _get_if_branch_id(self) -> int:
        return self._if_branch_id

    def _get_function_id(self) -> int:
        return self._function_id

    def _get_branch_results(self) -> List[BranchResultData]:
        return self._branch_results
    # !SECTION
    
    # SECTION   IfBranchData setter functions
    def _set_if_branch_id(self, if_branch_id:int):
        if if_branch_id is None:
            raise ValueError("if_branch_id can't be none")
        elif not isinstance(if_branch_id, int):
            raise TypeError("if_branch_id shall be of type int")
        else:
            self._if_branch_id = if_branch_id

    def _set_function_id(self, function_id:int):
        if function_id is None:
            raise ValueError("function_id can't be none")
        elif not isinstance(function_id, int):
            raise TypeError("function_id shall be of type int")
        else:
            self._function_id = function_id

    def _set_branch_results(self, branch_results:List[BranchResultData]):
        if branch_results is None:
            raise ValueError("branch_results can't be none")
        elif not isinstance(branch_results, List[BranchResultData]):
            raise TypeError("branch_results shall be of type List[BranchResultData]")
        else:
            self._branch_results = branch_results
    # !SECTION
    
    # SECTION   IfBranchData property definitions
    if_branch_id: int = property(fget=_get_if_branch_id,
                  fset=_set_if_branch_id,
                  doc="Stores a unique ID of the if branch")
    function_id: int = property(fget=_get_function_id,
                  fset=_set_function_id,
                  doc="Stores the Id of the parent function")
    branch_results: List[BranchResultData] = property(fget=_get_branch_results,
                  fset=_set_branch_results,
                  doc="Stores the branch results of the if branch")
    # !SECTION
    
    # SECTION   IfBranchData private functions
    # !SECTION
    
    # SECTION   IfBranchData public functions
    # !SECTION
# !SECTION

# SECTION   SwitchBranchData class
class SwitchBranchData:
    """SwitchBranchData class.
       Stores the code information about a switch branch.
    """
    
    # SECTION   SwitchBranchData private attribute definitions
    __slots__ = ["_switch_branch_id", "_function_id", "_expression_code_section", "_cases"]

    _switch_branch_id: int
    _function_id: int
    _expression_code_section: CodeSectionData
    _cases: List[CaseData]
    # !SECTION
    
    # SECTION   SwitchBranchData public attribute definitions
    # !SECTION
    
    # SECTION   SwitchBranchData initialization
    def __init__(self, switch_branch_id: int, function_id: int,
            expression_code_section: CodeSectionData, cases: List[CaseData]):
        self.switch_branch_id = switch_branch_id
        self.function_id = function_id
        self.expression_code_section = expression_code_section
        self.cases = cases
        return
    # !SECTION
    
    # SECTION   SwitchBranchData getter functions
    def _get_switch_branch_id(self) -> int:
        return self._switch_branch_id

    def _get_function_id(self) -> int:
        return self._function_id

    def _get_expression_code_section(self) -> CodeSectionData:
        return self._expression_code_section

    def _get_cases(self) -> List[CaseData]:
        return self._cases
    # !SECTION
    
    # SECTION   SwitchBranchData setter functions
    def _set_switch_branch_id(self, switch_branch_id:int):
        if switch_branch_id is None:
            raise ValueError("switch_branch_id can't be none")
        elif not isinstance(switch_branch_id, int):
            raise TypeError("switch_branch_id shall be of type int")
        else:
            self._switch_branch_id = switch_branch_id

    def _set_function_id(self, function_id:int):
        if function_id is None:
            raise ValueError("function_id can't be none")
        elif not isinstance(function_id, int):
            raise TypeError("function_id shall be of type int")
        else:
            self._function_id = function_id

    def _set_expression_code_section(self, expression_code_section:CodeSectionData):
        if expression_code_section is None:
            raise ValueError("expression_code_section can't be none")
        elif not isinstance(expression_code_section, CodeSectionData):
            raise TypeError("expression_code_section shall be of type CodeSectionData")
        else:
            self._expression_code_section = expression_code_section

    def _set_cases(self, cases:List[CaseData]):
        if cases is None:
            raise ValueError("cases can't be none")
        elif not isinstance(cases, List[CaseData]):
            raise TypeError("cases shall be of type List[CaseData]")
        else:
            self._cases = cases
    # !SECTION
    
    # SECTION   SwitchBranchData property definitions
    switch_branch_id: int = property(fget=_get_switch_branch_id,
                  fset=_set_switch_branch_id,
                  doc="Stores a unique ID for the switch branch")
    function_id: int = property(fget=_get_function_id,
                  fset=_set_function_id,
                  doc="Stores the id of the parent function")
    expression_code_section: CodeSectionData = property(fget=_get_expression_code_section,
                  fset=_set_expression_code_section,
                  doc="Stores the code section of the switch evaluation")
    cases: List[CaseData] = property(fget=_get_cases,
                  fset=_set_cases,
                  doc="Stores all cases belonging to the switch branch")
    # !SECTION
    
    # SECTION   SwitchBranchData private functions
    # !SECTION
    
    # SECTION   SwitchBranchData public functions
    # !SECTION
# !SECTION

# SECTION   LoopData class
class LoopData:
    """LoopData class.
       Stores the code information about a loop.
    """
    
    # SECTION   LoopData private attribute definitions
    __slots__ = ["_loop_id", "_loop_type", "_function_id",
                 "_evaluation_marker_id", "_evaluation_code_section", "_body_code_section",
                 "_conditions"]

    _loop_id: int
    _loop_type: LoopType
    _function_id: int
    _evaluation_marker_id: int
    _evaluation_code_section: CodeSectionData
    _body_code_section: CodeSectionData
    _conditions: List[ConditionData]
    # !SECTION
    
    # SECTION   LoopData public attribute definitions
    # !SECTION
    
    # SECTION   LoopData initialization
    def __init__(self, loop_id: int, loop_type: LoopType, function_id: int,
            evaluation_marker_id: int, evaluation_code_section: CodeSectionData,
            body_code_section: CodeSectionData, conditions: List[ConditionData]):
        self.loop_id = loop_id
        self.loop_type = loop_type
        self.function_id = function_id
        self.evaluation_marker_id = evaluation_marker_id
        self.evaluation_code_section = evaluation_code_section
        self.body_code_section = body_code_section
        self.conditions = conditions
        return
    # !SECTION
    
    # SECTION   LoopData getter functions
    def _get_loop_id(self) -> int:
        return self._loop_id

    def _get_loop_type(self) -> LoopType:
        return self._loop_type

    def _get_function_id(self) -> int:
        return self._function_id

    def _get_evaluation_marker_id(self) -> int:
        return self._evaluation_marker_id

    def _get_evaluation_code_section(self) -> CodeSectionData:
        return self._evaluation_code_section

    def _get_body_code_section(self) -> CodeSectionData:
        return self._body_code_section

    def _get_conditions(self) -> List[ConditionData]:
        return self._conditions
    # !SECTION
    
    # SECTION   LoopData setter functions
    def _set_loop_id(self, loop_id:int):
        if loop_id is None:
            raise ValueError("loop_id can't be none")
        elif not isinstance(loop_id, int):
            raise TypeError("loop_id shall be of type int")
        else:
            self._loop_id = loop_id

    def _set_loop_type(self, loop_type:LoopType):
        if loop_type is None:
            raise ValueError("loop_type can't be none")
        elif not isinstance(loop_type, LoopType):
            raise TypeError("loop_type shall be of type LoopType")
        else:
            self._loop_type = loop_type

    def _set_function_id(self, function_id:int):
        if function_id is None:
            raise ValueError("function_id can't be none")
        elif not isinstance(function_id, int):
            raise TypeError("function_id shall be of type int")
        else:
            self._function_id = function_id

    def _set_evaluation_marker_id(self, evaluation_marker_id:int):
        if evaluation_marker_id is None:
            raise ValueError("evaluation_marker_id can't be none")
        elif not isinstance(evaluation_marker_id, int):
            raise TypeError("evaluation_marker_id shall be of type int")
        else:
            self._evaluation_marker_id = evaluation_marker_id

    def _set_evaluation_code_section(self, evaluation_code_section:CodeSectionData):
        if evaluation_code_section is None:
            raise ValueError("evaluation_code_section can't be none")
        elif not isinstance(evaluation_code_section, CodeSectionData):
            raise TypeError("evaluation_code_section shall be of type CodeSectionData")
        else:
            self._evaluation_code_section = evaluation_code_section

    def _set_body_code_section(self, body_code_section:CodeSectionData):
        if body_code_section is None:
            raise ValueError("body_code_section can't be none")
        elif not isinstance(body_code_section, CodeSectionData):
            raise TypeError("body_code_section shall be of type CodeSectionData")
        else:
            self._body_code_section = body_code_section
        
    def _set_conditions(self, conditions:List[ConditionData]):
        if conditions is None:
            raise ValueError("conditions can't be none")
        elif not isinstance(conditions, List[ConditionData]):
            raise TypeError("conditions shall be of type List[ConditionData]")
        else:
            self._conditions = conditions
    # !SECTION
    
    # SECTION   LoopData property definitions
    loop_id: int = property(fget=_get_loop_id,
                  fset=_set_loop_id,
                  doc="Stores a unique id for the loop")
    loop_type: LoopType = property(fget=_get_loop_type,
                  fset=_set_loop_type,
                  doc="Stores the type of the loop")
    function_id: int = property(fget=_get_function_id,
                  fset=_set_function_id,
                  doc="Stoes the id of the parent function")
    evaluation_marker_id: int = property(fget=_get_evaluation_marker_id,
                  fset=_set_evaluation_marker_id,
                  doc="Stores the id of the according evaluation marker")
    evaluation_code_section: CodeSectionData = property(fget=_get_evaluation_code_section,
                  fset=_set_evaluation_code_section,
                  doc="Stoes the code section of the loop evaluation")
    body_code_section: CodeSectionData = property(fget=_get_body_code_section,
                  fset=_set_body_code_section,
                  doc="Stores the code section of the loop body")
    conditions: List[ConditionData] = property(fget=_get_conditions,
                  fset=_set_conditions,
                  doc="Stores the conditions of the loop evaluation")
    # !SECTION
    
    # SECTION   LoopData private functions
    # !SECTION
    
    # SECTION   LoopData public functions
    # !SECTION
# !SECTION

# SECTION   CodeData class
class CodeData:
    """CodeData class.
       Stores all information about the parsed code
    """
    
    # SECTION   CodeData private attribute definitions
    __slots__ = ["_classes", "_functions", "_statements", "_if_branches",
                 "_switch_branches", "_loops"]

    _classes: List[ClassData]
    _functions: List[FunctionData]
    _statements: List[StatementData]
    _if_branches: List[IfBranchData]
    _switch_branches: List[SwitchBranchData]
    _loops: List[LoopData]
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
        self.loops = list()
        return
    # !SECTION
    
    # SECTION   CodeData getter functions
    def _get_classes(self) -> List[ClassData]:
        return self._classes

    def _get_functions(self) -> List[FunctionData]:
        return self._functions

    def _get_statements(self) -> List[StatementData]:
        return self._statements

    def _get_if_branches(self) -> List[IfBranchData]:
        return self._if_branches

    def _get_switch_branches(self) -> List[SwitchBranchData]:
        return self._switch_branches

    def _get_loops(self) -> List[LoopData]:
        return self._loops
    # !SECTION
    
    # SECTION   CodeData setter functions
    def _set_classes(self, classes:List[ClassData]):
        if classes is None:
            raise ValueError("classes can't be none")
        elif not isinstance(classes, list):
            raise TypeError("classes shall be of type list")
        else:
            self._classes = classes

    def _set_functions(self, functions:List[FunctionData]):
        if functions is None:
            raise ValueError("functions can't be none")
        elif not isinstance(functions, list):
            raise TypeError("functions shall be of type list")
        else:
            self._functions = functions

    def _set_statements(self, statements:List[StatementData]):
        if statements is None:
            raise ValueError("statements can't be none")
        elif not isinstance(statements, list):
            raise TypeError("statements shall be of type list")
        else:
            self._statements = statements

    def _set_if_branches(self, if_branches:List[IfBranchData]):
        if if_branches is None:
            raise ValueError("if_branches can't be none")
        elif not isinstance(if_branches, list):
            raise TypeError("if_branches shall be of type list")
        else:
            self._if_branches = if_branches

    def _set_switch_branches(self, switch_branches:List[SwitchBranchData]):
        if switch_branches is None:
            raise ValueError("switch_branches can't be none")
        elif not isinstance(switch_branches, list):
            raise TypeError("switch_branches shall be of type list")
        else:
            self._switch_branches = switch_branches

    def _set_loops(self, loops:List[LoopData]):
        if loops is None:
            raise ValueError("loops can't be none")
        elif not isinstance(loops, list):
            raise TypeError("loops shall be of type list")
        else:
            self._loops = loops
    # !SECTION
    
    # SECTION   CodeData property definitions
    classes = property(fget=_get_classes,
                  fset=_set_classes,
                  doc="Stores information about the classes of the instrumented code")
    functions = property(fget=_get_functions,
                  fset=_set_functions,
                  doc="Stores information about the functions of the instrumented code")
    statements = property(fget=_get_statements,
                  fset=_set_statements,
                  doc="Stores information about the statements of the instrumented code")
    if_branches = property(fget=_get_if_branches,
                  fset=_set_if_branches,
                  doc="Stores information about the if branches of the instrumented code")
    switch_branches = property(fget=_get_switch_branches,
                  fset=_set_switch_branches,
                  doc="Stores information about the switch branches of the instrumented code")
    loops = property(fget=_get_loops,
                  fset=_set_loops,
                  doc="Stores information about the loops of the instrumented code")
    # !SECTION
    
    # SECTION   CodeData private functions
    # !SECTION
    
    # SECTION   CodeData public functions
    # !SECTION
# !SECTION

# SECTION   CIDData class
class CIDData:
    """CIDData class.
       Stores the data of a "Codeconut Instrumentation Data" object.
    """
    
    # SECTION   CIDData private attribute definitions
    __slots__ = ['_source_code_filename', '_source_code_hash',
                 '_instrumentation_random', '_checkpoint_markers_enabled',
                 '_evaluation_markers_enabled',
                 '_marker_data', '_code_data']

    _source_code_filename: str
    _source_code_hash: str
    _instrumentation_random: str
    _checkpoint_markers_enabled: bool
    _evaluation_markers_enabled: bool
    _marker_data: List[MarkerData]
    _code_data: List[CodeData]
    # !SECTION
    
    # SECTION   CIDData public attribute definitions
    # !SECTION
    
    # SECTION   CIDData initialization
    def __init__(self,
                 source_code_filename: str,
                 source_code_hash: str,
                 instrumentation_random: str,
                 checkpoint_markers_enabled: bool,
                 evaluation_markers_enabled: bool):
        self.source_code_filename = source_code_filename
        self.source_code_hash = source_code_hash
        self.instrumentation_random = instrumentation_random
        self.checkpoint_markers_enabled = checkpoint_markers_enabled
        self.evaluation_markers_enabled = evaluation_markers_enabled
        self._marker_data = MarkerData()
        self._code_data = CodeData()
        return
    # !SECTION
    
    # SECTION   CIDData getter functions
    def _get_source_code_filename(self) -> str:
        return self._source_code_filename

    def _get_source_code_hash(self) -> str:
        return self._source_code_hash

    def _get_instrumentation_random(self) -> str:
        return self._instrumentation_random

    def _get_checkpoint_markers_enabled(self) -> bool:
        return self._checkpoint_markers_enabled

    def _get_evaluation_markers_enabled(self) -> bool:
        return self._evaluation_markers_enabled

    def _get_marker_data(self) -> MarkerData:
        return self._marker_data

    def _get_code_data(self) -> CodeData:
        return self._code_data
    # !SECTION
    
    # SECTION   CIDData setter functions
    def _set_source_code_filename(self, source_code_filename:str):
        if source_code_filename is None:
            raise ValueError("source_code_filename can't be none")
        elif not isinstance(source_code_filename, str):
            raise TypeError("source_code_filename shall be of type str")
        else:
            self._source_code_filename = source_code_filename

    def _set_source_code_hash(self, source_code_hash:str):
        if source_code_hash is None:
            raise ValueError("source_code_hash can't be none")
        elif not isinstance(source_code_hash, str):
            raise TypeError("source_code_hash shall be of type str")
        else:
            self._source_code_hash = source_code_hash

    def _set_instrumentation_random(self, instrumentation_random:str):
        if instrumentation_random is None:
            raise ValueError("instrumentation_random can't be none")
        elif not isinstance(instrumentation_random, str):
            raise TypeError("instrumentation_random shall be of type str")
        else:
            self._instrumentation_random = instrumentation_random

    def _set_checkpoint_markers_enabled(self, checkpoint_markers_enabled:bool):
        if checkpoint_markers_enabled is None:
            raise ValueError("checkpoint_markers_enabled can't be none")
        elif not isinstance(checkpoint_markers_enabled, bool):
            raise TypeError("checkpoint_markers_enabled shall be of type bool")
        else:
            self._checkpoint_markers_enabled = checkpoint_markers_enabled

    def _set_evaluation_markers_enabled(self, evaluation_markers_enabled:bool):
        if evaluation_markers_enabled is None:
            raise ValueError("evaluation_markers_enabled can't be none")
        elif not isinstance(evaluation_markers_enabled, bool):
            raise TypeError("evaluation_markers_enabled shall be of type bool")
        else:
            self._evaluation_markers_enabled = evaluation_markers_enabled
    # !SECTION
    
    # SECTION   CIDData property definitions
    source_code_filename: str = property(fget=_get_source_code_filename,
                  fset=_set_source_code_filename,
                  doc="Stores the filename of the source code file")
    source_code_hash: str = property(fget=_get_source_code_hash,
                  fset=_set_source_code_hash,
                  doc="Stores a hash of the source code file")
    instrumentation_random: str = property(fget=_get_instrumentation_random,
                  fset=_set_instrumentation_random,
                  doc="Stores a random string for this instrumentation process")
    checkpoint_markers_enabled: bool = property(fget=_get_checkpoint_markers_enabled,
                  fset=_set_checkpoint_markers_enabled,
                  doc="Stores, if checkpoint markers are enabled")
    evaluation_markers_enabled: bool = property(fget=_get_evaluation_markers_enabled,
                  fset=_set_evaluation_markers_enabled,
                  doc="Stoes, if evaluation markers are enabled")
    marker_data: MarkerData = property(fget=_get_marker_data,
                  doc="Stores the marker data of the instrumentation")
    code_data: CodeData = property(fget=_get_code_data,
                  doc="Stores the code information data of the instrumentation")
    # !SECTION
    
    # SECTION   CIDData private functions
    # !SECTION
    
    # SECTION   CIDData public functions
    # !SECTION
# !SECTION