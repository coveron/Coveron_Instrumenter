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

from .Configuration import Configuration
# from .ArgumentHandler import ArgumentHandler
from .CIDManager import CIDManager
# from .Instrumenter import Instrumenter
from .Parser import Parser


def main():
    config = Configuration()
    cid_manager = CIDManager(config, 'test_filename.c', 'test_code')

    parser = Parser(config, cid_manager, "")
    parser.start_parser()
    return


if __name__ == "__main__":
    main()
