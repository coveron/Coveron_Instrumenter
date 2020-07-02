// Copyright 2020 Glenn Töws
//
// This file is part of the Coveron project
//
// The Coveron project is licensed under the LGPL-3.0 license

// TEST FILE DECISION AND CONDITION EVALUATION

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
 * SECTION SERVANTS FOR REPETITIVE TASKS
 */
void servant_expect_write(uint8_t expectArray[5])
{
    FWRITE_ExpectWithArrayAndReturn(expectArray,
                                    5,
                                    1,
                                    5, // 5 bytes marker length
                                    dummyFilePointer,
                                    sizeof(dummyFilePointer),
                                    5);
}
// !SECTION

/*
 * SECTION   TEST FUNCTIONS
 */
// Test simple true evaluation
void test_evaluation_simple_true(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0xA6}; // evaluates to true

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 5)));
}

// Test a == true && b == true evaluation
void test_evaluation_and_true(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0xA6}; // evaluates to true
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0xA6}; // evaluates to true

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonCondition2MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 5)) &&
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 2)));
}

// Test a == false && b == true evaluation (short-circuit)
void test_evaluation_and_false_short_circuit(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0x59}; // evaluates to false
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0x59}; // evaluates to false

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 4)) &&
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 2)));
}

// Test a == true && b == false evaluation
void test_evaluation_and_false(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0xA6}; // evaluates to true
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0x59}; // evaluates to false
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0x59}; // evaluates to false

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonCondition2MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 5)) &&
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 1)));
}

// Test a == true || b == true evaluation
void test_evaluation_or_true_short_circuit(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0xA6}; // evaluates to true
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0xA6}; // evaluates to true

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 5)) ||
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 2)));
}

// Test a == false || b == true evaluation
void test_evaluation_or_true(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0x59}; // evaluates to false
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0xA6}; // evaluates to true

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonCondition2MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 4)) ||
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 2)));
}

// Test a == false || b == false evaluation
void test_evaluation_or_false(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0x59}; // evaluates to false
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0x59}; // evaluates to false
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0x59}; // evaluates to false

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonCondition2MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 4)) ||
            ___COVERON_SET_EVALUATION_MARKER(
                0x71, 0x72, 0x73, 0x74, &testInputData, (b == 1)));
}

// Test a == true && (b == false || c == true) evaluation
void test_evaluation_complex1_true(void)
{
    // expect the creation of a condition marker
    uint8_t comparisonCondition1MarkerArray[5] = {
        0x61, 0x62, 0x63, 0x64, 0xA6}; // evaluates to true
    uint8_t comparisonCondition2MarkerArray[5] = {
        0x71, 0x72, 0x73, 0x74, 0x59}; // evaluates to false
    uint8_t comparisonCondition3MarkerArray[5] = {
        0x81, 0x82, 0x83, 0x84, 0xA6}; // evaluates to true
    uint8_t comparisonDecisionMarkerArray[5] = {
        0x51, 0x52, 0x53, 0x54, 0xA6}; // evaluates to true

    servant_expect_write(comparisonCondition1MarkerArray);
    servant_expect_write(comparisonCondition2MarkerArray);
    servant_expect_write(comparisonCondition3MarkerArray);
    servant_expect_write(comparisonDecisionMarkerArray);

    // simulate the evaluation
    int a = 5;
    int b = 2;
    int c = 10;
    ___COVERON_SET_EVALUATION_MARKER(
        0x51,
        0x52,
        0x53,
        0x54,
        &testInputData,
        ___COVERON_SET_EVALUATION_MARKER(
            0x61, 0x62, 0x63, 0x64, &testInputData, (a == 5)) &&
            (___COVERON_SET_EVALUATION_MARKER(
                 0x71, 0x72, 0x73, 0x74, &testInputData, (b == 1)) ||
             ___COVERON_SET_EVALUATION_MARKER(
                 0x81, 0x82, 0x83, 0x84, &testInputData, (c == 10))));
}

// !SECTION