#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""ArgumentHandler for Codeconut Instrumenter.
   Parses the arguments given via command-line options.
"""

from .Configuration import Configuration

import argparse


class ArgumentHandler:
    """ArgumentHandler class.
       Parses the command line option and sets the correlating variables inside the Configuration module
    """

    __slots__ = ['_config']

    _config: Configuration

    def __init__(self, config):
        """Initializes the new ArgumentHandler"""

        # Load configuration
        self._config = config

        return

    def check_arguments(self):
        """Checks the passed arguments and sets them in the passed configuration module"""

        # TODO implement value checking
        return
