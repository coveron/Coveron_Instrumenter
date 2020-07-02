#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""CID-Manager for Codeconut Instrumenter.
   Contains all instrumentation data during runtime.
"""

import hashlib
import string
import random
import os
import copy
import json
import gzip
import base64

from typing import List

from DataTypes import *
from Configuration import Configuration


# SECTION   CIDManager class
class CIDManager:
    """CIDManager class.
       Stores Codeconut Instrumentation Data for a source file
    """

    # SECTION   CIDManager private attribute definitions
    __slots__ = ['config', '_cid_data', 'source_file', '_current_id']

    config: Configuration
    _cid_data: CIDData
    source_file: SourceFile
    _current_id: int
    # !SECTION

    # SECTION   CIDManager public attribute definitions
    # !SECTION

    # SECTION   CIDManager initialization
    def __init__(self, config: Configuration, source_file: SourceFile, source_code: SourceCode):
        self.config = config
        self.source_file = source_file
        self._current_id = 1  # starting with ID 1

        # get SHA256 hash
        source_code_sha256 = hashlib.sha256(
            source_code.encode('utf-8')).hexdigest()

        # create instrumentation random
        random_string = ''.join(random.choice(string.digits + string.ascii_lowercase + string.ascii_uppercase)
                                for i in range(32))
        instrumentation_random = hashlib.sha256(
            random_string.encode('utf-8')).hexdigest()[:32]

        # Initialize CIDData object
        self._cid_data = CIDData(source_code_path=self.source_file.input_file,
                                 source_code_hash=source_code_sha256,
                                 source_code_base64=str(
                                     base64.b64encode(source_code.encode("utf-8")), "utf-8"),
                                 instrumentation_random=instrumentation_random,
                                 checkpoint_markers_enabled=self.config.checkpoint_markers_enabled,
                                 evaluation_markers_enabled=self.config.evaluation_markers_enabled)
        return
    # !SECTION

    # SECTION   CIDManager getter functions
    # !SECTION

    # SECTION   CIDManager setter functions
    # !SECTION

    # SECTION   CIDManager property definitions
    # !SECTION

    # SECTION   CIDManager private functions
    # !SECTION

    # SECTION   CIDManager public functions
    def get_new_id(self) -> int:
        '''Returns a unique id for the new marker/data'''
        current_id = self._current_id
        self._current_id += 1  # increase id counter by one
        return current_id

    def get_instrumentation_random(self) -> str:
        return self._cid_data.instrumentation_random

    def get_source_code_hash(self) -> str:
        return self._cid_data.source_code_hash

    def get_checkpoint_markers(self) -> list:
        # reutrn deepcopy to prevent accidental changes
        return copy.deepcopy(self._cid_data.marker_data.checkpoint_markers)

    def get_evaluation_markers(self) -> list:
        return copy.deepcopy(self._cid_data.marker_data.evaluation_markers)

    def add_checkpoint_marker(self, checkpoint_marker_id: int,
                              code_position: CodePositionData) -> int:
        '''Create new checkpoint marker. Returns new checkpoint_marker_id'''

        self._cid_data.marker_data.checkpoint_markers.append(
            CheckpointMarkerData(checkpoint_marker_id, code_position))
        return checkpoint_marker_id

    def add_evaluation_marker(self, evaluation_marker_id: int,
                              code_section: CodeSectionData, evaluation_type: EvaluationType) -> int:
        '''Create new evaluation marker. Returns new evaluation_marker_id'''
        self._cid_data.marker_data.evaluation_markers.append(
            EvaluationMarkerData(evaluation_marker_id, evaluation_type, code_section))
        return evaluation_marker_id

    def add_class_data(self, class_id: int, class_name: str) -> int:
        '''Create new class in code data. Returns new class_id'''
        self._cid_data.code_data.classes.append(
            ClassData(class_id, class_name))
        return class_id

    def add_function_data(self,
                          function_id: int,
                          function_name: str,
                          function_type: FunctionType,
                          parent_function_id: int,
                          checkpoint_marker_id: int,
                          header_code_section: CodeSectionData,
                          inner_code_section: CodeSectionData) -> int:
        '''Create new function in code data. Returns new function_id'''
        self._cid_data.code_data.functions.append(FunctionData(function_id, function_name,
                                                               function_type, parent_function_id, checkpoint_marker_id, header_code_section, inner_code_section))
        return function_id

    def add_statement_data(self,
                           statement_id: int,
                           statement_type: StatementType,
                           function_id: int,
                           checkpoint_marker_id: int,
                           code_section: CodeSectionData) -> int:
        '''Create new statement in code data. Returns new statement_id'''
        self._cid_data.code_data.statements.append(StatementData(statement_id, statement_type, function_id,
                                                                 checkpoint_marker_id, code_section))
        return statement_id

    def add_if_branch_data(self,
                           if_branch_id: int,
                           function_id: int,
                           branch_results: List[BranchResultData]) -> int:
        '''Create new if branch in code data. Returns new if_branch_id'''
        self._cid_data.code_data.if_branches.append(
            IfBranchData(if_branch_id, function_id, branch_results))
        return if_branch_id

    def add_switch_branch_data(self,
                               switch_branch_id: int,
                               function_id: int,
                               expression_code_section: CodeSectionData,
                               cases: List[CaseData]) -> int:
        '''Create new switch branch in code data. Returns new switch_branch_id'''
        self._cid_data.code_data.switch_branches.append(SwitchBranchData(switch_branch_id, function_id,
                                                                         expression_code_section, cases))
        return switch_branch_id

    def add_ternary_expression_data(self,
                                    ternary_expression_id: int,
                                    function_id: int,
                                    evaluation_marker_id: int,
                                    evaluation_code_section: CodeSectionData,
                                    condition_possibilities,
                                    conditions: List[ConditionData],
                                    true_code_section: CodeSectionData,
                                    false_code_section: CodeSectionData
                                    ):
        '''Create new ternary expression in code data. Return new ternary_expression_id'''
        self._cid_data.code_data.ternary_expressions.append(TernaryExpressionData(ternary_expression_id,
                                                                                  function_id, evaluation_marker_id, evaluation_code_section, condition_possibilities, conditions, true_code_section,
                                                                                  false_code_section))

    def add_loop_data(self,
                      loop_id: int,
                      loop_type: LoopType,
                      function_id: int,
                      evaluation_marker_id: int,
                      evaluation_code_section: CodeSectionData,
                      body_code_section: CodeSectionData,
                      condition_possibilities,
                      conditions: List[ConditionData]) -> int:
        '''Create new loop in code data. Returns new loop_id'''
        self._cid_data.code_data.loops.append(LoopData(loop_id, loop_type, function_id, evaluation_marker_id,
                                                       evaluation_code_section, body_code_section, condition_possibilities, conditions))
        return loop_id

    def write_cid_file(self):
        '''Writes a CID file from the curretly stored information to the specified filepath'''
        cid_file = self.source_file.cid_file

        cid_string = json.dumps(self._cid_data.asJSON(),
                                cls=CustomJSONEncoder, indent=4)

        if self.config.nocomp_cid:
            with open(os.path.join(self.config.output_abs_path, self.source_file.cid_file), 'w') as output_file_ptr:
                try:
                    output_file_ptr.write(cid_string)
                except:
                    raise(RuntimeError(
                        self.source_file.cid_file + " can't be written!"))

        else:
            # Routine for saving gzip compressed data (not needed during first development)
            cid_bytes = cid_string.encode('utf-8')

            with gzip.GzipFile(os.path.join(self.config.output_abs_path, self.source_file.cid_file), 'w') as output_file_ptr:
                try:
                    output_file_ptr.write(cid_bytes)
                except:
                    raise(RuntimeError(
                        self.source_file.cid_file + " can't be written!"))
    # !SECTION
# !SECTION
