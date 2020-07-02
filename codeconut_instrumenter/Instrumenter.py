#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Instrumenter for Codeconut Instrumenter.
   Modifies the input code to contain all the calls to the runtime helper.
"""

from typing import List
from DataTypes import *
import copy

from Configuration import Configuration
from CIDManager import CIDManager

# SECTION   InstrumenterMarkerType


class InstrumenterMarkerType(Enum):
    '''Enum for the type of a internal instrumenter marker'''
    CHECKPOINT = 1
    EVALUATION_START = 3
    EVALUATION_END = 4
# !SECTION

# SECTION   InstrumenterMarker class
# reduced type safety, since it's only used in Instrumenter


class InstrumenterMarker:
    """ InstrumenterMarker class.
        This class is a intermediate data store for markers before instrumenting.
        Here, the markers are broken down even more for ease of use during instrumentation.
    """
    __slots__ = ["code_line", "code_column",
                 "marker_type", "marker_id", "condition"]

    code_line: int  # line of the code insertion position
    code_column: int  # column of the code insertion position
    marker_type: InstrumenterMarkerType  # type of the instrumenter marker
    marker_id: int
    condition: bool

    def __init__(self, code_line: int, code_column: int, marker_type: InstrumenterMarkerType,
                 marker_id: int, condition: bool):
        self.code_line = code_line
        self.code_column = code_column
        self.marker_type = marker_type
        self.marker_id = marker_id
        self.condition = condition
        return
# !SECTION


# SECTION   Instrumenter class
class Instrumenter:
    """Instrumenter class.
       Uses the given marker data from the CIDData and generates a instrumented source file
    """

    # SECTION   Instrumenter private attribute definitions
    __slots__ = ["config", "cid_manager", "source_file", "source_code",
                 "_instrumented_code", "_instrumenter_marker_list"]

    config: Configuration
    cid_manager: CIDManager
    source_file: SourceFile
    source_code: SourceCode
    _instrumented_code: SourceCode
    _instrumenter_marker_list: List[InstrumenterMarker]
    # !SECTION

    # SECTION   Instrumenter public attribute definitions
    # !SECTION

    # SECTION   Instrumenter initialization
    def __init__(self, config: Configuration, cid_manager: CIDManager,
                 source_file: SourceFile, source_code: SourceCode):
        self.config = config
        self.cid_manager = cid_manager
        self.source_file = source_file
        self.source_code = source_code
        self._instrumented_code = copy.copy(self.source_code)
        self._instrumenter_marker_list = list()
        return
    # !SECTION

    # SECTION   Instrumenter getter functions
    # !SECTION

    # SECTION   Instrumenter setter functions
    # !SECTION

    # SECTION   Instrumenter property definitions
    # !SECTION

    # SECTION   Instrumenter private functions

    def _prepare_markers(self):
        """Takes all markers from CIDData and creates preprocessed markers for instrumentation"""
        # TODO implement function

        # create all abstract markers
        if self.config.checkpoint_markers_enabled:
            for marker in self.cid_manager.get_checkpoint_markers():
                marker: CheckpointMarkerData  # type hint for IDE

                # store checkpoint marker
                self._instrumenter_marker_list.append(InstrumenterMarker(
                    marker.code_position.line,
                    marker.code_position.column,
                    InstrumenterMarkerType.CHECKPOINT,
                    marker.checkpoint_marker_id, False))

        if self.config.evaluation_markers_enabled:
            for marker in self.cid_manager.get_evaluation_markers():
                marker: EvaluationMarkerData  # type hint for IDE

                # get evaluation type
                conditionMarker: bool = False
                if marker.evaluation_type is EvaluationType.CONDITION:
                    conditionMarker = True

                # store start marker
                self._instrumenter_marker_list.append(InstrumenterMarker(
                    marker.code_section.start_position.line,
                    marker.code_section.start_position.column,
                    InstrumenterMarkerType.EVALUATION_START,
                    marker.evaluation_marker_id,
                    conditionMarker))

                # store end marker
                self._instrumenter_marker_list.append(InstrumenterMarker(
                    marker.code_section.end_position.line,
                    marker.code_section.end_position.column,
                    InstrumenterMarkerType.EVALUATION_END,
                    marker.evaluation_marker_id,
                    conditionMarker))

        # sort for right direction
        # (last items come first, evaluations of condition type come in front of decision type)
        # TODO  finish the sorting stuff...
        self._instrumenter_marker_list.sort(key=(lambda e: (e.code_line, e.code_column, e.condition)),
                                            reverse=True)
        return

    def _insert_text(self, insert_text: str, line: int, column: int):
        """Modify the source code by inserting text at a given position"""
        source_lines = self._instrumented_code.splitlines()
        source_lines[line - 1] = source_lines[line -
                                              1][:(column - 1)] + insert_text + source_lines[line - 1][(column - 1):]
        self._instrumented_code = "\n".join(source_lines)
        return

    def _get_file_struct_name(self) -> str:
        """Build a file struct name out of the instrumentation random"""
        return "___CODECONUT_FILE_" + self.cid_manager.get_instrumentation_random().upper()

    def _write_markers(self):
        """Modify the input source code to integrate the marker calls"""

        for marker in self._instrumenter_marker_list:
            marker: InstrumenterMarker
            m_id_1, m_id_2, m_id_3, m_id_4 = marker.marker_id.to_bytes(
                4, byteorder="big")
            insert_code = ""
            if marker.marker_type is InstrumenterMarkerType.CHECKPOINT:
                insert_code = ("___CODECONUT_SET_CHECKPOINT_MARKER(" +
                               "0x" + "%02x" % m_id_1 + ", " +
                               "0x" + "%02x" % m_id_2 + ", " +
                               "0x" + "%02x" % m_id_3 + ", " +
                               "0x" + "%02x" % m_id_4 + ", " +
                               "&" + self._get_file_struct_name() + ");")
            elif marker.marker_type is InstrumenterMarkerType.EVALUATION_START:
                insert_code = ("___CODECONUT_SET_EVALUATION_MARKER(" +
                               "0x" + "%02x" % m_id_1 + ", " +
                               "0x" + "%02x" % m_id_2 + ", " +
                               "0x" + "%02x" % m_id_3 + ", " +
                               "0x" + "%02x" % m_id_4 + ", " +
                               "&" + self._get_file_struct_name() + ", ")
            elif marker.marker_type is InstrumenterMarkerType.EVALUATION_END:
                insert_code = ")"

            self._insert_text(insert_code, marker.code_line,
                              marker.code_column)

        # TODO implement function
        return

    def _write_wrapper(self):
        """Modify the input source code to integrate other necessary defines and calls"""

        # build include string
        include_string = "#include \"" + self.config.runtime_helper_header_path + "\""

        # build byte array of hash(take hash string and split it every two chars)
        source_hash_string = self.cid_manager.get_source_code_hash()
        source_hash_array = [source_hash_string[i:i+2]
                             for i in range(0, len(source_hash_string), 2)]
        source_hash_array = [("0x"+hexbyte.upper())
                             for hexbyte in source_hash_array]  # add hex signature "0x"

        # build byte array of instrumentation random (take random string and split it every two chars)
        instr_random_string = self.cid_manager.get_instrumentation_random()
        instr_random_array = [instr_random_string[i:i+2]
                              for i in range(0, len(instr_random_string), 2)]
        instr_random_array = [("0x"+hexbyte.upper())
                              for hexbyte in instr_random_array]

        # build cri file string (with escaping for windows style paths)
        cri_file_path = os.path.join(
            self.config.output_abs_path, self.source_file.cri_file).replace("\\", "\\\\")

        # create file object string
        file_object_string = ("___CODECONUT_FILE_T " + self._get_file_struct_name() + " = {\n" +
                              "{" + ", ".join(source_hash_array) + "},\n" +
                              "{" + ", ".join(instr_random_array) + "},\n" +
                              "___CODECONUT_BOOL_FALSE,\nNULL,\n " +
                              "\"" + self.source_file.cri_file + "\"};")

        # create full wrapper string
        wrapper_string = (include_string + "\n" + file_object_string + "\n\n")

        # insert wrapper string
        self._insert_text(wrapper_string, 1, 1)
        return

    # !SECTION

    # SECTION   Instrumenter public functions

    def start_instrumentation(self):
        """Start the instrumentation of the configured source code"""
        # prepare all markers
        self._prepare_markers()

        # write markers
        self._write_markers()

        # write wrapper
        self._write_wrapper()

        # print("ORIGINAL:\n" + self.source_code)
        # print("INSTRUMENTED:\n" + self._instrumented_code)
        # TODO implement function
        return

    def write_output_file(self):
        """Create the instrumented source code and write it to a file"""
        with open(self.source_file.output_file, 'w') as output_file_ptr:
            try:
                output_file_ptr.write(self._instrumented_code)
            except:
                raise(RuntimeError(
                    self.source_file.output_file + " can't be written!"))
        return

    # !SECTION
# !SECTION
