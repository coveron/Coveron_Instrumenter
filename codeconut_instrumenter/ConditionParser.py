#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Condition parser for Codeconut Instrumenter.
   Extends the decision parser by parsing individual conditions (useful for MC/DC).
"""

from .DataTypes import SourceCode, CodeSectionData

from .CIDManager import CIDManager


class ConditionParser:
    """ConditionParser class.
       Parses the given code to find conditions inside a decision and pass them to the given CID Manager.
    """

    __slots__ = ["_cid_manager", "_input_code", "_parent_id", "_code_section"]

    _cid_manager: CIDManager
    _input_code: SourceCode
    _parent_id: int
    _code_section: CodeSectionData

    def __init__(self,
                 cid_manager: CIDManager,
                 input_code: SourceCode,
                 parent_id: int,
                 code_section: CodeSectionData):
        """Initializes the ConditionParser"""

        # TODO implement value initialization (and sanity checks)
        return

    def start_parse(self):
        """Start the parsing of the configured source code"""

        # TODO implement parsing algorithm
        return
