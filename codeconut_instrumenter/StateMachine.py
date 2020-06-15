#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""State machine patterns for Codeconut Instrumenter.
"""


class StateParent:
    """State machine parent pattern class
    Used to define every other type of State machine class
    in order to improve type safety
    """
    # SECTION   StateParent private attribute definitions
    __slots__ = []
    # !SECTION

    # SECTION   StateParent initialization
    def __init__(self):
        """Initialization routine for state parent pattern
        """
        return
    # !SECTION


class State(StateParent):
    """State machine state pattern class
    """
    # SECTION   State private attribute definitions
    __slots__ = ['_parent', '_stateMachine', '_return_state', '_child_state']

    _parent: StateParent
    _state_machine: 'StateMachine'
    _return_state: 'State'
    _child_state: 'State'
    # !SECTION

    # SECTION   State initialization
    def __init__(self, parent, state_machine, return_state=None, child_state=None):
        """Initialization routine for state machine pattern
        """
        StateParent.__init__(self)
        self.parent = parent
        self.state_machine = state_machine
        if return_state is not None:
            self.return_state = return_state
        if child_state is not None:
            self.child_state = child_state
        return
    # !SECTION

    # SECTION   State getter functions
    def _get_parent(self) -> StateParent:
        return self._parent

    def _get_state_machine(self) -> 'StateMachine':
        return self._state_machine

    def _get_return_state(self) -> 'State':
        return self._return_state

    def _get_child_state(self) -> 'State':
        return self._child_state
    # !SECTION

    # SECTION   State setter functions
    def _set_parent(self, parent):
        if parent is None:
            raise ValueError("parent not defined!")
        elif not issubclass(type(parent), StateParent):
            raise TypeError("parent shall be of type StateParent!")
        else:
            self._parent = parent

    def _set_state_machine(self, state_machine):
        if state_machine is None:
            raise ValueError("state_machine not defined!")
        elif not issubclass(type(state_machine), StateMachine):
            raise TypeError("state_machine shall be of type StateParent!")
        else:
            self._state_machine = state_machine

    def _set_return_state(self, return_state):
        if return_state is None:
            raise ValueError("return_state not defined!")
        elif not issubclass(type(return_state), State):
            raise TypeError("return_state shall be of type State!")
        else:
            self._return_state = return_state

    def _set_child_state(self, child_state):
        if child_state is None:
            raise ValueError("child_state not defined!")
        elif not issubclass(type(child_state), 'State'):
            raise TypeError("child_state shall be of type State!")
        else:
            self._child_state = child_state
    # !SECTION

    # SECTION   State property definitions
    parent = property(_get_parent, _set_parent)
    state_machine = property(_get_state_machine, _set_state_machine)
    return_state = property(_get_return_state, _set_return_state)
    child_state = property(_get_child_state, _set_child_state)
    # !SECTION

    # SECTION   State public function definitions
    def run(self, input):
        """Run function for state"""
        raise NotImplementedError("run function wasn't declared!")
        return

    def next(self, input):
        """Determine next state for state"""
        raise NotImplementedError("next function wasn't declared!")
        return
    # !SECTION


class StateMachine(StateParent):
    """State machine pattern class
    """
    # SECTION   StateMachine private attribute definitions
    __slots__ = ['_child_state', 'states']

    _child_state: State
    # !SECTION

    # SECTION   StateMachine initialization
    def __init__(self, child_state=None):
        """Initialization routine for state machine pattern
        """
        StateParent.__init__(self)
        if child_state is not None:
            self.child_state = child_state
        return
    # !SECTION

    # SECTION   StateMachine getter functions
    def _get_child_state(self) -> State:
        return self._child_state
    # !SECTION

    # SECTION   StateMachine setter functions
    def _set_child_state(self, next_state):
        if next_state is None:
            raise ValueError("next_state not defined!")
        elif not issubclass(type(next_state), State):
            raise TypeError("next_state shall be of type State!")
        else:
            self._child_state = next_state
    # !SECTION

    # SECTION   StateMachine property definitions
    active_state = property(_get_child_state, _set_child_state)
    child_state = property(_get_child_state, _set_child_state)
    # !SECTION

    # SECTION   State machine public function definitions
    def init(self):
        """Initialize state machine with first state"""
        raise NotImplementedError(
            "State machine initialization function wasn't declared!")
        return

    def run(self):
        """Run the state machine"""
        print("Hello!")
        raise NotImplementedError(
            "State machine run function wasn't declared!")
        return
    # !SECTION
