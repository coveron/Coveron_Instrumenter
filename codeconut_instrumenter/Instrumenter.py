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
    __slots__ = ["code_line", "code_column", "marker_type", "marker_id", "condition"]

    code_line: int # line of the code insertion position
    code_column: int # column of the code insertion position
    marker_type: InstrumenterMarkerType # type of the instrumenter marker
    marker_id: int
    condition: bool
# !SECTION


# SECTION   Instrumenter class
class Instrumenter:
    """Instrumenter class.
       Uses the given marker data from the CIDData and generates a instrumented source file
    """
    
    # SECTION   Instrumenter private attribute definitions
    __slots__ = ["_config", "_cid_manager", "_source_file", "_source_code",
                 "_instrumented_code", "_instrumenter_marker_list"]

    _config: Configuration
    _cid_manager: CIDManager
    _source_file: SourceFile
    _source_code: SourceCode
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
        return
    # !SECTION
    
    # SECTION   Instrumenter getter functions
    def _get_config(self) -> Configuration:
        return self._config

    def _get_cid_manager(self) -> CIDManager:
        return self._cid_manager

    def _get_source_file(self) -> SourceFile:
        return self._source_file

    def _get_source_code(self) -> SourceCode:
        return self._source_code
    # !SECTION
    
    # SECTION   Instrumenter setter functions
    def _set_config(self, config:Configuration):
        if config is None:
            raise ValueError("config can't be none")
        elif not isinstance(config, Configuration):
            raise TypeError("config shall be of type Configuration")
        else:
            self._config = config

    def _set_cid_manager(self, cid_manager:CIDManager):
        if cid_manager is None:
            raise ValueError("cid_manager can't be none")
        elif not isinstance(cid_manager, CIDManager):
            raise TypeError("cid_manager shall be of type CIDManager")
        else:
            self._cid_manager = cid_manager

    def _set_source_file(self, source_file:SourceFile):
        if source_file is None:
            raise ValueError("source_file can't be none")
        elif not isinstance(source_file, SourceFile):
            raise TypeError("source_file shall be of type SourceFile")
        else:
            self._source_file = source_file

    def _set_source_code(self, source_code:SourceCode):
        if source_code is None:
            raise ValueError("source_code can't be none")
        elif not isinstance(source_code, SourceCode):
            raise TypeError("source_code shall be of type SourceCode")
        else:
            self._source_code = source_code
    # !SECTION
    
    # SECTION   Instrumenter property definitions
    config: Configuration = property(fget=_get_config,
                  fset=_set_config,
                  doc="Stores the config of the Codeconut Instrumenter")
    cid_manager: CIDManager = property(fget=_get_cid_manager,
                  fset=_set_cid_manager,
                  doc="Stores the CID Manager of the source file")
    source_file: SourceFile = property(fget=_get_source_file,
                  fset=_set_source_file,
                  doc="Stores source file informations")
    source_code: SourceCode = property(fget=_get_source_code,
                  fset=_set_source_code,
                  doc="Stores the source code")
    # !SECTION
    
    # SECTION   Instrumenter private functions

    def _prepare_markers(self):
        """Takes all markers from CIDData and creates preprocessed markers for instrumentation"""
        # TODO implement function
        return

    def _write_markers(self):
        """Modify the input source code to integrate the marker calls"""

        # TODO implement function
        return

    def _write_wrapper(self):
        """Modify the input source code to integrate other necessary defines and calls"""
        # TODO implement function
        return

    # !SECTION
    
    # SECTION   Instrumenter public functions

    def start_instrumentation(self):
        """Start the instrumentation of the configured source code"""

        # TODO implement function
        return

    def write_output_file(self):
        """Create the instrumented source code and write it to a file"""

        # TODO implement function
        return

    # !SECTION
# !SECTION
