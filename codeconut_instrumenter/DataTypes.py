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
        elif not isinstance(checkpoint_markers, List[CheckpointMarkerData]):
            raise TypeError("checkpoint_markers shall be of type List[CheckpointMarkerData]")
        else:
            self._checkpoint_markers = checkpoint_markers

    def _set_evaluation_markers(self, evaluation_markers:List[EvaluationMarkerData]):
        if evaluation_markers is None:
            raise ValueError("evaluation_markers can't be none")
        elif not isinstance(evaluation_markers, List[EvaluationMarkerData]):
            raise TypeError("evaluation_markers shall be of type List[EvaluationMarkerData]")
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
    # !SECTION
    
    # SECTION   BranchResultData public attribute definitions
    # !SECTION
    
    # SECTION   BranchResultData initialization
    def __init__(self):
        return
    # !SECTION
    
    # SECTION   BranchResultData getter functions
    # !SECTION
    
    # SECTION   BranchResultData setter functions
    # !SECTION
    
    # SECTION   BranchResultData property definitions
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
    # !SECTION
    
    # SECTION   ClassData public attribute definitions
    # !SECTION
    
    # SECTION   ClassData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   FunctionData class
class FunctionData:
    """FunctionData class.
       Stores the code information about a function.
    """
    
    # SECTION   FunctionData private attribute definitions
    # !SECTION
    
    # SECTION   FunctionData public attribute definitions
    # !SECTION
    
    # SECTION   FunctionData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   StatementData class
class StatementData:
    """StatementData class.
       Stores the code information about a statement.
    """
    
    # SECTION   StatementData private attribute definitions
    # !SECTION
    
    # SECTION   StatementData public attribute definitions
    # !SECTION
    
    # SECTION   StatementData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   IfBranchData class
class IfBranchData:
    """IfBranchData class.
       Stores the code information about a if branch.
    """
    
    # SECTION   IfBranchData private attribute definitions
    # !SECTION
    
    # SECTION   IfBranchData public attribute definitions
    # !SECTION
    
    # SECTION   IfBranchData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   SwitchBranchData class
class SwitchBranchData:
    """SwitchBranchData class.
       Stores the code information about a switch branch.
    """
    
    # SECTION   SwitchBranchData private attribute definitions
    # !SECTION
    
    # SECTION   SwitchBranchData public attribute definitions
    # !SECTION
    
    # SECTION   SwitchBranchData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   LoopData class
class LoopData:
    """LoopData class.
       Stores the code information about a loop.
    """
    
    # SECTION   LoopData private attribute definitions
    # !SECTION
    
    # SECTION   LoopData public attribute definitions
    # !SECTION
    
    # SECTION   LoopData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   CodeData class
class CodeData:
    """CodeData class.
       Stores all information about the parsed code
    """
    
    # SECTION   CodeData private attribute definitions
    # !SECTION
    
    # SECTION   CodeData public attribute definitions
    # !SECTION
    
    # SECTION   CodeData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION

# SECTION   CIDData class
class CIDData:
    """CIDData class.
       Stores the data of a "Codeconut Instrumentation Data" object.
    """
    
    # SECTION   CIDData private attribute definitions
    # !SECTION
    
    # SECTION   CIDData public attribute definitions
    # !SECTION
    
    # SECTION   CIDData initialization
    def __init__(self):
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
    # !SECTION
# !SECTION


#class CIDData:
    """Stores the instrumentation data for a input file"""

    # SECTION   CIDData private attribute definitions
    __slots__ = ['_source_code_filename', '_source_code_hash',
                 '_instrumentation_random', '_statement_markers_enabled',
                 '_decision_markers_enabled', '_condition_markers_enabled',
                 '_marker_data']

    _source_code_filename: str
    _source_code_hash: str
    _instrumentation_random: str
    _checkpoint_markers_enabled: bool
    _evaluation_markers_enabled: bool
    _marker_data: list
    _code_data: list
    # !SECTION

    # SECTION   CIDData initialization
    def __init__(self,
                 source_code_filename=None,
                 source_code_hash=None,
                 instrumentation_random=None,
                 statement_markers_enabled=None,
                 decision_markers_enabled=None,
                 condition_markers_enabled=None):
        self.source_code_filename = source_code_filename
        self.source_code_hash = source_code_hash
        self.instrumentation_random = instrumentation_random
        self.statement_markers_enabled = statement_markers_enabled
        self.decision_markers_enabled = decision_markers_enabled
        self.condition_markers_enabled = condition_markers_enabled
        self._marker_data = list()
    # !SECTION

    # SECTION   CIDData getter functions
    def _get_source_code_filename(self) -> str:
        return self._source_code_filename

    def _get_source_code_hash(self) -> str:
        return self._source_code_hash

    def _get_instrumentation_random(self) -> str:
        return self._instrumentation_random

    def _get_statement_markers_enabled(self) -> bool:
        return self._statement_markers_enabled

    def _get_decision_markers_enabled(self) -> bool:
        return self._decision_markers_enabled

    def _get_condition_markers_enabled(self) -> bool:
        return self._condition_markers_enabled

    def _get_marker_data(self) -> List[MarkerData]:
        return self._marker_data
    # !SECTION

    # SECTION   CIDData setter functions
    def _set_source_code_filename(self, source_code_filename):
        if source_code_filename is None:
            raise ValueError("source_code_filename not defined!")
        elif not isinstance(source_code_filename, str):
            raise TypeError("source_code_filename shall be of type str!")
        else:
            self._source_code_filename = source_code_filename

    def _set_source_code_hash(self, source_code_hash):
        if source_code_hash is None:
            raise ValueError("source_code_hash not defined!")
        elif not isinstance(source_code_hash, str):
            raise TypeError("source_code_hash shall be of type str!")
        elif len(source_code_hash) != 64:
            raise ValueError("source_code_hash has bad length!")
        elif re.match("^[0-9a-f]+$", source_code_hash) is None:
            raise ValueError("source_code_hash has bad characters!")
        else:
            self._source_code_hash = source_code_hash

    def _set_instrumentation_random(self, instrumentation_random):
        if instrumentation_random is None:
            raise ValueError("instrumentation_random not defined!")
        elif not isinstance(instrumentation_random, str):
            raise TypeError("instrumentation_random shall be of type str!")
        elif len(instrumentation_random) != 16:
            raise ValueError("instrumentation_random has bad length!")
        elif re.match("^[0-9a-zA-Z]+$", instrumentation_random) is None:
            raise ValueError("instrumentation_random has bad characters!")
        else:
            self._instrumentation_random = instrumentation_random

    def _set_statement_markers_enabled(self, statement_markers_enabled):
        if statement_markers_enabled is None:
            raise ValueError("statement_markers_enabled not defined!")
        elif not isinstance(statement_markers_enabled, bool):
            raise TypeError("statement_markers_enabled shall be of type bool!")
        else:
            self._statement_markers_enabled = statement_markers_enabled

    def _set_decision_markers_enabled(self, decision_markers_enabled):
        if decision_markers_enabled is None:
            raise ValueError("decision_markers_enabled not defined!")
        elif not isinstance(decision_markers_enabled, bool):
            raise TypeError("decision_markers_enabled shall be of type bool!")
        else:
            self._decision_markers_enabled = decision_markers_enabled

    def _set_condition_markers_enabled(self, condition_markers_enabled):
        if condition_markers_enabled is None:
            raise ValueError("condition_markers_enabled not defined!")
        elif not isinstance(condition_markers_enabled, bool):
            raise TypeError("condition_markers_enabled shall be of type bool!")
        else:
            self._condition_markers_enabled = condition_markers_enabled

    def add_marker_data(self, new_marker: MarkerData):
        if new_marker is None:
            raise ValueError("new marker not defined!")
        elif not isinstance(new_marker, MarkerData):
            raise TypeError("new marker shall be of type MarkerData!")
        elif new_marker in self._marker_data:
            raise ValueError("marker already exists in marker data!")
        else:
            self._marker_data.append(new_marker)

    def update_marker_data(self, marker: MarkerData, new_marker: MarkerData):
        if new_marker is None:
            raise ValueError("new marker not defined!")
        elif not isinstance(new_marker, MarkerData):
            raise TypeError("new marker shall be of type MarkerData!")
        elif marker not in self._marker_data:
            raise ValueError("old marker not found!")
        else:
            self._marker_data[self._marker_data.index(marker)] = new_marker

    def delete_marker_data(self, marker: MarkerData):
        self._marker_data.remove(marker)
    # !SECTION

    # SECTION   CIDData property definitions
    source_code_filename = property(
        _get_source_code_filename, _set_source_code_filename)
    source_code_hash = property(
        _get_source_code_hash, _set_source_code_hash)
    instrumentation_random = property(
        _get_instrumentation_random, _set_instrumentation_random)
    statement_markers_enabled = property(
        _get_statement_markers_enabled, _set_statement_markers_enabled)
    decision_markers_enabled = property(
        _get_decision_markers_enabled, _set_decision_markers_enabled)
    condition_markers_enabled = property(
        _get_condition_markers_enabled, _set_condition_markers_enabled)
    marker_data = property(_get_marker_data)  # read-only
    # !SECTION
