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
from .StateMachine import StateMachine, State

from .Configuration import Configuration
from .CIDManager import CIDManager


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

    # !SECTION

    def __init__(self, config: Configuration, cid_manager: CIDManager, input_code: SourceCode):
        """Initializes the new Parser"""

        # TODO implement variable initialization (and sanity checks)
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
        state_machine.init(self._cid_manager)
        state_machine.run(input_data)

        return


class ParserStateMachine(StateMachine):
    """State machine for Parser"""
    # SECTION   ParserStateMachine private attribute definitions
    __slots__ = ['_cid_manager']

    _cid_manager: CIDManager
    # !SECTION

    # SECTION   ParserStateMachine getter functions
    def _get_cid_manager(self) -> CIDManager:
        return self._cid_manager
    # !SECTION

    # SECTION   ParserStateMachine setter functions
    def _set_cid_manager(self, cid_manager):
        if cid_manager is None:
            raise ValueError("cid_manager not defined!")
        elif not issubclass(cid_manager, CIDManager):
            raise TypeError("cid_manager shall be of type CIDManager!")
        else:
            self._cid_manager = cid_manager
    # !SECTION

    # SECTION   ParserStateMachine property definitions
    cid_manager = property(_get_cid_manager, _set_cid_manager)
    # !SECTION

    def init(self, cid_manager):
        self.cid_manager = cid_manager
        self.active_state = ParserStateMachine.IdleState(
            self, self.cid_manager)

    def run(self, input_data):
        self.active_state.run(input_data)
        self.active_state.next(input_data)

    class IdleState(State):
        """Idle State for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class DQMStringState(State):
        """Double quotation mark state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager, last_state):
            State.__init__(self, parent, last_state, None)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class DQMStringNormalState(State):
        """Double quotation mark normal state for Parser"""
        ___slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class DQMStringEscapeState(State):
        """Double quotation mark escape state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class SQMStringState(State):
        """Single quotation mark state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager, last_state):
            State.__init__(self, parent, last_state, None)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class SQMStringNormalState(State):
        """Single quotation mark normal state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class SQMStringEscapeState(State):
        """Single quotation mark escape state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class SLCommentState(State):
        """Single line comment state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager, last_state):
            State.__init__(self, parent, last_state)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class MLCommentState(State):
        """Multi line comment state for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager, last_state):
            State.__init__(self, parent, last_state)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class ClassState(State):
        """Class State (inside a class) for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class FunctionState(State):
        """Function State (inside a function) for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(
                self, parent, FunctionIdleState(self, cid_manager))
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return

    class FunctionIdleState(State):
        """Idle State (inside a class) for Parser"""
        __slots__ = ['_cid_manager']

        def __init__(self, parent, cid_manager):
            State.__init__(self, parent)
            self._cid_manager = cid_manager

        def run(self, input, cid_manager):
            """Run function for state"""
            # TODO implement function
            return

        def next(self, parent, input):
            """Determine next state for state"""
            # TODO implement function
            return
