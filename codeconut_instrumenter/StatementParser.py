#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Statement parser for Codeconut Instrumenter.
"""

from .DataTypes import SourceCode
from .Configuration import Configuration
from .CIDManager import CIDManager


class StatementParser:
    """StatementParser class.
       Parses the given code to find statements, groups them and passes them to the given CID Manager.
    """

    __slots__ = ["_config", "_cid_manager", "_input_code"]

    _config: Configuration
    _cid_manager: CIDManager
    _input_code: SourceCode

    def __init__(self, config: Configuration, cid_manager: CIDManager, input_code: SourceCode):
        """Initializes the StatementParser"""

        # TODO implement value initialization (and sanity checks)
        return

    def start_parse(self):
        """Start the parsing of the configured source code"""

        # TODO implement function
        return