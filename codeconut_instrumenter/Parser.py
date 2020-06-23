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

import clang.cindex

from DataTypes import *

from Configuration import Configuration
from CIDManager import CIDManager


# SECTION   ClangBridge class
class ClangBridge:
    """ClangBridge class.
       Connects libclang to Codeconut Instrumenter by
       returning the Clang AST of a input file
    """
    
    # SECTION   ClangBridge private attribute definitions
    # !SECTION
    
    # SECTION   ClangBridge public attribute definitions
    # !SECTION
    
    # SECTION   ClangBridge initialization
    def __init__(self):
        clang.cindex.Config.set_library_path("C:\\Program Files\\LLVM\\bin")
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
            location_file = location_file.replace('\\\\', '/').replace('\\', '/').split('/')[-1]

            if location_file != self.cid_manager.source_file.input_filename.split('/')[-1]:
                # Child is not in the correct file, so we can ignore it
                continue

            kind: clang.cindex.CursorKind = root_child.kind
            if kind == clang.cindex.CursorKind.FUNCTION_DECL:
                self._traverse_function(root_child, dict(parent_function_id = -1))
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
            CodePositionData(ast_cursor.extent.start.line, ast_cursor.extent.start.column),
            None
        )

        inner_code_section: CodeSectionData = None

        inner_traverse_args = dict(
            is_case = False,
            parent_function_id = function_id
        )

        return_data = dict()

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
                    CodePositionData(function_child.extent.start.line, function_child.extent.start.column),
                    CodePositionData(function_child.extent.end.line, function_child.extent.end.column)
                )

                # call analysis of function internals
                self._traverse_compound_statement(function_child, inner_traverse_args, return_data)

                

        print("Header start line: " + str(header_code_section.start_position.line))
        print("Header start column: " + str(header_code_section.start_position.column))
        print("Header end line: " + str(header_code_section.end_position.line))
        print("Header end column: " + str(header_code_section.end_position.column))

        print("Inner start line: " + str(inner_code_section.start_position.line))
        print("Inner start column: " + str(inner_code_section.start_position.column))
        print("Inner end line: " + str(inner_code_section.end_position.line))
        print("Inner end column: " + str(inner_code_section.end_position.column))

        self.cid_manager.add_function_data(function_id, function_name, function_type, parent_function_id,
                return_data.get('first_checkpoint_marker_id'), header_code_section, inner_code_section)
        return

    def _traverse_compound_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        """Parses a compound statement given to it"""
        # use given checkpoint_marker_id if passed (i.e. CompoundStmt in CompoundStmt)
        active_checkpoint_marker_id = args.get('start_checkpoint_marker_id', self.cid_manager.get_new_id())
        return_data['first_checkpoint_marker_id'] = active_checkpoint_marker_id
        first_checkpoint_set = False # status variable to check, if the first checkpoint was set
        return_data['new_parent_checkpoint_required'] = False # status variable to check,
                                               # if a new checkpoint request shall be passed to the parent
        new_checkpoint_required = False # status variable to check, if a new checkpoint is neccessary

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
            # If yes, we should just skip it, since it's not useful for us.
            if child_kind == clang.cindex.CursorKind.LABEL_STMT:
                continue

            # check, if the first checkpoint wasn't set. If no, set it up.
            # Inject at start of current element.
            if not first_checkpoint_set:
                self.cid_manager.add_checkpoint_marker(active_checkpoint_marker_id,
                        CodePositionData(child_element.extent.start.line, child_element.extent.start.column))
                first_checkpoint_set = True
            
            # check, if a new checkpoint is required since the last child element
            if new_checkpoint_required:
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
                        StatementType.RETURN, args.get('parent_function_id'), active_checkpoint_marker_id,
                        CodeSectionData(
                            CodePositionData(child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                        )
            elif child_kind == clang.cindex.CursorKind.BREAK_STMT:
                # same a with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                        StatementType.BREAK, args.get('parent_function_id'), active_checkpoint_marker_id,
                        CodeSectionData(
                            CodePositionData(child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                        )
            elif child_kind == clang.cindex.CursorKind.CONTINUE_STMT:
                # same as with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                        StatementType.CONTINUE, args.get('parent_function_id'), active_checkpoint_marker_id,
                        CodeSectionData(
                            CodePositionData(child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                        )
            elif (child_kind == clang.cindex.CursorKind.GOTO_STMT or
                    child_kind == clang.cindex.CursorKind.INDIRECT_GOTO_STMT):
                # same as with return statement
                new_checkpoint_required = True
                return_data['new_parent_checkpoint_required'] = True

                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                        StatementType.GOTO, args.get('parent_function_id'), active_checkpoint_marker_id,
                        CodeSectionData(
                            CodePositionData(child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                        )
            elif child_kind == clang.cindex.CursorKind.COMPOUND_STMT:
                # found a compound statement, so do a recursive call
                inner_traverse_args = dict(
                    is_case = False,
                    parent_function_id = args.get('parent_function_id'),
                    start_checkpoint_marker_id = active_checkpoint_marker_id
                )
                inner_return_data = dict()
                self._traverse_compound_statement(child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is neccessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required']= True

            elif child_kind == clang.cindex.CursorKind.IF_STMT:
                # found a if_branch, so open the if statement handler
                inner_traverse_args = dict(parent_function_id = args.get('parent_function_id'))
                inner_return_data = dict()
                self._traverse_if_statement(child_element, inner_traverse_args, inner_return_data)

                # check, if new checkpoint marker is neccessary
                if inner_return_data.get('new_parent_checkpoint_required', True):
                    new_checkpoint_required = True
                    return_data['new_parent_checkpoint_required']= True
            else:
                # add the statement to the code data
                self.cid_manager.add_statement_data(self.cid_manager.get_new_id(),
                        StatementType.NORMAL, args.get('parent_function_id'), active_checkpoint_marker_id,
                        CodeSectionData(
                            CodePositionData(child_element.extent.start.line, child_element.extent.start.column),
                            CodePositionData(child_element.extent.end.line, child_element.extent.end.column))
                        )
        print("Traversed compound statement")

    def _traverse_evaluation(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        # Traverse a evaluation and return a list of conditions with evaluation_marker_ids and code_sections
        
        # Check, if we are in a compound condition
        print(ast_cursor.)
        if ast_cursor.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
            print("For now, I do nothing")

    def _traverse_if_statement(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        # Starting analysis of if statement

        # Get branch results
        inner_traverse_args = dict()
        inner_return_data = dict(branch_results = list())

        self._traverse_if_branch_result(ast_cursor, inner_traverse_args, inner_return_data)

        # Create correct code data info
        self.cid_manager.add_if_branch_data(self.cid_manager.get_new_id(), args.get('parent_function_id'),
                inner_return_data.get('branch_results'))
        
        # Check, if parent blocks should create new checkpoint marker id's
        if inner_return_data.get('new_parent_checkpoint_required', False):
            return_data['new_parent_checkpoint_required'] = True

    def _traverse_if_branch_result(self, ast_cursor: clang.cindex.Cursor, args: dict, return_data: dict):
        # Traverse If Branch
        child_elements = ast_cursor.get_children()

        for i, child_element in enumerate(child_elements):
            # Check first element. This is the evaluation statement
            if i == 0 and self.config.evaluation_markers_enabled:
                evaluation_traverse_args = dict()
                evaluation_return_data = dict(conditions = list())
                self._traverse_evaluation(child_element, evaluation_traverse_args, evaluation_return_data)

            # Check second element. This is the compound statement of the if-branch

            # Create the IfBRanchResult Data. Add id to list passed via args.

            # Check the existence of a third element.

                # Check the type of the third element.

                    # If this is a IF_STMT, it's a if else branch. Check recursively

                    # If this is a COMPOUND_STMT, this is the else branch.


    # !SECTION
    
    # SECTION   Parser public functions
    def start_parser(self):
        self._traverse_root(self.clang_ast)
        return

    # !SECTION
# !SECTION