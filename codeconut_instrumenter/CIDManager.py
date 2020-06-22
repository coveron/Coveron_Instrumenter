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

from typing import List
from DataTypes import *

from Configuration import Configuration


# SECTION   CIDManager class
class CIDManager:
    """CIDManager class.
       Stores Codeconut Instrumentation Data for a source file
    """
    
    # SECTION   CIDManager private attribute definitions
    __slots__ = ['_config', '_cid_data', '_source_file', '_current_id']

    _config: Configuration
    _cid_data: CIDData
    _source_file: SourceFile
    _current_id: int
    # !SECTION
    
    # SECTION   CIDManager public attribute definitions
    # !SECTION
    
    # SECTION   CIDManager initialization
    def __init__(self, config: Configuration, source_file: SourceFile, source_code: SourceCode):
        self.config = config
        self.source_file = source_file
        self._current_id = 1 # starting with ID 1
        
        # get SHA256 hash
        source_code_sha256 = hashlib.sha256(source_code.encode('utf-8')).hexdigest()

        # create instrumentation random
        random_string = ''.join(random.choice(string.digits +string.ascii_lowercase + string.ascii_uppercase)
                        for i in range(32))
        instrumentation_random = hashlib.sha256(random_string.encode('utf-8')).hexdigest()[:32]

        # Initialize CIDData object
        self._cid_data = CIDData(source_code_filename=self.source_file.input_filename,
                                 source_code_hash=source_code_sha256,
                                 instrumentation_random=instrumentation_random,
                                 checkpoint_markers_enabled=self.config.checkpoint_markers_enabled,
                                 evaluation_markers_enabled=self.config.evaluation_markers_enabled)
        return
    # !SECTION
    
    # SECTION   CIDManager getter functions
    def _get_config(self) -> Configuration:
        return self._config

    def _get_source_file(self) -> SourceFile:
        return self._source_file
    # !SECTION
    
    # SECTION   CIDManager setter functions
    def _set_config(self, config:Configuration):
        if config is None:
            raise ValueError("config can't be none")
        elif not isinstance(config, Configuration):
            raise TypeError("config shall be of type Configuration")
        else:
            self._config = config

    def _set_source_file(self, source_file:SourceFile):
        if source_file is None:
            raise ValueError("source_file can't be none")
        elif not isinstance(source_file, SourceFile):
            raise TypeError("source_file shall be of type SourceFile")
        else:
            self._source_file = source_file
    # !SECTION
    
    # SECTION   CIDManager property definitions
    config = property(fget=_get_config,
                  fset=_set_config,
                  doc="Stores the config of the Codeconut Instrumenter")
    source_file = property(fget=_get_source_file,
                  fset=_set_source_file,
                  doc="Stores information about the according souce file")
    # !SECTION
    
    # SECTION   CIDManager private functions
    def _get_new_id(self) -> int:
        '''Returns a unique id for the new marker/data'''
        current_id = self._current_id
        self._current_id += 1 # increase id counter by one
        return current_id
    # !SECTION
    
    # SECTION   CIDManager public functions
    def get_instrumentation_random(self) -> str:
        return self._cid_data.instrumentation_random

    def get_source_code_hash(self) -> str:
        return self._cid_data.source_code_hash

    def get_checkpoint_markers(self) -> list:
        # reutrn deepcopy to prevent accidental changes
        return copy.deepcopy(self._cid_data.marker_data.checkpoint_markers)

    def get_evaluation_markers(self) -> list:
        return copy.deepcopy(self._cid_data.marker_data.evaluation_markers)

    def add_checkpoint_marker(self, code_position: CodePositionData) -> int:
        '''Create new checkpoint marker. Returns new checkpoint_marker_id'''
        # get new checkpoint_marker_id
        checkpoint_marker_id = self._get_new_id()

        self._cid_data.marker_data.checkpoint_markers.append(
                CheckpointMarkerData(checkpoint_marker_id, code_position))
        return checkpoint_marker_id

    def add_evaluation_marker(self, code_section: CodeSectionData, evaluation_type: EvaluationType) -> int:
        '''Create new evaluation marker. Returns new evaluation_marker_id'''
        # get new evaluation_marker_id
        evaluation_marker_id = self._get_new_id()

        self._cid_data.marker_data.evaluation_markers.append(
                EvaluationMarkerData(evaluation_marker_id, evaluation_type, code_section))
        return evaluation_marker_id

    def add_class_data(self, class_name: str) -> int:
        '''Create new class in code data. Returns new class_id'''
        # get new class_id
        class_id = self._get_new_id()
        return class_id
    
    def add_function_data(self,
                          function_name: str,
                          function_type: FunctionType,
                          parent_function_id: int,
                          checkpoint_marker_id: int,
                          header_code_section: CodeSectionData,
                          inner_code_section: CodeSectionData) -> int:
        '''Create new function in code data. Returns new function_id'''
        # get new function_id
        function_id = self._get_new_id()
        return function_id

    def add_statement_data(self,
                           statement_type: StatementType,
                           function_id: int,
                           checkpoint_marker_id: int,
                           code_section: CodeSectionData) -> int:
        '''Create new statement in code data. Returns new statement_id'''
        # get new statement_id
        statement_id = self._get_new_id()
        return statement_id

    def add_if_branch_data(self,
                           function_id: int,
                           branch_results: List[BranchResultData]) -> int:
        '''Create new if branch in code data. Returns new if_branch_id'''
        # get new if_branch_id
        if_branch_id = self._get_new_id()
        return if_branch_id

    def add_switch_branch_data(self,
                               function_id: int,
                               expression_code_section: CodeSectionData,
                               cases: List[CaseData]) -> int:
        '''Create new switch branch in code data. Returns new switch_branch_id'''
        # get new switch_branch_id
        switch_branch_id = self._get_new_id()
        return switch_branch_id

    def add_loop_data(self,
                      loop_type: LoopType,
                      function_id: int,
                      evaluation_marker_id: int,
                      evaluation_code_section: CodeSectionData,
                      body_code_section: CodeSectionData,
                      conditions: List[ConditionData]) -> int:
        '''Create new loop in code data. Returns new loop_id'''
        loop_id = self._get_new_id()
        return loop_id

    def write_cid_file(self):
        '''Writes a CID file from the curretly stored information to the specified filepath'''
        cid_filename = self.source_file.cid_filename
    # !SECTION
# !SECTION