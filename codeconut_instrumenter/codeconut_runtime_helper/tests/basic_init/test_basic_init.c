// Copyright 2020 Glenn Töws
//
// This file is part of the Codeconut project
//
// The Codeconut project is licensed under the LGPL-3.0 license

// TEST FILE FOR RUNTIME HELPER INITIALIZATION

#include "codeconut_helper.h"
#include "mock_fake_stdio.h"
#include "unity.h"

/*
 * SECTION   STRINGIFY FOR COMMENT PARSING
 */
#define STRINGIFY(x) #x
#define CMD_STRING(x) STRINGIFY(x)
// !SECTION

/*
 * SECTION   TEST DATA
 */

FILE dummy_file;

___CODECONUT_FILE_T testInputData = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                                     {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                                     ___CODECONUT_BOOL_FALSE,
                                     NULL,
                                     "test_output.cri"};

const ___CODECONUT_FILE_T testInputData_default = {
    {0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA,
     0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5,
     0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF},
    {0x50,
     0x51,
     0x52,
     0x53,
     0x54,
     0x55,
     0x56,
     0x57,
     0x58,
     0x59,
     0x5A,
     0x5B,
     0x5C,
     0x5D,
     0x5E,
     0x5F},
    ___CODECONUT_BOOL_FALSE,
    NULL,
    "test_output.cri"};
// !SECTION

/*
 * SECTION   SETUP & TEARDOWN FUNCTIONS
 */
void setUp() {
    // reinitialize criFile array
    for (int i = 0; i < sizeof(testInputData_default); i++) {
        ((uint8_t *)&testInputData)[i] = ((uint8_t *)&testInputData_default)[i];
    }
}

void tearDown() {}
// !SECTION

/*
 * SECTION   TEST FUNCTIONS
 */
// Test with the return of a null pointer for the file
void test_basic_null_ptr_criFile(void) {
    // expect the loading of a eventually existing file, return NULL pointer
    FOPEN_ExpectAndReturn(testInputData_default.outputFilename, "ab+", (void *)NULL);

    // expect the creation of a new file
    FILE *dummyFilePointer = &(dummy_file);
    FREOPEN_ExpectAndReturn(
        testInputData_default.outputFilename, "wb+", (void *)NULL, dummyFilePointer);

    // expect the writing of a new header
    uint8_t comparisonHeaderArray[59] = {
        0x49, 0x4D, 0x41, 0x43, 0x52, 0x49, 0x46, 0x21,  // magic number
        0x00, 0x01,                                      // version
        0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA,
        0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5,
        0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,  // SHA256 hash
        0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A,
        0x5B, 0x5C, 0x5D, 0x5E, 0x5F,  // Instrumentation random
        0x0A                           // newline
    };
    FWRITE_ExpectWithArrayAndReturn(
        comparisonHeaderArray, 59, 1, 59, dummyFilePointer, sizeof(dummyFilePointer), 59);

    // expect the creation of a execution marker
    uint8_t comparisonExecutionMarkerArray[9] = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x52, 0x55, 0x4E, 0x21};
    FWRITE_ExpectWithArrayAndReturn(
        comparisonExecutionMarkerArray,
        9,  // only compare the first 9 bytes (since the comment length is variable)
        1,
        10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)),
        dummyFilePointer,
        sizeof(dummyFilePointer),
        10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)));

    // ignore further write commands for marker execution
    FWRITE_IgnoreAndReturn(0);

    // simulate the writing of a checkpoint marker
    ___CODECONUT_SET_CHECKPOINT_MARKER(0, 0, 0, 0, &testInputData);

    // check, if the given codeconutFile object is set to initialized
    TEST_ASSERT_EQUAL_INT(___CODECONUT_BOOL_TRUE, testInputData.helperInitialized);
    return;
}

// Test with the return of a null pointer for the file, but fail at file creation
void test_basic_fail_file_creation(void) {
    // expect the loading of a eventually existing file, return NULL pointer
    FOPEN_ExpectAndReturn(testInputData_default.outputFilename, "ab+", (void *)NULL);

    // expect the creation of a new file, return NULL pointer
    FREOPEN_ExpectAndReturn(
        testInputData_default.outputFilename, "wb+", (void *)NULL, (void *)NULL);

    // simulate the writing of checkpoint marker
    ___CODECONUT_SET_CHECKPOINT_MARKER(0, 0, 0, 0, &testInputData);

    // check, if the given codeconutFile object is set to not initialized
    TEST_ASSERT_EQUAL_INT(___CODECONUT_BOOL_FALSE, testInputData.helperInitialized);
}

// Test with the return of a empty cri file

void test_basic_corrupted_criFile(void) {
    // expect the loading of a eventually existing file, return dummy pointer
    FILE *dummyFilePointer = &(dummy_file);
    FOPEN_ExpectAndReturn(testInputData_default.outputFilename, "ab+", dummyFilePointer);

    // return empty array
    uint8_t corruptedData[59] = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
    FSEEK_ExpectAndReturn(dummyFilePointer, 0, SEEK_SET, 0);
    FREAD_ExpectAndReturn((void *)NULL, 1, 59, dummyFilePointer, 59);
    FREAD_IgnoreArg_cmock_arg1();
    FREAD_ReturnArrayThruPtr_cmock_arg1(corruptedData, 59);

    // Header creation procedure already was tested, so ignore that
    FREOPEN_IgnoreAndReturn(dummyFilePointer);
    FWRITE_IgnoreAndReturn(0);

    // simulate the writing of a checkpoint marker
    ___CODECONUT_SET_CHECKPOINT_MARKER(0, 0, 0, 0, &testInputData);

    // check, if the given codeconutFile object is set to not initialized
    TEST_ASSERT_EQUAL_INT(___CODECONUT_BOOL_TRUE, testInputData.helperInitialized);
}

void test_basic_correct_criFile(void) {
    // expect the loading of a eventually existing file, return dummy pointer
    FILE *dummyFilePointer = &(dummy_file);
    FOPEN_ExpectAndReturn(testInputData_default.outputFilename, "ab+", dummyFilePointer);

    // return empty array
    uint8_t correctData[59] = {
        0x49, 0x4D, 0x41, 0x43, 0x52, 0x49, 0x46, 0x21,  // magic number
        0x00, 0x01,                                      // version
        0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5, 0xA6, 0xA7, 0xA8, 0xA9, 0xAA,
        0xAB, 0xAC, 0xAD, 0xAE, 0xAF, 0xB0, 0xB1, 0xB2, 0xB3, 0xB4, 0xB5,
        0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC, 0xBD, 0xBE, 0xBF,  // SHA256 hash
        0x50, 0x51, 0x52, 0x53, 0x54, 0x55, 0x56, 0x57, 0x58, 0x59, 0x5A,
        0x5B, 0x5C, 0x5D, 0x5E, 0x5F,  // Instrumentation random
        0x0A                           // newline
    };
    FSEEK_ExpectAndReturn(dummyFilePointer, 0, SEEK_SET, 0);
    FREAD_ExpectAndReturn((void *)NULL, 1, 59, dummyFilePointer, 59);
    FREAD_IgnoreArg_cmock_arg1();
    FREAD_ReturnArrayThruPtr_cmock_arg1(correctData, 59);

    // expect file pointer to set to last char
    FSEEK_ExpectAndReturn(dummyFilePointer, 0, SEEK_END, 0);

    // expect the creation of a execution marker
    uint8_t comparisonExecutionMarkerArray[9] = {
        0x00, 0x00, 0x00, 0x00, 0x00, 0x52, 0x55, 0x4E, 0x21};
    FWRITE_ExpectWithArrayAndReturn(
        comparisonExecutionMarkerArray,
        9,  // only compare the first 9 bytes (since the comment length is variable)
        1,
        10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)),
        dummyFilePointer,
        sizeof(dummyFilePointer),
        10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)));

    // expect one write for checkpoint
    FWRITE_ExpectAnyArgsAndReturn(0);

    // simulate the writing of a checkpoint marker
    ___CODECONUT_SET_CHECKPOINT_MARKER(0, 0, 0, 0, &testInputData);

    // check, if the given codeconutFile object is set to not initialized
    TEST_ASSERT_EQUAL_INT(___CODECONUT_BOOL_TRUE, testInputData.helperInitialized);
}
// !SECTION