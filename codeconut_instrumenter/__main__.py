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
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


#from ClangBridge import ClangBridge
#from Parser import Parser
#from CIDManager import CIDManager
from Configuration import Configuration

from ArgumentHandler import ArgumentHandler
# from Instrumenter import Instrumenter


def main():
    # load configuration
    config = Configuration()

    # load arguments
    arguments = ArgumentHandler(config)

    # create new instrumentation process for every source file detected by ArgumentHandler
    for source_file in config.source_files:
        # load the source file

        # create a cid_manager

        # create a parser instance

        # write cid data

        # write instrumented source code file

        # delete cid_manager, parser and instrumenter instances
        break

    # call the compiler with the pass thru arguments, the new instrumented files and the link to the runtime_helper (as absolute path)

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

def get_absolute_runtime_helper_path(self):
    print("Not implemented yet")
    return


if __name__ == "__main__":
    main()
