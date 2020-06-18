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


from Parser import ClangBridge, Parser
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

        # load source code
        source_code: SourceCode = ""
        if os.path.isfile(source_file.input_filename):
            with open(source_file.input_filename, 'r') as source_file_ptr:
                try:
                    source_code = source_file_ptr.read()
                except:
                    raise(RuntimeError(source_file.input_filename + " can't be accessed!"))
        else:
            raise(RuntimeError(self.source_file.input_filename + " not found!"))

        # create a cid_manager
        cid_manager = CIDManager(config, source_file, source_code)

        # create a clang bridge and get a clang AST from the source file
        clang_tree = clang_bridge.clang_parse(source_file.input_filename, config.clang_args)
        
        # create a parser instance, pass the clang AST. Start the parser
        parser = Parser(config, cid_manager, clang_tree)
        parser.start_parser()

        # write cid data
        cid_manager.write_cid_file()

        # create a instrumenter instance
        instrumenter = Instrumenter(config, cid_manager, source_file, source_code)

        # create the instrumented source code and write the instrumened source file
        instrumenter.start_instrumentation()
        instrumenter.write_output_file()

        # delete cid_manager, parser and instrumenter instances
        del cid_manager
        del parser
        del instrumenter
        continue

    # delete clang bridge after running through every file
    del clang_bridge

    # call the compiler with the pass thru arguments, the new instrumented files and the link to the runtime_helper (as absolute path)
    # command_string = " ".join([config.compiler_exec, config.compiler_args, ' '.join(source_file.output_filename for source_file in config.source_files)])
    # compiler_returncode = subprocess.call(command_string, shell=True)

    #if config.verbose:
        #if compiler_returncode is not 0:
        #    print(colorama.Fore.RED + "Compiler failed!" + colorama.Fore.RESET)
        #else:
        #    print(colorama.Fore.GREEN + "Compiled succeeded!" + colorama.Fore.RESET)
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
