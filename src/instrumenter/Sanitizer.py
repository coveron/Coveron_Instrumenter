#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Sanitizer for Codeconut Instrumenter.
   Get's called by the Parser to first create a sanitized copy of the code.
   Parsing is done on sanitized code and instrumntation is done on the real code.
"""

from typing import List
from .DataTypes import *


class Sanitizer:
    """Sanitizer class.
       Sanitizes up the input source code to remove distractions for further parsers.
    """

    __slots__ = []

    def __init__(self):
        """Initialize the new sanitizer"""

        return

    def _sanitize_stage_comments(self, input_code: SourceCode) -> SourceCode:
        """Sanitize the input from comments"""

        # TODO implement function
        return ""

    def _sanitize_stage_strings(self, input_code: SourceCode) -> SourceCode:
        """Sanitize the input from string contents"""

        # TODO implement function
        return ""

    def sanitize_code(self, input_code: SourceCode) -> SourceCode:
        """Fully sanitize the input source code and return the sanitized variant"""

        # TODO implement function
        return ""
