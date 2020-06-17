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

# SECTION   SourceFile class
class SourceFile:
    """Contains all information about a source file passed to the instrumenter"""

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
        _output_filename = source_file[0:source_file.rindex(
            '.')+1] + "instr." + source_file[source_file.rindex(
                '.')+1:]

        # determine cid filename
        _cid_filename = self.output_filename[0:self.output_filename.rindex(
            '.')+1] + "cid"
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
    def _set_input_filename(self, input_filename):
        if input_filename is None:
            raise ValueError("input_filename can't be none")
        if not isinstance(input_filename, str):
            raise TypeError("input_filename has to be a str")
        else:
            self._input_filename = input_filename
    # !SECTION

    # SECTION   SourceFile property definitions
    input_filename = property(fget=_get_input_filename,
                              fset=_set_input_filename,
                              doc="Filename of the input file")
    output_filename = property(fget=_get_output_filename,
                               doc="Filename of the output file")
    cid_filename = property(fget=_get_cid_filename,
                            doc="Filename of the output CID file")
    # !SECTION

    # SECTION   SourceFile private functions
    # !SECTION

    # SECTION   SourceFile public functions
    # !SECTION
#!SECTION


#SECTION    SourceCode class
SourceCode = str
#!SECTION


class SourceStream:
    """Contains a source file stream with line and column information"""

    # SECTION   SourceStream private attribute definitions
    __slots__ = ['_code', '_active_line', '_active_col']

    _code: List[List[str]]
    # !SECTION

    # SECTION   SourceStream initialization
    def __init__(self, source_code: SourceCode):
        # set active line and col to first position
        self._active_line = 0
        self._active_col = 0

        # check if input code is of correct type
        if not isinstance(source_code, SourceCode):
            raise TypeError("source_code has to be of type SourceCode")

        # split code into lines
        self._code = []
        for sourceline in source_code.splitlines():
            # add newline char for improved analysis
            self._code.append([char for char in (sourceline + "\n")])
    # !SECTION

    # SECTION   SourceStream getter functions
    def _get_active_line(self) -> int:
        return self._active_line + 1

    def _get_active_col(self) -> int:
        return self._active_col + 1

    def _get_eof(self) -> bool:
        if len(self._code) < (self._active_line + 1):
            return True
        elif len(self._code) == (self._active_line + 1) and self._active_col >= len(self._code[self._active_line]):
            return True
        else:
            return False
    # !SECTION

    # SECTION   SourceStream setter functions
    def _set_active_line(self, new_line):
        if not isinstance(new_line, int):
            raise TypeError("new_line has to be a int")
        elif (new_line - 1) < 0:
            raise ValueError("new_line can't be smaller than 0")
        elif (new_line - 1) > len(self._code):
            raise ValueError("new_line is out of source code bounds")
        else:
            self._active_line = new_line - 1

        if len(self._code[self._active_line]) < self._active_col:
            # set _active_col to begin of line if the pointer is out of line bounds
            self._active_col = 0

    def _set_active_col(self, new_col):
        if not isinstance(new_col, int):
            raise TypeError("new_col has to be a int")
        elif (new_col - 1) < 0:
            raise ValueError("new_col can't be smaller than 0")
        elif (new_col - 1) > len(self._code[self._active_line]):
            raise ValueError("new_line is out of source code bounds")
        else:
            self._active_col = new_col - 1
    # !SECTION

    # SECTION   SourceStream property definitions
    active_line = property(_get_active_line, _set_active_line)
    active_col = property(_get_active_col, _set_active_col)
    eof = property(_get_eof)
    # !SECTION

    # SECTION   SourceStream public function definitions
    def get_char(self) -> str:
        # check if end of file was reached
        if self.eof:
            return None

        # get currently active char
        active_char = self._code[self._active_line][self._active_col]

        # set next char position
        if (self._active_col + 1) < len(self._code[self._active_line]):
            self._active_col += 1
        else:
            self._active_line += 1
            self._active_col = 0

        return active_char
    # !SECTION


class CodePositionData:
    """Empty for now"""

class CodeSectionData:
    """Stores the start and end position of a specific code section"""

    __slots__ = ['start_line', 'start_column', 'end_line', 'end_column']

    start_line: int
    start_column: int
    end_line: int
    end_column: int

    # Initialization function for CodeSectionData object
    def __init__(self,
                 start_line=None,
                 start_column=None,
                 end_line=None,
                 end_column=None):
        # start_line is a required argument
        if start_line is None:
            raise ValueError("start_line not defined!")
        elif not isinstance(start_line, int):
            raise TypeError("start_line shall be of type int!")

        # start_column is a required argument
        if start_column is None:
            raise ValueError("start_column not defined!")
        elif not isinstance(start_column, int):
            raise TypeError("start_column shall be of type int!")

        # end_line is a required argument
        if end_line is None:
            raise ValueError("end_line not defined!")
        elif not isinstance(end_line, int):
            raise TypeError("end_line shall be of type int!")

        # end_column is a required argument
        if end_column is None:
            raise ValueError("end_column not defined!")
        elif not isinstance(end_column, int):
            raise TypeError("end_column shall be of type int!")

        # check, if the end pointer is behind the start pointer
        if start_line > end_line or (start_line == end_line and
                                     start_column >= end_column):
            raise ValueError("Invalid values for code section data!")
        else:
            # if yes, assign the values to the object
            self.start_line = start_line
            self.start_column = start_column
            self.end_line = end_line
            self.end_column = end_column


class MarkerTypeEnum(Enum):
    """Enum for the type of a marker"""

    STATEMENT = 1
    DECISION = 2
    CONDITION = 3


class MarkerData:
    """Stores the information for one marker"""

    # SECTION   MarkerData private attribute definitions
    __slots__ = ["_marker_id", "_marker_type",
                 "_parent_id", "_should_write", "_code_section_data"]

    _marker_id: int
    _marker_type: MarkerTypeEnum
    _parent_id: int
    _code_section_data: List[CodeSectionData]
    # !SECTION

    # SECTION   MarkerData initialization
    def __init__(self,
                 marker_id=None,
                 marker_type=None,
                 parent_id=None,
                 code_section_data=None):
        self.marker_id = marker_id
        self.marker_type = marker_type
        self.parent_id = parent_id
        self._code_section_data = code_section_data
    # !SECTION

    # SECTION   MarkerData getter functions
    def _get_marker_id(self) -> int:
        return self._marker_id

    def _get_marker_type(self) -> MarkerTypeEnum:
        return self._marker_type

    def _get_parent_id(self) -> int:
        return self._parent_id

    def _get_code_section_data(self) -> List[CodeSectionData]:
        return self._code_section_data
    # !SECTION

    # SECTION   MarkerData setter functions
    def _set_marker_id(self, marker_id):
        if marker_id is None:
            raise ValueError("marker_id not defined!")
        elif not isinstance(marker_id, int):
            raise TypeError("marker_id shall be of type int!")
        else:
            self._marker_id = marker_id

    def _set_marker_type(self, marker_type):
        if marker_type is None:
            raise ValueError("marker_type not defined!")
        elif not isinstance(marker_type, MarkerTypeEnum):
            raise TypeError("marker_type shall be of type MarkerTypeEnum!")
        else:
            self._marker_type = marker_type

    def _set_parent_id(self, parent_id):
        if isinstance(parent_id, int):
            self._parent_id = parent_id
        elif parent_id is not None:
            raise TypeError("parent_id shall be of type int!")

    def _set_code_section_data(self, code_section_data):
        if code_section_data is None:
            raise ValueError("code_section_data not defined!")
        elif not isinstance(code_section_data, list):
            raise TypeError(
                "code_section_data shall be of type List[CodeSectionData]!")
        elif len(code_section_data) == 0:
            raise ValueError("at least one code section must be given!")
        for item in code_section_data:
            if not isinstance(item, CodeSectionData):
                raise TypeError(
                    "code_section_data items shall be of type CodeSectionData!")

        self._code_section_data = code_section_data
    # !SECTION

    # SECTION   MarkerData property definitions
    marker_id = property(
        _get_marker_id, _set_marker_id)
    marker_type = property(
        _get_marker_type, _set_marker_type)
    parent_id = property(
        _get_parent_id, _set_parent_id)
    code_section_data = property(
        _get_code_section_data, _set_code_section_data)
    # !SECTION


class CIDData:
    """Stores the instrumentation data for a input file"""

    # SECTION   CIDData private attribute definitions
    __slots__ = ['_source_code_filename', '_source_code_hash',
                 '_instrumentation_random', '_statement_markers_enabled',
                 '_decision_markers_enabled', '_condition_markers_enabled',
                 '_marker_data']

    _source_code_filename: str
    _source_code_hash: str
    _instrumentation_random: str
    _statement_markers_enabled: bool
    _decision_markers_enabled: bool
    _condition_markers_enabled: bool
    _marker_data: List[MarkerData]
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
