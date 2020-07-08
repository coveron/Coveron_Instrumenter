#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Unit Tests for the Configuration module.
"""

from unittest.mock import Mock, patch

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.Configuration import Configuration


def test_Configuration_Init(tmpdir):
    config = Configuration()

    # check, if the current absolute output path is the current working directory
    assert isinstance(config, Configuration) == True
    assert config.output_abs_path == os.path.abspath(os.getcwd())


def test_Configuration_CompilerArgs():
    config = Configuration()

    # enable checkpoint and evaluation markers
    config.evaluation_markers_enabled = True
    config.checkpoint_markers_enabled = True

    # add compiler args
    config.compiler_args = "-arg1 -arg2 --arg3 hello"

    # check all compiler args to see, if defines were added
    assert config.compiler_args == "-arg1 -arg2 --arg3 hello -D___COVERON_CHECKPOINT_ANALYSIS_ENABLED -D___COVERON_EVALUATION_ANALYSIS_ENABLED"
