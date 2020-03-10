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
from .DataTypes import SourceCode, MarkerData

from .Configuration import Configuration
from .CIDManager import CIDManager


class Instrumenter:
    """Instrumenter class.
       Instruments the given input code according to the information from the markers.
    """

    __slots__ = ["_config", "_markers", "_cid_manager",
                 "_input_code", "_instrumented_code"]

    _config: Configuration
    _markers: List[MarkerData]
    _cid_manager: CIDManager
    _input_code: SourceCode
    _instrumented_code: SourceCode

    def __init__(self, config: Configuration, cid_manager: CIDManager, input_code: SourceCode):
        """Initializes the Instrumenter"""

        # TODO implement value initialization (and sanity checks)
        return

    def start_instrumentation(self):
        """Start the instrumentation of the configured source code"""

        # TODO implement function
        return

    def write_output_file(self, filename: str):
        """Create the instrumented source code and write it to a file"""

        # TODO implement function
        return

    def _write_markers(self):
        """Modify the input source code to integrate the marker calls"""

        # TODO implement function
        return

    def _write_wrapper(self):
        """Modify the input source code to integrate other necessary defines and calls"""
