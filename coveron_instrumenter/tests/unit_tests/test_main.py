#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Unit Tests for the main function.
"""

from unittest.mock import Mock, patch

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.Parser import ClangBridge, Parser
from coveron_instrumenter.CIDManager import CIDManager
from coveron_instrumenter.Configuration import Configuration
from coveron_instrumenter.ArgumentHandler import ArgumentHandler
from coveron_instrumenter.Instrumenter import Instrumenter
import coveron_instrumenter.__main__ as main_func

# To be done
