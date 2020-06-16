#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Parser State Machine for Codeconut Instrumenter.
   Coordinates all the modules responsible for parsing the source code.
"""

from .DataTypes import SourceCode
from .StateMachine import StateMachine, State

from .Configuration import Configuration
from .CIDManager import CIDManager


# SECTION   STATE LIST
class IdleState(State):
    """Idle State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

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
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine, last_state):
        State.__init__(self, parent, state_machine, last_state)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class DQMStringNormalState(State):
    """Double quotation mark normal state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class DQMStringEscapeState(State):
    """Double quotation mark escape state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SQMStringState(State):
    """Single quotation mark state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SQMStringNormalState(State):
    """Single quotation mark normal state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SQMStringEscapeState(State):
    """Single quotation mark escape state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SLCommentState(State):
    """Single line comment state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class MLCommentState(State):
    """Multi line comment state for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class ClassState(State):
    """Class State (inside a class) for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)
        self.code_block_depth = 0

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "IdleState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in IdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class FunctionState(State):
    """Function State (inside a function) for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)
        self.code_block_depth = 0

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionIdleState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class FunctionIdleState(State):
    """Idle State (inside a function) for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class WhileLoopState(State):
    """While Loop State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "WhileLoopDecisionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class WhileLoopDecisionState(State):
    """While Loop Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "WhileLoopConditionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class WhileLoopConditionState(State):
    """While Loop Condition State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class WhileLoopInsideState(State):
    """While Loop Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class ForLoopState(State):
    """For Loop Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "ForLoopDecisionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class ForLoopDecisionState(State):
    """For Loop Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "ForLoopConditionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class ForLoopConditionState(State):
    """For Loop Condition State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class ForLoopInsideState(State):
    """For Loop Inside State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class DoWhileLoopState(State):
    """Do While Loop State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "DoWhileLoopInsideState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class DoWhileLoopInsideState(State):
    """Do While Loop Inside State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class DoWhileLoopDecisionState(State):
    """Do While Loop Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "DoWhileLoopConditionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class DoWhileLoopConditionState(State):
    """Do While Loop Condition State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SwitchBranchState(State):
    """Switch Branch State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "SwitchBranchExpressionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SwitchBranchExpressionState(State):
    """Switch Branch Expression State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class SwitchBranchInsideState(State):
    """Switch Branch Inside State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class IfBranchState(State):
    """If Branch State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "IfBranchDecisionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class IfBranchDecisionState(State):
    """If Branch Decision State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "IfBranchConditionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class IfBranchConditionState(State):
    """If Branch Condition State for Parser"""
    state_machine: 'ParserStateMachine'

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        return


class IfBranchInsideState(State):
    """If Branch Inside State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return


class ElseBranchState(State):
    """Else Branch State for Parser"""
    state_machine: 'ParserStateMachine'

    __slots__ = ["code_block_depth"]
    code_block_depth: int

    def __init__(self, parent, state_machine):
        State.__init__(self, parent, state_machine)

    def run(self, input):
        """Run function for state"""
        # TODO implement function
        # NOTE This state also has a child state. The initial child state is "FunctionState"
        return

    def next(self, input):
        """Determine next state for state"""
        # TODO implement function
        # NOTE If code_block_depth get smaller than 0, we're out of the code block.
        #      Verify, that we're in FunctionIdleState, otherwise invoke a error
        #      (Code Blocks not correct).
        return
# !SECTION


# SECTION   STATE MACHINE DEFINITION
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
        elif not isinstance(cid_manager, CIDManager):
            raise TypeError("cid_manager shall be of type CIDManager!")
        else:
            self._cid_manager = cid_manager
    # !SECTION

    # SECTION   ParserStateMachine property definitions
    cid_manager = property(_get_cid_manager, _set_cid_manager)
    # !SECTION

    # SECTION   ParserStateMachine public function overrides
    def init(self, cid_manager):
        self.cid_manager = cid_manager
        self.active_state = IdleState(self, self)

    def run(self, input_data):
        self.active_state.run(input_data)
        self.active_state.next(input_data)
    # !SECTION
# !SECTION
