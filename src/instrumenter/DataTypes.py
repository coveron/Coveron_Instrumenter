#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Custom type definitions for Codeconut Instrumenter.
"""

from typing import List
from enum import Enum


SourceCode = str


class CodeSectionData:
    """Stores the start and end position of a specific code section"""

    __slots__ = ['start_line', 'start_column', 'end_line', 'end_column']

    start_line: int
    start_column: int
    end_line: int
    end_column: int


class MarkerTypeEnum(Enum):
    """Enum for the type of a marker"""

    STATEMENT = 1
    DECISION = 2
    CONDITION = 3


class MarkerData:
    """Stores the information for one marker"""

    __slots__ = ["marker_id", "marker_type",
                 "parent_id", "should_write", "code_section_data"]

    marker_id: int
    marker_type: MarkerTypeEnum
    parent_id: int
    should_write: bool
    code_section_data: CodeSectionData


class CIDData:
    """Stores the instrumentation data for a input file"""

    __slots__ = ['source_code_filename', 'source_code_hash', 'instrumentation_random',
                 'statement_markers_enabled', 'decision_markers_enabled', 'condition_markers_enabled', 'marker_data']

    source_code_filename: str
    source_code_hash: str
    instrumentation_random: str
    statement_markers_enabled: bool
    decision_markers_enabled: bool
    condition_markers_enabled: bool
    marker_data: List[MarkerData]
