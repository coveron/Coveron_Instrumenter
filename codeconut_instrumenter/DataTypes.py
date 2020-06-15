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


SourceCode = str


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
    def get_marker_id(self) -> int:
        return self._marker_id

    def get_marker_type(self) -> MarkerTypeEnum:
        return self._marker_type

    def get_parent_id(self) -> int:
        return self._parent_id

    def get_code_section_data(self) -> List[CodeSectionData]:
        return self._code_section_data
    # !SECTION

    # SECTION   MarkerData setter functions
    def set_marker_id(self, marker_id):
        if marker_id is None:
            raise ValueError("marker_id not defined!")
        elif not isinstance(marker_id, int):
            raise TypeError("marker_id shall be of type int!")
        else:
            self._marker_id = marker_id

    def set_marker_type(self, marker_type):
        if marker_type is None:
            raise ValueError("marker_type not defined!")
        elif not isinstance(marker_type, MarkerTypeEnum):
            raise TypeError("marker_type shall be of type MarkerTypeEnum!")
        else:
            self._marker_type = marker_type

    def set_parent_id(self, parent_id):
        if isinstance(parent_id, int):
            self._parent_id = parent_id
        elif parent_id is not None:
            raise TypeError("parent_id shall be of type int!")

    def set_code_section_data(self, code_section_data):
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
        get_marker_id, set_marker_id)
    marker_type = property(
        get_marker_type, set_marker_type)
    parent_id = property(
        get_parent_id, set_parent_id)
    code_section_data = property(
        get_code_section_data, set_code_section_data)
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
    def get_source_code_filename(self) -> str:
        return self._source_code_filename

    def get_source_code_hash(self) -> str:
        return self._source_code_hash

    def get_instrumentation_random(self) -> str:
        return self._instrumentation_random

    def get_statement_markers_enabled(self) -> bool:
        return self._statement_markers_enabled

    def get_decision_markers_enabled(self) -> bool:
        return self._decision_markers_enabled

    def get_condition_markers_enabled(self) -> bool:
        return self._condition_markers_enabled

    def get_marker_data(self) -> List[MarkerData]:
        return self._marker_data
    # !SECTION

    # SECTION   CIDData setter functions
    def set_source_code_filename(self, source_code_filename):
        if source_code_filename is None:
            raise ValueError("source_code_filename not defined!")
        elif not isinstance(source_code_filename, str):
            raise TypeError("source_code_filename shall be of type str!")
        else:
            self._source_code_filename = source_code_filename

    def set_source_code_hash(self, source_code_hash):
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

    def set_instrumentation_random(self, instrumentation_random):
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

    def set_statement_markers_enabled(self, statement_markers_enabled):
        if statement_markers_enabled is None:
            raise ValueError("statement_markers_enabled not defined!")
        elif not isinstance(statement_markers_enabled, bool):
            raise TypeError("statement_markers_enabled shall be of type bool!")
        else:
            self._statement_markers_enabled = statement_markers_enabled

    def set_decision_markers_enabled(self, decision_markers_enabled):
        if decision_markers_enabled is None:
            raise ValueError("decision_markers_enabled not defined!")
        elif not isinstance(decision_markers_enabled, bool):
            raise TypeError("decision_markers_enabled shall be of type bool!")
        else:
            self._decision_markers_enabled = decision_markers_enabled

    def set_condition_markers_enabled(self, condition_markers_enabled):
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
        get_source_code_filename, set_source_code_filename)
    source_code_hash = property(
        get_source_code_hash, set_source_code_hash)
    instrumentation_random = property(
        get_instrumentation_random, set_instrumentation_random)
    statement_markers_enabled = property(
        get_statement_markers_enabled, set_statement_markers_enabled)
    decision_markers_enabled = property(
        get_decision_markers_enabled, set_decision_markers_enabled)
    condition_markers_enabled = property(
        get_condition_markers_enabled, set_condition_markers_enabled)
    marker_data = property(get_marker_data)  # read-only
    # !SECTION
