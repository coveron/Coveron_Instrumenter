#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Package main for Codeconut Instrumenter.
"""

import sys
import os
import subprocess
import colorama
colorama.init()
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


from ClangBridge import ClangBridge
from Parser import Parser
from CIDManager import CIDManager
from Configuration import Configuration

from ArgumentHandler import ArgumentHandler
from Instrumenter import Instrumenter

from DataTypes import SourceFile, SourceCode


def main():
    # load configuration
    config = Configuration()

    # load arguments
    ArgumentHandler(config)

    # write title and config, if verbose
    if config.verbose:
        print_title()
        config.print_config()

    # instantiate clang bridge
    clang_bridge = ClangBridge()

    # create new instrumentation process for every source file detected by ArgumentHandler
    for source_file in config.source_files:
        if config.verbose:
            print("Instrumenting "+source_file.input_filename+" ...")
        
        # load the source file
        sourcecode: SourceCode = ""
        if os.path.isfile(source_file.input_filename):
            with open(source_file.input_filename, 'r') as sourcefile:
                try:
                    sourcecode = sourcefile.read()
                except:
                    print(colorama.Fore.RED + "Codeconut fatal error: " + colorama.Fore.RESET + source_file.input_filename + " can't be accessed!")
        else:
            print(colorama.Fore.RED + "Codeconut fatal error: " + colorama.Fore.RESET + source_file.input_filename + " not found!")
            exit(1)

        # create a cid_manager
        cid_manager = CIDManager(config, source_file, sourcecode)

        # create a clang bridge and get a clang AST from the source file
        clang_tree = clang_bridge.clang_parse(source_file.input_filename, config.clang_args)
        
        # create a parser instance, pass the clang AST
        parser = Parser(config, clang_tree)

        # write cid data
        cid_manager.write_output_file()

        # write instrumented source code file
        instrumenter = Instrumenter(source_file.output_filename, cid_manager, sourcecode)

        # delete cid_manager, parser and instrumenter instances
        del cid_manager
        del parser
        del instrumenter
        continue

    # delete clang bridge after running through every file
    del clang_bridge

    # call the compiler with the pass thru arguments, the new instrumented files and the link to the runtime_helper (as absolute path)
    command_string = " ".join([config.compiler_exec, config.compiler_args, ' '.join(source_file.output_filename for source_file in config.source_files)])
    compiler_returncode = subprocess.call(command_string, shell=True)

    if config.verbose:
        if compiler_returncode is not 0:
            print(colorama.Fore.RED + "Compiler failed!" + colorama.Fore.RESET)
        else:
            print(colorama.Fore.GREEN + "Compiled succeeded!" + colorama.Fore.RESET)

    # load inputfile and create sourcecode variable
    #sourcecode = ""
    #with open(config.input_filename, 'r') as sourcefile:
        #sourcecode = sourcefile.read()

    #cid_manager = CIDManager(config, sourcecode)

    #clang_bridge = ClangBridge()
    #clang_bridge.clang_parse(config.input_filename)

    #parser = Parser(config, cid_manager, sourcecode)
    # parser.start_parser()
    return

def print_title():
    # Write title to output
    print(colorama.Fore.CYAN + "Codeconut Instrumenter" + colorama.Fore.RESET)
    print("======================")

def get_absolute_runtime_helper_path():
    print("Not implemented yet")
    return


if __name__ == "__main__":
    main()
