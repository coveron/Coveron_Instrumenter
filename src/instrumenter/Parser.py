#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Parser for Codeconut Instrumenter.
   Coordinates all the modules responsible for parsing the source code.
"""

from typing import List
from .DataTypes import *

from .Configuration import Configuration
from .CIDManager import CIDManager
from .Sanitizer import Sanitizer
from .StatementParser import StatementParser
from .DecisionParser import DecisionParser

import hashlib
import string


class Parser:
    """Parser class.
       Coordinates all parsers for the source code.
    """

    __slots__ = ['_config', '_cid_manager', '_sanitizer', '_input_code',
                 '_sanitized_code', '_statement_parser', '_decision_parser']

    _config: Configuration
    _cid_manager: CIDManager
    _sanitizer: Sanitizer
    _input_code: SourceCode
    _sanitizied_code: SourceCode
    _statement_parser: StatementParser
    _decision_parser: DecisionParser

    def __init__(self, config: Configuration, input_filename: str, input_code: SourceCode):
        """Initializes the new Parser"""

        # TODO implement variable initialization (and sanity checks)
        return

    def start_parser(self):
        """Starts the parsing of the input source code"""

        # TODO implement function
        return

    def _parser_stage_sanitize(self):
        """Execute the sanitizer for the input source code"""

        # TODO implement function
        return

    def _parser_stage_statements(self):
        """Execute the statements parsing stage for the input source code"""

        # TODO implement function
        return

    def _parser_stage_decisions(self):
        """Execute the decisions parsing stage for the input source code"""

        # TODO implement function
        return
