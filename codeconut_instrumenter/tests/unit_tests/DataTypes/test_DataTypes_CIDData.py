#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Codeconut project
#
# The Codeconut project is licensed under the LGPL-3.0 license

"""Unit Tests for the CID-Manager module.
"""

import sys
import os

import pytest
from unittest.mock import Mock, patch

from codeconut_instrumenter.DataTypes import CIDData, CodeSectionData, MarkerTypeEnum, MarkerData


@pytest.fixture
def cid_data_success():
    return CIDData(source_code_filename="test",
                   source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                   instrumentation_random="hqz9lEMJE6NYqI7p",
                   statement_markers_enabled=True,
                   decision_markers_enabled=True,
                   condition_markers_enabled=True)


def test_CIDData_badType_souce_code_filename():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename=0,
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_undefined_souce_code_filename():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badType_souce_code_hash():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash=123,
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_undefined_souce_code_hash():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badLength_souce_code_hash():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="hqz9lE",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badChars_souce_code_hash():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="g0e686258f0694fa5463d133bc408688078d96bgb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badType_instrumentation_random():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random=123,
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_undefined_instrumentation_random():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badLength_instrumentation_random():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="abc",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badChars_instrumentation_random():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE/NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badType_statement_markers_enabled():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=1,
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_undefined_statement_markers_enabled():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           decision_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badType_decision_markers_enabled():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=1,
                           condition_markers_enabled=True)


def test_CIDData_undefined_decision_markers_enabled():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           condition_markers_enabled=True)


def test_CIDData_badType_condition_markers_enabled():
    with pytest.raises(TypeError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True,
                           condition_markers_enabled=1)


def test_CIDData_undefined_condition_markers_enabled():
    with pytest.raises(ValueError):
        cid_data = CIDData(source_code_filename="test",
                           source_code_hash="e0e686258f0694fa5463d133bc408688078d96bdb3319d8c31d42a2e7e639e0f",
                           instrumentation_random="hqz9lEMJE6NYqI7p",
                           statement_markers_enabled=True,
                           decision_markers_enabled=True)


def test_CIDData_add_marker_data_undefined(cid_data_success):
    with pytest.raises(ValueError):
        cid_data_success.add_marker_data(None)


def test_CIDData_add_marker_data_badType(cid_data_success):
    with pytest.raises(TypeError):
        cid_data_success.add_marker_data(123)


def test_CIDData_add_marker_data_double(cid_data_success):
    new_marker = MarkerData(marker_id=1,
                            marker_type=MarkerTypeEnum.STATEMENT,
                            code_section_data=[CodeSectionData(start_line=1,
                                                               start_column=1,
                                                               end_line=2,
                                                               end_column=5)])
    cid_data_success.add_marker_data(new_marker)
    with pytest.raises(ValueError):
        # expect error, because the item already exists
        cid_data_success.add_marker_data(new_marker)


def test_CIDData_update_marker_data_success(cid_data_success):
    first_marker = MarkerData(marker_id=1,
                              marker_type=MarkerTypeEnum.STATEMENT,
                              code_section_data=[CodeSectionData(start_line=1,
                                                                 start_column=1,
                                                                 end_line=2,
                                                                 end_column=5)])
    second_marker = MarkerData(marker_id=1,
                               marker_type=MarkerTypeEnum.STATEMENT,
                               code_section_data=[CodeSectionData(start_line=1,
                                                                  start_column=1,
                                                                  end_line=3,
                                                                  end_column=5)])

    cid_data_success.add_marker_data(first_marker)

    cid_data_success.update_marker_data(first_marker, second_marker)


def test_CIDData_update_marker_data_badType(cid_data_success):
    first_marker = MarkerData(marker_id=1,
                              marker_type=MarkerTypeEnum.STATEMENT,
                              code_section_data=[CodeSectionData(start_line=1,
                                                                 start_column=1,
                                                                 end_line=2,
                                                                 end_column=5)])
    second_marker = 12345
    cid_data_success.add_marker_data(first_marker)

    with pytest.raises(TypeError):
        cid_data_success.update_marker_data(first_marker, second_marker)


def test_CIDData_update_marker_data_notExisting(cid_data_success):
    first_marker = MarkerData(marker_id=1,
                              marker_type=MarkerTypeEnum.STATEMENT,
                              code_section_data=[CodeSectionData(start_line=1,
                                                                 start_column=1,
                                                                 end_line=2,
                                                                 end_column=5)])
    second_marker = MarkerData(marker_id=1,
                               marker_type=MarkerTypeEnum.STATEMENT,
                               code_section_data=[CodeSectionData(start_line=1,
                                                                  start_column=1,
                                                                  end_line=3,
                                                                  end_column=5)])

    with pytest.raises(ValueError):
        cid_data_success.update_marker_data(first_marker, second_marker)
