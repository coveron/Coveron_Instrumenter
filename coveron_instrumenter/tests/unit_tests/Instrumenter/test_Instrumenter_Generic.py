#!/usr/bin/env python
# -*- coding: utf-8 -*
#
# Copyright 2020 Glenn Töws
#
# This file is part of the Coveron project
#
# The Coveron project is licensed under the LGPL-3.0 license

"""Unit Tests for the Instrumenter module.
"""

from unittest.mock import Mock, patch
import pytest
import json
import jsonschema
import gzip

from coveron_instrumenter.DataTypes import *

from coveron_instrumenter.Instrumenter import Instrumenter, InstrumenterMarker, InstrumenterMarkerType
from coveron_instrumenter.Configuration import Configuration, SourceFile
from coveron_instrumenter.CIDManager import CIDManager

dummySourceCode: SourceCode = "int main() {\n    test0;\n    test1;\n    test2;\n}"


@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Instrumenter_init(mock_config, mock_cid_manager, tmpdir):

    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True
    mock_config.output_abs_path = tmpdir
    source_file = SourceFile('test_file.c')

    instrumenter = Instrumenter(
        mock_config, mock_cid_manager, source_file, dummySourceCode)

    assert isinstance(instrumenter, Instrumenter) == True


@patch('coveron_instrumenter.CIDManager.CIDManager.get_source_code_hash')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_instrumentation_random')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_evaluation_markers')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_checkpoint_markers')
@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Instrumenter_writeMarkers(mock_config,
                                   mock_cid_manager,
                                   mock_cp_markers,
                                   mock_ev_markers,
                                   mock_ir,
                                   mock_sc_h,
                                   tmpdir):

    mock_config.runtime_helper_header_path = "C:\\testpath\\coveron_helper.h"
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True
    mock_config.output_abs_path = tmpdir
    source_file = SourceFile(os.path.join(tmpdir, 'test_file.c'))

    instrumenter = Instrumenter(
        mock_config, mock_cid_manager, source_file, dummySourceCode)

    # create dummy instrumentation random (in lower_case, to check if transform to uppercase works)
    mock_ir.return_value = "abcdefghijklmnopqrstuvwxyz123456"

    # create dummy source code hash
    mock_sc_h.return_value = "abcdefghijklmnopqrstuvwxyz123456abcdefghijklmnopqrstuvwxyz234567"

    # create dummy markers for return
    mock_cp_markers.return_value = [
        CheckpointMarkerData(1, CodePositionData(2, 5))]
    mock_ev_markers.return_value = [
        EvaluationMarkerData(2, EvaluationType.DECISION, CodeSectionData(
            CodePositionData(3, 5), CodePositionData(3, 10))),
        EvaluationMarkerData(3, EvaluationType.CONDITION, CodeSectionData(CodePositionData(4, 5), CodePositionData(4, 10)))]

    # start instrumentation with marker
    instrumenter.start_instrumentation()

    # write output file
    instrumenter.write_output_file()

    # open output file and compare with reference string
    with open(tmpdir.join('test_file.instr.c'), 'r') as output_source_code_ptr:
        source_code_instr_string = output_source_code_ptr.read()

    print(source_code_instr_string)

    source_code_instr_ref_str = '''#include "C:\\testpath\\coveron_helper.h"
___COVERON_FILE_T ___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456 = {
{0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x12, 0x34, 0x56, 0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x23, 0x45, 0x67},
{0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x12, 0x34, 0x56},
___COVERON_BOOL_FALSE,
NULL,
 "test_file.cri"};

int main() {
    ___COVERON_SET_CHECKPOINT_MARKER(0x00, 0x00, 0x00, 0x01, &___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456);test0;
    ___COVERON_SET_EVALUATION_MARKER(0x00, 0x00, 0x00, 0x02, &___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456, test1);
    ___COVERON_SET_EVALUATION_MARKER(0x00, 0x00, 0x00, 0x03, &___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456, test2);
}'''

    assert source_code_instr_string == source_code_instr_ref_str


@patch('coveron_instrumenter.CIDManager.CIDManager.get_source_code_hash')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_instrumentation_random')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_evaluation_markers')
@patch('coveron_instrumenter.CIDManager.CIDManager.get_checkpoint_markers')
@patch('coveron_instrumenter.CIDManager.CIDManager')
@patch('coveron_instrumenter.Configuration.Configuration')
def test_Instrumenter_writeNestedEvalMarkers(mock_config,
                                             mock_cid_manager,
                                             mock_cp_markers,
                                             mock_ev_markers,
                                             mock_ir,
                                             mock_sc_h,
                                             tmpdir):

    mock_config.runtime_helper_header_path = "C:\\testpath\\coveron_helper.h"
    mock_config.checkpoint_markers_enabled = True
    mock_config.evaluation_markers_enabled = True
    mock_config.output_abs_path = tmpdir
    source_file = SourceFile(os.path.join(tmpdir, 'test_file.c'))

    instrumenter = Instrumenter(
        mock_config, mock_cid_manager, source_file, dummySourceCode)

    # create dummy instrumentation random (in lower_case, to check if transform to uppercase works)
    mock_ir.return_value = "abcdefghijklmnopqrstuvwxyz123456"

    # create dummy source code hash
    mock_sc_h.return_value = "abcdefghijklmnopqrstuvwxyz123456abcdefghijklmnopqrstuvwxyz234567"

    # create dummy markers for return
    mock_cp_markers.return_value = []
    mock_ev_markers.return_value = [
        EvaluationMarkerData(2, EvaluationType.DECISION, CodeSectionData(
            CodePositionData(3, 5), CodePositionData(3, 10))),
        EvaluationMarkerData(3, EvaluationType.CONDITION, CodeSectionData(CodePositionData(3, 5), CodePositionData(3, 10)))]

    # start instrumentation with marker
    instrumenter.start_instrumentation()

    # write output file
    instrumenter.write_output_file()

    # open output file and compare with reference string
    with open(tmpdir.join('test_file.instr.c'), 'r') as output_source_code_ptr:
        source_code_instr_string = output_source_code_ptr.read()

    print(source_code_instr_string)

    source_code_instr_ref_str = '''#include "C:\\testpath\\coveron_helper.h"
___COVERON_FILE_T ___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456 = {
{0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x12, 0x34, 0x56, 0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x23, 0x45, 0x67},
{0xAB, 0xCD, 0xEF, 0xGH, 0xIJ, 0xKL, 0xMN, 0xOP, 0xQR, 0xST, 0xUV, 0xWX, 0xYZ, 0x12, 0x34, 0x56},
___COVERON_BOOL_FALSE,
NULL,
 "test_file.cri"};

int main() {
    test0;
    ___COVERON_SET_EVALUATION_MARKER(0x00, 0x00, 0x00, 0x02, &___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456, ___COVERON_SET_EVALUATION_MARKER(0x00, 0x00, 0x00, 0x03, &___COVERON_FILE_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456, test1));
    test2;
}'''

    assert source_code_instr_string == source_code_instr_ref_str
