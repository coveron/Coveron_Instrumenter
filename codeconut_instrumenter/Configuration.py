#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Configuration for Codeconut Instrumenter.
   Contains the configuration for all modules.
"""


class Configuration:
    """Configuration class.
       Stores all configuration values for the instrumenter.
    """

    __slots__ = ["statement_analysis_enabled",
                 "decision_analysis_enabled", "condition_analysis_enabled"]

    statement_analysis_enabled: bool
    decision_analysis_enabled: bool
    condition_analysis_enabled: bool

    def __init__(self):
        """Initializes the ConditionParser"""

        # TODO implement default values
        return
