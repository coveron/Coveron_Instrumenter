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

from typing import List
from DataTypes import *

from Configuration import Configuration

import hashlib
import string
import random


# SECTION   CIDManager class
class CIDManager:
    """CIDManager class.
       Stores Codeconut Instrumentation Data for a source file
    """
    
    # SECTION   CIDManager private attribute definitions
    __slots__ = ['_config', '_cid_data', '_current_id']

    _config: Configuration
    _cid_data: CIDData
    _current_id: int
    # !SECTION
    
    # SECTION   CIDManager public attribute definitions
    # !SECTION
    
    # SECTION   CIDManager initialization
    def __init__(self, config: Configuration, source_file: SourceFile, sourcecode: SourceCode):

        # Load configuration
        self._config = config

        # Set filename and hash for the source code file
        self._cid_data = CIDData(source_code_filename=source_file.input_filename,
                                 source_code_hash=hashlib.sha256(
                                     sourcecode.encode('utf-8')).hexdigest(),
                                 instrumentation_random=''.join(random.choice(
                                     string.digits +
                                     string.ascii_lowercase +
                                     string.ascii_uppercase) for i in range(16)),
                                 checkpoint_markers_enabled=self._config.checkpoint_markers_enabled,
                                 evaluation_markers_enabled=self._config.evaluation_markers_enabled)
        return
    # !SECTION
    
    # SECTION   CIDManager getter functions
    # !SECTION
    
    # SECTION   CIDManager setter functions
    # !SECTION
    
    # SECTION   CIDManager property definitions
    # !SECTION
    
    # SECTION   CIDManager private functions
    def _get_new_id(self) -> int:
        '''Returns a unique id for the new marker/data'''
        current_id = self._current_id
        self._current_id += 1 # increase id counter by one
        return current_id
    # !SECTION
    
    # SECTION   CIDManager public functions
    def add_checkpoint_marker(self, code_position: CodePositionData) -> int:
        '''Create new checkpoint marker. Returns new checkpoint_marker_id'''
        # get new checkpoint_marker_id
        checkpoint_marker_id = self._get_new_id()
        return checkpoint_marker_id

    def add_evaluation_marker(self, code_position: CodeSectionData) -> int:
        '''Create new evaluation marker. Returns new evaluation_marker_id'''
        # get new evaluation_marker_id
        evaluation_marker_id = self._get_new_id()
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

    def write_cid_file(self, cid_filename: str):
        '''Writes a CID file from the curretly stored information to the specified filepath'''

    # !SECTION
# !SECTION