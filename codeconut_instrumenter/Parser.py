#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Parser for Codeconut Instrumenter.
   Coordinates all the modules responsible for parsing the source code.
"""

from .DataTypes import SourceCode

from .Configuration import Configuration
from .CIDManager import CIDManager

from .ParserStateMachine import ParserStateMachine


class Parser:
    """Parser class.
       Coordinates all parsers for the source code.
    """
    # SECTION   Parser private attribute definitions
    __slots__ = ['_config', '_cid_manager', '_input_code']

    _config: Configuration
    _cid_manager: CIDManager
    _input_code: SourceCode
    # !SECTION

    # SECTION   Parser getter functions
    def _get_config(self) -> Configuration:
        return self._config

    def _get_cid_manager(self) -> CIDManager:
        return self._cid_manager

    def _get_input_code(self) -> SourceCode:
        return self._input_code
    # !SECTION

    # SECTION   Parser setter functions
    def _set_config(self, config):
        if config is None:
            raise ValueError("config not defined!")
        elif not isinstance(config, Configuration):
            raise TypeError("config shall be of type Configuration!")
        else:
            self._config = config

    def _set_cid_manager(self, cid_manager):
        if cid_manager is None:
            raise ValueError("cid_manager not defined!")
        elif not isinstance(cid_manager, CIDManager):
            raise TypeError("cid_manager shall be of type CIDManager!")
        else:
            self._cid_manager = cid_manager

    def _set_input_code(self, input_code):
        if input_code is None:
            raise ValueError("input_code not defined!")
        elif not isinstance(input_code, SourceCode):
            raise TypeError("input_code shall be of type SourceCode!")
        else:
            self._input_code = input_code
    # !SECTION

    # SECTION   Parser property definitions
    config = property(_get_config, _set_config)
    cid_manager = property(_get_cid_manager, _set_cid_manager)
    input_code = property(_get_input_code, _set_input_code)
    # !SECTION

    def __init__(self, config: Configuration, cid_manager: CIDManager, input_code: SourceCode):
        """Initializes the new Parser"""
        self.config = config
        self.cid_manager = cid_manager
        self.input_code = input_code
        return

    def start_parser(self):
        """Starts the parsing of the input source code"""

        input_data = {
            "code": "TEST",
            "current_line": 0,
            "current_column": 0
        }

        # TODO implement function
        state_machine = ParserStateMachine()
        state_machine.init(self.cid_manager)
        state_machine.run(input_data)

        return
