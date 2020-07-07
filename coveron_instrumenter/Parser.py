#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Parser for Coveron Instrumenter.
   Coordinates all the modules responsible for parsing the source code.
"""

import clang.cindex

from DataTypes import *

from Configuration import Configuration
from CIDManager import CIDManager


# SECTION   ClangBridge class
class ClangBridge:
    """ClangBridge class.
       Connects libclang to Coveron Instrumenter by
       returning the Clang AST of a input file
    """

    # SECTION   ClangBridge private attribute definitions
    # !SECTION

    # SECTION   ClangBridge public attribute definitions
    # !SECTION

    # SECTION   ClangBridge initialization
    def __init__(self):
        if not clang.cindex.Config.loaded:
            clang.cindex.Config.set_library_path(os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "clang", "bin"))
        return
    # !SECTION

    # SECTION   ClangBridge getter functions
    # !SECTION

    # SECTION   ClangBridge setter functions
    # !SECTION

    # SECTION   ClangBridge property definitions
    # !SECTION

    # SECTION   ClangBridge private functions
    # !SECTION

    # SECTION   ClangBridge public functions
    def clang_parse(self, file, parse_args) -> clang.cindex.Cursor:
        """Invoke libclang to parse the given source file"""
        clang_index = clang.cindex.Index.create()
        tu = clang_index.parse(file, [parse_args]).cursor
        return tu
    # !SECTION
# !SECTION


# SECTION   Parser class
class Parser:
    """Parser class.
       Parses the source code by using the passed Clang AST
    """

    # SECTION   Parser private attribute definitions
    __slots__ = ['config', 'cid_manager', 'clang_ast']

    config: Configuration
    cid_manager: CIDManager
    clang_ast: clang.cindex.Cursor
    # !SECTION

    # SECTION   Parser public attribute definitions
    # !SECTION

    # SECTION   Parser initialization
    def __init__(self, config: Configuration, cid_manager: CIDManager, clang_ast: clang.cindex.Cursor):
        self.config = config
        self.cid_manager = cid_manager
        self.clang_ast = clang_ast
        return
    # !SECTION

    # SECTION   Parser getter functions
    # !SECTION

    # SECTION   Parser setter functions
    # !SECTION

    # SECTION   Parser property definitions
    # !SECTION

    # SECTION   Parser private functions
    def _traverse_root(self, ast_pointer: clang.cindex.Cursor):
        """Searches for functions inside the code of the active source file."""

        for root_child in ast_pointer.get_children():
            root_child: clang.cindex.Cursor

            location: clang.cindex.SourceLocation = root_child.location
            location_file: str = location.file.name
            location_file = location_file.replace(
                '\\\\', '/').replace('\\', '/').split('/')[-1]

            if location_file != os.path.basename(self.cid_manager.source_file.input_file):
                # Child is not in the correct file, so we can ignore it
                continue

            kind: clang.cindex.CursorKind = root_child.kind
            if kind == clang.cindex.CursorKind.FUNCTION_DECL:
                self._traverse_function(
                    root_child, dict(parent_function_id=-1))
        # Travel through the first layer of the AST.
        # Goal: Find functions with a source file name equal to the file name of the instrumented code.
        #       (ignore headers etc.)
        return

    def _traverse_function(self, ast_cursor: clang.cindex.Cursor, args: dict):
        """Parses a function passed to it"""
        function_id = self.cid_manager.get_new_id()
        function_name = ast_cursor.displayname
        function_type = FunctionType.NORMAL
        parent_function_id = args.get("parent_function_id", -1)

        header_code_section = CodeSectionData(
            CodePositionData(ast_cursor.extent.start.line,
                             ast_cursor.extent.start.column),
            None
        )

        inner_code_section: CodeSectionData = None

        inner_traverse_args = dict(
            is_case=False,
            parent_function_id=function_id
        )

        inner_return_data = dict()

        for function_child in ast_cursor.get_children():
            if function_child.kind == clang.cindex.CursorKind.COMPOUND_STMT:
                # function body found!

                # set header code section end
                header_code_section.end_position = CodePositionData(
                    function_child.location.line,
                    function_child.location.column
                )

                # set inner code section
                inner_code_section = CodeSectionData(
                    CodePositionData(function_child.extent.start.line,
                                     function_child.extent.start.column),
                    CodePositionData(function_child.extent.end.line,
                                     function_child.extent.end.column)
                )

                # call analysis of function internals
                self._traverse_compound_statement(
                    function_child, inner_traverse_args, inner_return_data)

        self.cid_manager.add_function_data(function_id, function_name, function_type, parent_function_id,
                                           inner_return_data['first_checkpoint_marker_id'], header_code_section, inner_code_section)
        return

    def _traverse_compound_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Parses a compound statement given to it"""
        # use given checkpoint_marker_id if passed (i.e. CompoundStmt in CompoundStmt)
        active_checkpoint_marker_id = args.get(
            'start_checkpoint_marker_id', self.cid_manager.get_new_id())
        return_data['first_checkpoint_marker_id'] = active_checkpoint_marker_id
        # status variable to check, if the first checkpoint was set
        first_checkpoint_set = False
        # status variable to check,
        # if a new checkpoint request shall be passed to the parent
        return_data['new_parent_checkpoint_required'] = False
        # status variable to check, if a new checkpoint is neccessary
        new_checkpoint_required = False

        # set first_checkpoint_set to true, if 'start_checkpoint_marker_id' was set
        if args.get('start_checkpoint_marker_id') is not None:
            first_checkpoint_set = True

        # get all child elements
        child_elements = ast_cursor.get_children()

        # if this is a case statement, skip the first statement, since that is the evaluation
        if ast_cursor.kind == clang.cindex.CursorKind.CASE_STMT:
            next(child_elements)

        # iterate over all child statements in this compound statement
        for child_element in child_elements:
            # get the element type
            child_kind: clang.cindex.CursorKind = child_element.kind

            # check, if the active statement is a label statement.
            # If yes, we should skip it and create a new checkpoint
            if child_kind == clang.cindex.CursorKind.LABEL_STMT:
                new_checkpoint_required = True
                continue

            # check, if the first checkpoint wasn't set. If no, set it up.
            # Inject at start of current element.
            if not first_checkpoint_set and self.config.checkpoint_markers_enabled:
                first_checkpoint_set = True
                self.cid_manager.add_checkpoint_marker(active_checkpoint_marker_id,
                                                       CodePositionData(child_element.extent.start.line, child_element.extent.start.column))

            # check, if a new checkpoint is required since the last child element
            if new_checkpoint_required and self.config.checkpoint_markers_enabled:
                # get new id for new checkpoint
                active_checkpoint_marker_id = self.cid_manager.get_new_id()
                # insert new checkpoint marker
                self.cid_manager.add_checkpoint_marker(active_checkpoint_marker_id,
                                                       CodePositionData(child_element.extent.start.line, child_element.extent.start.column))
                new_checkpoint_required = False

            # check for other types of Cursors for further handling
            if child_kind == clang.cindex.CursorKind.RETURN_STMT:
                # a new checkpoint marker will be neccessary (for parent elements also), so set it up
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                                                    StatementType.RETURN, args['parent_function_id'], active_checkpoint_marker_id,
                                                    CodeSectionData(
                    CodePositionData(
                        child_element.extent.start.line, child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column)))

            elif child_kind == clang.cindex.CursorKind.BREAK_STMT:
                # same a with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                                                    StatementType.BREAK, args['parent_function_id'], active_checkpoint_marker_id,
                                                    CodeSectionData(
                    CodePositionData(
                        child_element.extent.start.line, child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column)))

            elif child_kind == clang.cindex.CursorKind.CONTINUE_STMT:
                # same as with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                                                    StatementType.CONTINUE, args[
                                                        'parent_function_id'], active_checkpoint_marker_id,
                                                    CodeSectionData(
                    CodePositionData(
                        child_element.extent.start.line, child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column)))

            elif (child_kind == clang.cindex.CursorKind.GOTO_STMT or
                    child_kind == clang.cindex.CursorKind.INDIRECT_GOTO_STMT):
                # same as with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                                                    StatementType.GOTO, args['parent_function_id'], active_checkpoint_marker_id,
                                                    CodeSectionData(
                    CodePositionData(
                        child_element.extent.start.line, child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column)))

            elif child_kind == clang.cindex.CursorKind.COMPOUND_STMT:
                # found a compound statement, so do a recursive call
                inner_traverse_args = dict(
                    is_case=False,
                    parent_function_id=args['parent_function_id'],
                    start_checkpoint_marker_id=active_checkpoint_marker_id
                )
                inner_return_data = dict()
                self._traverse_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is neccessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.IF_STMT:
                # found a if_branch, so open the if statement handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_if_statement(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is neccessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.SWITCH_STMT:
                # found a switch_branch, so open the switch statement handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_switch_statement(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is neccessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
                # found a ternary expression, so open the ternary expression handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_ternary_statement(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is necessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.FOR_STMT:
                # found a for loop, so open the for loop handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_for_loop(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is necessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.WHILE_STMT:
                # found a while loop, so open the while loop handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_while_loop(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is necessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            elif child_kind == clang.cindex.CursorKind.DO_STMT:
                # found a do-while loop, so open the do-while loop handler
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._traverse_do_while_loop(
                    child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is necessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required'] = True

            else:
                # recursively search for ternary expressions, since they're often hidden
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()
                self._search_for_ternary(
                    child_element, inner_traverse_args, inner_return_data)

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                                                    StatementType.NORMAL, args['parent_function_id'], active_checkpoint_marker_id,
                                                    CodeSectionData(
                    CodePositionData(
                        child_element.extent.start.line, child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                )

    def _traverse_evaluation(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a evaluation and return a list of conditions with evaluation_marker_ids and code_sections"""

        # Create conditions var to store all child conditions for this function call
        conditions = list()

        if not args.get('is_condition', False):
            # This is a decision

            # Pass current cursor to _traverse_evaluation again, but as condition
            inner_traverse_args = dict(is_condition=True)
            inner_return_data = dict(
                conditions=list(), condition_possibilities=dict(true=[], false=[]))
            self._traverse_evaluation(
                ast_cursor, inner_traverse_args, inner_return_data)
            # append conditions
            conditions.extend(inner_return_data['conditions'])

            # Create evaluation_code_section and EvaluationMarker for the whole decision
            # and pass back all the information
            evaluation_marker_id = self.cid_manager.get_new_id()
            evaluation_code_section = CodeSectionData(
                CodePositionData(ast_cursor.extent.start.line,
                                 ast_cursor.extent.start.column),
                CodePositionData(ast_cursor.extent.end.line, ast_cursor.extent.end.column))
            self.cid_manager.add_evaluation_marker(evaluation_marker_id, evaluation_code_section,
                                                   EvaluationType.DECISION)
            return_data['evaluation_marker_id'] = evaluation_marker_id
            return_data['evaluation_code_section'] = evaluation_code_section
            return_data['conditions'] = conditions
            return_data['condition_possibilities'] = (
                inner_return_data['condition_possibilities'])

        else:
            # This is a (compound) condition

            # Check, if it's a ParenExpr or a BinaryOperator for Compounding.
            # If yes, recursively jump into children of the active cursor
            if (ast_cursor.kind == clang.cindex.CursorKind.PAREN_EXPR or
                    (ast_cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR and
                     (ast_cursor.binary_operator == clang.cindex.BinaryOperator.LAnd or
                      ast_cursor.binary_operator == clang.cindex.BinaryOperator.LOr))):

                # store condition possibilities for both sides in order to generate table after traversing children
                left_condition_possibilities: list()
                right_condition_possibilities: list()

                for i, child_element in enumerate(ast_cursor.get_children()):
                    # create the necessary pass thru variables
                    inner_traverse_args = dict(is_condition=True)
                    inner_return_data = dict(
                        conditions=list(), condition_possibilities=list())
                    self._traverse_evaluation(
                        child_element, inner_traverse_args, inner_return_data)
                    # append conditions
                    conditions.extend(inner_return_data['conditions'])
                    return_data['conditions'] = conditions

                    # Create the table for condition possibilities
                    if (ast_cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR):
                        if i == 0:
                            left_condition_possibilities = inner_return_data['condition_possibilities']
                        elif i == 1:
                            right_condition_possibilities = inner_return_data['condition_possibilities']
                    elif (ast_cursor.kind == clang.cindex.CursorKind.PAREN_EXPR):
                        return_data['condition_possibilities'] = inner_return_data['condition_possibilities']

                # Create condition possibility table for MC/DC analysis
                if (ast_cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR and
                        ast_cursor.binary_operator == clang.cindex.BinaryOperator.LAnd):
                    condition_possibilities = list()

                    for left_condition_result in filter(lambda x: x.decision_result == True, left_condition_possibilities):
                        for right_condition_result in filter(lambda x: x.decision_result == True, right_condition_possibilities):
                            # both sides are true, so add this to the possible compound condition results for true
                            condition_possibilities.append(
                                ConditionPossibility(True,
                                                     left_condition_result.condition_combination + right_condition_result.condition_combination))

                        for right_condition_result in filter(lambda x: x.decision_result == False, right_condition_possibilities):
                            # right side is false, so add this to the possible compound condition results for false
                            condition_possibilities.append(
                                ConditionPossibility(False,
                                                     left_condition_result.condition_combination + right_condition_result.condition_combination))

                    for left_condition_result in filter(lambda x: x.decision_result == False, left_condition_possibilities):
                        # left side is false, so add this to the possible compound condition results for false
                        # right side is ignoreds
                        condition_possibilities.append(left_condition_result)

                    return_data['condition_possibilities'] = condition_possibilities

                elif (ast_cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR and
                        ast_cursor.binary_operator == clang.cindex.BinaryOperator.LOr):
                    condition_possibilities = list()

                    for left_condition_result in filter(lambda x: x.decision_result == True, left_condition_possibilities):
                        # left side is true, so add this to the possible compound condition results for true
                        # right side is ignored
                        condition_possibilities.append(left_condition_result)

                    for left_condition_result in filter(lambda x: x.decision_result == False, left_condition_possibilities):
                        for right_condition_result in filter(lambda x: x.decision_result == True, right_condition_possibilities):
                            # right side is true, so add this to the possible compound condition results for true
                            condition_possibilities.append(
                                ConditionPossibility(True,
                                                     left_condition_result.condition_combination + right_condition_result.condition_combination))

                        for right_condition_result in filter(lambda x: x.decision_result == False, right_condition_possibilities):
                            # both sides are false, so add this to the possible compound condition results for false
                            condition_possibilities.append(
                                ConditionPossibility(False,
                                                     left_condition_result.condition_combination + right_condition_result.condition_combination))

                    return_data['condition_possibilities'] = condition_possibilities

            else:
                # This is a atomic condition. Create a EvaluationMarker and create new ConditionData
                evaluation_marker_id = self.cid_manager.get_new_id()
                evaluation_code_section = CodeSectionData(
                    CodePositionData(ast_cursor.extent.start.line,
                                     ast_cursor.extent.start.column),
                    CodePositionData(ast_cursor.extent.end.line, ast_cursor.extent.end.column))
                if self.config.evaluation_markers_enabled:
                    self.cid_manager.add_evaluation_marker(evaluation_marker_id, evaluation_code_section,
                                                           EvaluationType.CONDITION)
                condition = ConditionData(
                    evaluation_marker_id, evaluation_code_section)
                return_data['conditions'] = [condition]
                # create condition possibilities for MC/DC analysis
                return_data['condition_possibilities'] = [
                    ConditionPossibility(
                        True, [ConditionResult(evaluation_marker_id, True)]),
                    ConditionPossibility(
                        False, [ConditionResult(evaluation_marker_id, False)])]

    def _traverse_if_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Start analysis of if statement"""

        # Get branch results
        inner_traverse_args = dict(
            parent_function_id=args['parent_function_id'])
        inner_return_data = dict(branch_results=list())

        self._traverse_if_branch_result(
            ast_cursor, inner_traverse_args, inner_return_data)

        # Create correct code data info
        self.cid_manager.add_if_branch_data(self.cid_manager.get_new_id(), args['parent_function_id'],
                                            inner_return_data['branch_results'])

        # Check, if parent blocks should create new checkpoint marker id's
        if inner_return_data.get('new_parent_checkpoint_required', False):
            return_data['new_parent_checkpoint_required'] = True

    def _traverse_if_branch_result(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a if branch and analyze the according evaluation"""
        child_elements = ast_cursor.get_children()

        # Variables for storing information on the active branch_result
        evaluation_marker_id: int
        condition_possibilities = None
        conditions: List[ConditionData]
        result_evaluation_code_section: CodeSectionData
        result_body_code_section: CodeSectionData

        # variable that checks, if a new checkpoint marker id is required for the parent
        # status variable to check,
        return_data['new_parent_checkpoint_required'] = False
        # if a new checkpoint request shall be passed to the parent
        return_data['branch_results'] = list()  # initialize with empty list

        for i, child_element in enumerate(child_elements):
            # Check first element. This is the evaluation statement
            if i == 0 and self.config.evaluation_markers_enabled:
                evaluation_traverse_args = dict(is_condition=False)
                evaluation_return_data = dict()
                self._traverse_evaluation(
                    child_element, evaluation_traverse_args, evaluation_return_data)
                evaluation_marker_id = evaluation_return_data['evaluation_marker_id']
                conditions = evaluation_return_data['conditions']
                result_evaluation_code_section = evaluation_return_data['evaluation_code_section']
                condition_possibilities = evaluation_return_data['condition_possibilities']

            # Check second element. This is the compound statement of the if-branch
            if i == 1:
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()

                self._traverse_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

                if inner_return_data['new_parent_checkpoint_required']:
                    return_data['new_parent_checkpoint_required'] = True

                result_body_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

                # Create the IfBranchResult Data. Add id to list passed via args.
                if self.config.evaluation_markers_enabled:
                    return_data['branch_results'].append(BranchResultData(evaluation_marker_id, condition_possibilities,
                                                                          conditions, result_evaluation_code_section, result_body_code_section))

            # Check the existence of a third element.
            if i == 2:

                # Check the type of the third element.

                # If this is a IF_STMT, it's a if else branch. Check recursively
                if child_element.kind == clang.cindex.CursorKind.IF_STMT:
                    inner_traverse_args = dict(
                        parent_function_id=args['parent_function_id'])
                    inner_return_data = dict()

                    self._traverse_if_branch_result(
                        child_element, inner_traverse_args, inner_return_data)

                    if inner_return_data['new_parent_checkpoint_required']:
                        return_data['new_parent_checkpoint_required'] = True

                    return_data['branch_results'].extend(
                        inner_return_data['branch_results'])

                # If this is a COMPOUND_STMT, this is the else branch.
                elif child_element.kind == clang.cindex.CursorKind.COMPOUND_STMT:
                    # get code_section
                    else_code_section = CodeSectionData(
                        CodePositionData(
                            child_element.extent.start.line, child_element.extent.start.column),
                        CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

                    # create a branch result with evaluation_marker_id = -1
                    # (else get's detected by Analyzer)
                    return_data['branch_results'].append(BranchResultData(-1, list(), dict(true=[], false=[]),
                                                                          else_code_section,
                                                                          else_code_section))

                    # go into compound statement
                    inner_traverse_args = dict(
                        parent_function_id=args['parent_function_id'])
                    inner_return_data = dict()

                    self._traverse_compound_statement(child_element,
                                                      inner_traverse_args, inner_return_data)

    def _traverse_switch_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Start analysis of switch statement"""

        # Get all child elements
        child_elements = ast_cursor.get_children()

        switch_branch_code_section = CodeSectionData(
            CodePositionData(ast_cursor.extent.start.line,
                             ast_cursor.extent.start.column),
            CodePositionData(ast_cursor.extent.end.line, ast_cursor.extent.end.column))

        # Get switch branch cases
        inner_traverse_args = dict(
            parent_function_id=args['parent_function_id'])
        inner_return_data = dict(switch_cases=list())

        for i, child_element in enumerate(child_elements):
            # Get expression code section
            if i == 1:
                self._traverse_switch_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

        # Create correct code data info
        self.cid_manager.add_switch_branch_data(self.cid_manager.get_new_id(), args['parent_function_id'],
                                                switch_branch_code_section, inner_return_data['switch_cases'])

        # Check, if parent blocks should create new checkpoint marker id's
        if inner_return_data.get('new_parent_checkpoint_required', False):
            return_data['new_parent_checkpoint_required'] = True
        return

    def _traverse_switch_compound_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """traverse the compound statement of a switch statement in order to prevent cluttering
           the normal compound statement traversing function.
        """

        for child_element in ast_cursor.get_children():
            if child_element.kind == clang.cindex.CursorKind.CASE_STMT:
                # this is a normal case. Check if it includes another case (2nd child is CASE_STMT or DEFAULT_STMT),
                # so that we go into this case recursively
                # until we have a clean compound statement for further traversing

                case_evaluation_code_section: CodeSectionData
                case_body_code_section: CodeSectionData

                for i, case_child in enumerate(child_element.get_children()):
                    if i == 0:
                        case_evaluation_code_section = CodeSectionData(
                            CodePositionData(
                                child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(case_child.extent.end.line, case_child.extent.end.column))
                    elif (i == 1 and case_child.kind == clang.cindex.CursorKind.CASE_STMT or
                            i == 1 and case_child.kind == clang.cindex.CursorKind.DEFAULT_STMT):
                        # this is a direct case concatenation, so call this function recursively
                        inner_traverse_args = dict(
                            parent_function_id=args['parent_function_id'])
                        inner_return_data = dict(switch_cases=list())

                        # traverse inner case statement
                        self._traverse_switch_compound_statement(
                            child_element, inner_traverse_args, inner_return_data)

                        # append inner results to the cases in this function
                        return_data['switch_cases'].extend(
                            inner_return_data['switch_cases'])

                        if inner_return_data.get('new_parent_checkpoint_required', False):
                            return_data['new_parent_checkpoint_required'] = True

                        # take inner code section from first item in return data, since it's the same for nested cases
                        case = CaseData(inner_return_data['switch_cases'][0].checkpoint_marker_id, CaseType.CASE,
                                        case_evaluation_code_section, inner_return_data['switch_cases'][0].body_code_section)
                        return_data['switch_cases'].append(case)
                    elif (i == 1):
                        # this is a atomic case, so traverse with compound statement handler
                        inner_traverse_args = dict(
                            is_case=True,
                            parent_function_id=args['parent_function_id']
                        )
                        inner_return_data = dict()

                        self._traverse_compound_statement(
                            child_element, inner_traverse_args, inner_return_data)

                        if inner_return_data.get('new_parent_checkpoint_required', False):
                            return_data['new_parent_checkpoint_required'] = True

                        # create code section for the case
                        case_body_code_section = CodeSectionData(
                            CodePositionData(
                                case_child.extent.start.line, case_child.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

                        case = CaseData(inner_return_data['first_checkpoint_marker_id'], CaseType.CASE,
                                        case_evaluation_code_section, case_body_code_section)

                        return_data['switch_cases'].append(case)

            elif child_element.kind == clang.cindex.CursorKind.DEFAULT_STMT:
                # this is a default case. Check if it includes another case (1st child is CASE_STMT or DEFAULT_STMT),
                # so that we go into this case recursively
                # until we have a clean compound statement for further traversing
                case_body_code_section: CodeSectionData
                case_evaluation_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.start.line, child_element.extent.start.column + 7))

                for i, case_child in enumerate(child_element.get_children()):
                    if (i == 0 and case_child.kind == clang.cindex.CursorKind.CASE_STMT or
                            i == 0 and case_child.kind == clang.cindex.CursorKind.DEFAULT_STMT):
                        # this is a direct case concatenation, so call this function recursively
                        inner_traverse_args = dict(
                            parent_function_id=args['parent_function_id'])
                        inner_return_data = dict(switch_cases=list())

                        # traverse inner case statement
                        self._traverse_switch_compound_statement(
                            child_element, inner_traverse_args, inner_return_data)

                        # append inner results to the cases in this function
                        return_data['switch_cases'].extend(
                            inner_return_data['switch_cases'])

                        if inner_return_data.get('new_parent_checkpoint_required', False):
                            return_data['new_parent_checkpoint_required'] = True

                        # take inner code section from first item in return data, since it's the same for nested cases
                        case = CaseData(inner_return_data['switch_cases'][0].checkpoint_marker_id, CaseType.DEFAULT,
                                        case_evaluation_code_section, inner_return_data['switch_cases'][0].body_code_section)
                        return_data['switch_cases'].append(case)
                    elif (i == 0):
                        # this is a atomic case, so traverse with compound statement handler
                        inner_traverse_args = dict(
                            is_case=True,
                            parent_function_id=args['parent_function_id']
                        )
                        inner_return_data = dict()

                        self._traverse_compound_statement(
                            child_element, inner_traverse_args, inner_return_data)

                        if inner_return_data.get('new_parent_checkpoint_required', False):
                            return_data['new_parent_checkpoint_required'] = True

                        # create code section for the case
                        case_body_code_section = CodeSectionData(
                            CodePositionData(
                                case_child.extent.start.line, case_child.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

                        case = CaseData(inner_return_data['first_checkpoint_marker_id'], CaseType.DEFAULT,
                                        case_evaluation_code_section, case_body_code_section)

                        return_data['switch_cases'].append(case)
        return

    def _search_for_ternary(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverses a given node until every child is covered.
           If one child is a ternary statement, it get's checked.
           We're doing this, since ternary operations often are inside other nodes in the AST.
        """
        for child_element in ast_cursor.get_children():
            inner_traverse_args = args
            inner_return_data = return_data

            if child_element.kind == clang.cindex.CursorKind.CONDITIONAL_OPERATOR:
                self._traverse_ternary_statement(
                    child_element, inner_traverse_args, inner_return_data)
            else:
                self._search_for_ternary(
                    child_element, inner_traverse_args, inner_return_data)

    def _traverse_ternary_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a ternary statement and analyze the including evaluation"""
        # variables for storing information on the ternary expression
        evaluation_marker_id: int
        condition_possibilities = None
        conditions: list()
        evaluation_code_section: None
        true_code_section: None
        false_code_section: None

        # traverse through all three child elements
        for i, child_element in enumerate(ast_cursor.get_children()):
            if i == 0 and self.config.evaluation_markers_enabled:
                # this is the evaluation, so get all informations out of it
                inner_traverse_args = dict(
                    parent_function_id=args["parent_function_id"])
                inner_return_data = dict()
                self._traverse_evaluation(
                    child_element, inner_traverse_args, inner_return_data)
                evaluation_marker_id = inner_return_data['evaluation_marker_id']
                conditions = inner_return_data['conditions']
                evaluation_code_section = inner_return_data['evaluation_code_section']
                condition_possibilities = inner_return_data['condition_possibilities']

            elif i == 1:
                # this is the "true" branch. Get the size of it and then invoke compound statement analysis
                true_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line,
                                     child_element.extent.end.column)
                )

            elif i == 2:
                # this is the "false" branch. Get the size of it and then invoke compound statement analysis
                false_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line,
                                     child_element.extent.end.column)
                )

        self.cid_manager.add_ternary_expression_data(self.cid_manager.get_new_id(), args["parent_function_id"],
                                                     evaluation_marker_id, evaluation_code_section, condition_possibilities, conditions,
                                                     true_code_section, false_code_section)

        return

    def _traverse_for_loop(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a for loop"""

        # variables for storing evaluation and inner code data
        evaluation_marker_id: int
        condition_possibilities = None
        conditions = None
        evaluation_code_section = None
        body_code_section = None

        for i, child_element in enumerate(ast_cursor.get_children()):
            if i == 1 and self.config.evaluation_markers_enabled:
                # this is the evaluation, so get all informations out of it
                inner_traverse_args = dict(
                    parent_function_id=args["parent_function_id"])
                inner_return_data = dict()
                self._traverse_evaluation(
                    child_element, inner_traverse_args, inner_return_data)
                evaluation_marker_id = inner_return_data['evaluation_marker_id']
                conditions = inner_return_data['conditions']
                evaluation_code_section = inner_return_data['evaluation_code_section']
                condition_possibilities = inner_return_data['condition_possibilities']

            if i == 3:
                # this is the inner compound statement
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()

                self._traverse_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

                if inner_return_data['new_parent_checkpoint_required']:
                    return_data['new_parent_checkpoint_required'] = True

                # set body code section
                body_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

        self.cid_manager.add_loop_data(self.cid_manager.get_new_id(), LoopType.FOR, args["parent_function_id"],
                                       evaluation_marker_id, evaluation_code_section, body_code_section, condition_possibilities, conditions)

    def _traverse_while_loop(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a while loop"""

        # variables for storing evaluation and inner code data
        evaluation_marker_id: int
        condition_possibilities = None
        conditions = None
        evaluation_code_section = None
        body_code_section = None

        for i, child_element in enumerate(ast_cursor.get_children()):
            if i == 0 and self.config.evaluation_markers_enabled:
                # this is the evaluation, so get all informations out of it
                inner_traverse_args = dict(
                    parent_function_id=args["parent_function_id"])
                inner_return_data = dict()
                self._traverse_evaluation(
                    child_element, inner_traverse_args, inner_return_data)
                evaluation_marker_id = inner_return_data['evaluation_marker_id']
                conditions = inner_return_data['conditions']
                evaluation_code_section = inner_return_data['evaluation_code_section']
                condition_possibilities = inner_return_data['condition_possibilities']

            if i == 1:
                # this is the inner compound statement
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()

                self._traverse_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

                if inner_return_data['new_parent_checkpoint_required']:
                    return_data['new_parent_checkpoint_required'] = True

                # set body code section
                body_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

        self.cid_manager.add_loop_data(self.cid_manager.get_new_id(), LoopType.WHILE, args["parent_function_id"],
                                       evaluation_marker_id, evaluation_code_section, body_code_section, condition_possibilities, conditions)

    def _traverse_do_while_loop(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Traverse a do-while loop"""

        # variables for storing evaluation and inner code data
        evaluation_marker_id: int
        condition_possibilities = None
        conditions = None
        evaluation_code_section = None
        body_code_section = None

        for i, child_element in enumerate(ast_cursor.get_children()):
            if i == 0:
                # this is the inner compound statement
                inner_traverse_args = dict(
                    parent_function_id=args['parent_function_id'])
                inner_return_data = dict()

                self._traverse_compound_statement(
                    child_element, inner_traverse_args, inner_return_data)

                if inner_return_data['new_parent_checkpoint_required']:
                    return_data['new_parent_checkpoint_required'] = True

                # set body code section
                body_code_section = CodeSectionData(
                    CodePositionData(child_element.extent.start.line,
                                     child_element.extent.start.column),
                    CodePositionData(child_element.extent.end.line, child_element.extent.end.column))

            if i == 1 and self.config.evaluation_markers_enabled:
                # this is the evaluation, so get all informations out of it
                inner_traverse_args = dict(
                    parent_function_id=args["parent_function_id"])
                inner_return_data = dict()
                self._traverse_evaluation(
                    child_element, inner_traverse_args, inner_return_data)
                evaluation_marker_id = inner_return_data['evaluation_marker_id']
                conditions = inner_return_data['conditions']
                evaluation_code_section = inner_return_data['evaluation_code_section']
                condition_possibilities = inner_return_data['condition_possibilities']

        self.cid_manager.add_loop_data(self.cid_manager.get_new_id(), LoopType.DOWHILE, args["parent_function_id"],
                                       evaluation_marker_id, evaluation_code_section, body_code_section, condition_possibilities, conditions)
    # !SECTION

    # SECTION   Parser public functions
    def start_parser(self):
        self._traverse_root(self.clang_ast)
        return

    # !SECTION
# !SECTION
