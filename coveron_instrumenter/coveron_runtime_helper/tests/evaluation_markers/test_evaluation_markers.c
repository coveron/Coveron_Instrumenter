// Copyright 2020 Glenn Töws
//
// This file is part of the Coveron project
//
// The Coveron project is licensed under the LGPL-3.0 license

// TEST FILE FOR EVALUATION MARKERS

#include "coveron_helper.h"
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
FILE *dummyFilePointer = &dummy_file;

___COVERON_FILE_T testInputData = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                                   {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                                   ___COVERON_BOOL_FALSE,
                                   NULL,
                                   "test_output.cri"};

const ___COVERON_FILE_T testInputData_default = {
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
    ___COVERON_BOOL_TRUE,
    NULL,
    "test_output.cri"};
// !SECTION

/*
 * SECTION   SETUP & TEARDOWN FUNCTIONS
 */
void setUp()
{
    // reinitialize criFile array
    for (int i = 0; i < sizeof(testInputData_default); i++)
    {
        ((uint8_t *)&testInputData)[i] = ((uint8_t *)&testInputData_default)[i];
    }

    // set criFIle pointer to dummy
    testInputData.criFile = dummyFilePointer;
}

void tearDown() {}
// !SECTION

/*
 * SECTION   TEST FUNCTIONS
 */
// Test the creation of a evaluation marker with true evaluation
void test_create_evaluation_marker_true(void)
{
    // expect the creation of a evaluation marker
    uint8_t comparisonDecisionMarkerArray[5] = {0x51, 0x52, 0x53, 0x54, 0xA6};
    FWRITE_ExpectWithArrayAndReturn(comparisonDecisionMarkerArray,
                                    5,
                                    1,
                                    5, // 5 bytes marker length
                                    dummyFilePointer,
                                    sizeof(dummyFilePointer),
                                    5);

    // simulate the writing of a evaluation marker
    int a = 5;
    ___COVERON_SET_EVALUATION_MARKER(0x51, 0x52, 0x53, 0x54, &testInputData, (a == 5));
}

// Test the creation of a evaluation marker with false evaluation
void test_create_evaluation_marker_false(void)
{
    // expect the creation of a evaluation marker
    uint8_t comparisonDecisionMarkerArray[5] = {0x51, 0x52, 0x53, 0x54, 0x59};
    FWRITE_ExpectWithArrayAndReturn(comparisonDecisionMarkerArray,
                                    5,
                                    1,
                                    5, // 5 bytes marker length
                                    dummyFilePointer,
                                    sizeof(dummyFilePointer),
                                    5);

    // simulate the writing of a evaluation marker
    int a = 2;
    ___COVERON_SET_EVALUATION_MARKER(0x51, 0x52, 0x53, 0x54, &testInputData, (a == 5));
}
// !SECTION