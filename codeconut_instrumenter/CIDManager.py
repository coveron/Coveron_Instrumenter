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
from .DataTypes import SourceCode, CodeSectionData, MarkerData, CIDData

from .Configuration import Configuration

import hashlib
import string
import random


class CIDManager:
    """CID-Manager class.
       Contains all instrumentation data during runtime.
    """

    __slots__ = ['_config', '_cid_data']

    _config: Configuration
    _cid_data: CIDData

    def __init__(self, config: Configuration, input_filename: str, input_code: SourceCode):
        """Initializes the new CID Manager"""

        # Load configuration
        self._config = config

        # Set filename and hash for the soruce code file
        self._cid_data = CIDData()
        self._cid_data.source_code_filename = input_filename
        self._cid_data.source_code_hash = hashlib.sha256(
            input_code.encode('utf-8'))

        # Generate instrumentation random (16 chars, a-zA-Z0-9 possible)
        self._cid_data.instrumentation_random = ''.join(random.choice(
            string.digits + string.ascii_lowercase + string.ascii_uppercase) for i in range(16))

        # Enable/Disable specific markers according to configuration
        self._cid_data.statement_markers_enabled = self._config.statement_analysis_enabled
        self._cid_data.decision_markers_enabled = self._config.decision_analysis_enabled
        self._cid_data.condition_markers_enabled = self._config.condition_analysis_enabled

    def _get_new_marker_id(self) -> int:
        """Generates a new id for new markers"""

        if len(self._cid_data.marker_data) == 0:
            return 1
        else:
            return self._cid_data.marker_data[-1].marker_id + 1

    def _code_section_inside_parent(self, parent_code_section: CodeSectionData, child_code_section: CodeSectionData) -> bool:
        """Validates, that a given child code section is inside the parent code section"""

        # TODO Implement function
        return True

    def create_statement_marker(self, statement_collection: List[CodeSectionData]) -> int:
        """Creates a new statement marker from the specified statement collection"""

        # TODO Implement function
        return  # marker_id

    def create_decision_marker(self, code_section_data: CodeSectionData) -> int:
        """Creates a new decision marker from the specified code section"""

        # TODO Implement function
        return  # marker_id

    def create_condition_marker(self, decision_marker_id: int, code_section_data: CodeSectionData) -> int:
        """Creates a new condition marker from the specified parent decision marker ID and the code section"""

        # TODO Implement function
        return  # marker_id

    def get_markers(self) -> List[MarkerData]:
        """Returns a list of the currently stored marker data"""

        # TODO Implement function
        return self._cid_data.marker_data

    def write_cid_file(self, filename: str):
        """Writes a CID file form the currently stored information to the specified filepath/filename"""

        # TODO Implement function
        return
