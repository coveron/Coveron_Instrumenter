// Copyright 2020 Glenn Töws
//
// This file is part of the Codeconut project
//
// The Codeconut project is licensed under the LGPL-3.0 license

/*
 * SECTION   INCLUDES
 */
#include "codeconut_helper.h"
// !SECTION

/*
 * SECTION   STRINGIFY FOR COMMENT PARSING
 */
#define STRINGIFY(x) #x
#define CMD_STRING(x) STRINGIFY(x)
// !SECTION

/*
 * SECTION   DEFAULT EXECUTION INFO
 */
#ifndef CODECONUT_EXECUTION_COMMENT
#define CODECONUT_EXECUTION_COMMENT ""
#endif
// !SECTION

/*
 * SECTION   VERSION INFORMATION
 */
uint8_t ___CODECONUT_CRI_VERSION[2] = {
    0x00,  // High byte
    0x01   // Low byte
};
// !SECTION

/*
 * SECTION   MAGIC NUMBER
 */
const uint8_t ___CODECONUT_MAGIC_NUMBER[8] = {
    0x49,  // I
    0x4D,  // M
    0x41,  // A
    0x43,  // C
    0x52,  // R
    0x49,  // I
    0x46,  // F
    0x21   // !
};
// !SECTION

/*
 * SECTION   PRIVATE FUNCTION DECLARATIONS
 */
// initializes the instrumentation helper for one source file
___CODECONUT_BOOL_T ___CODECONUT_SETUP_INSTRUMENTATION(
    ___CODECONUT_FILE_T *codeconutFile);

// creates new output file in case old is damaged or not existing
___CODECONUT_BOOL_T ___CODECONUT_CREATE_NEW_OUTPUT_FILE(
    ___CODECONUT_FILE_T *codeconutFile);

// compares arrays (useful for validation of existing files)
___CODECONUT_BOOL_T ___CODECONUT_EQUAL_ARRAYS(uint8_t *Array1,
                                              uint8_t *Array2,
                                              int byteCount);

// copies array contents to another array for given length
void ___CODECONUT_COPY_ARRAY(uint8_t *SrcArray, uint8_t *DestArray, int byteCount);

// generates correct header out of the given codeconutFile pointer
void ___CODECONUT_GENERATE_HEADER(___CODECONUT_FILE_T *codeconutFile,
                                  uint8_t emptyArray[59]);

// generates execution marker
void ___CODECONUT_GENERATE_EXECUTION_MARKER(___CODECONUT_FILE_T *codeconutFile);
// !SECTION

/*
 * SECTION   PRIVATE FUNCTION DEFINITIONS
 */
___CODECONUT_BOOL_T ___CODECONUT_SETUP_INSTRUMENTATION(
    ___CODECONUT_FILE_T *codeconutFile) {
#ifdef CODECONUT_NO_CONCATENATED_EXECUTIONS
    // shortcut to just create a new file
    return ___CODECONUT_CREATE_NEW_OUTPUT_FILE(codeconutFile);
#endif
    /*
     * load input file
     */
    // load file as read and append
    codeconutFile->criFile = fopen(codeconutFile->outputFilename, "ab+");

    // check if file was successfully opened
    if (codeconutFile->criFile == NULL) {
        // try to create a new file
        return ___CODECONUT_CREATE_NEW_OUTPUT_FILE(codeconutFile);
    }

    /*
     * check header
     */
    // create correct header to compare to
    uint8_t headerSample[59];
    ___CODECONUT_GENERATE_HEADER(codeconutFile, headerSample);

    // read header from input file
    uint8_t headerRead[59];
    fseek(codeconutFile->criFile, 0, SEEK_SET);
    fread(&headerRead[0], 1, 59, codeconutFile->criFile);

    // compare header
    if (___CODECONUT_EQUAL_ARRAYS(&headerSample[0], &headerRead[0], 59) ==
        ___CODECONUT_BOOL_FALSE) {
        // if not equal, try to create a new file
        return ___CODECONUT_CREATE_NEW_OUTPUT_FILE(codeconutFile);
    }

    /*
     * set reader to end of file
     */
    fseek(codeconutFile->criFile, 0, SEEK_END);

    /*
     * generate execution marker
     */
    ___CODECONUT_GENERATE_EXECUTION_MARKER(codeconutFile);

    /*
     * set initialization var to true
     */
    codeconutFile->helperInitialized = ___CODECONUT_BOOL_TRUE;

    return ___CODECONUT_BOOL_TRUE;
}

___CODECONUT_BOOL_T ___CODECONUT_CREATE_NEW_OUTPUT_FILE(
    ___CODECONUT_FILE_T *codeconutFile) {
    /*
     * load input file
     */
    // load file as read and write
    codeconutFile->criFile =
        freopen(codeconutFile->outputFilename, "wb+", codeconutFile->criFile);

    // check if file was successfully opened
    if (codeconutFile->criFile == NULL) {
        // if not, return bad
        return ___CODECONUT_BOOL_FALSE;
    }

    /*
     * generate header
     */
    // create header in array
    uint8_t headerArray[59];
    ___CODECONUT_GENERATE_HEADER(codeconutFile, headerArray);

    // write to file
    fwrite(&headerArray[0], 1, 59, codeconutFile->criFile);

    /*
     * generate execution marker
     */
    ___CODECONUT_GENERATE_EXECUTION_MARKER(codeconutFile);

    /*
     * set initialization var to true
     */
    codeconutFile->helperInitialized = ___CODECONUT_BOOL_TRUE;
}

___CODECONUT_BOOL_T ___CODECONUT_EQUAL_ARRAYS(uint8_t *Array1,
                                              uint8_t *Array2,
                                              int byteCount) {
    // iterate over arrays for given byte length
    for (int i = 0; i < byteCount; i++) {
        // compare array items
        if (Array1[i] != Array2[i]) {
            return ___CODECONUT_BOOL_FALSE;
        }
    }

    return ___CODECONUT_BOOL_TRUE;
}

void ___CODECONUT_COPY_ARRAY(uint8_t *SrcArray, uint8_t *DestArray, int byteCount) {
    // iterate over arrays for given byte length
    for (int i = 0; i < byteCount; i++) {
        // set destination array value equal to source array
        DestArray[i] = SrcArray[i];
    }
}

void ___CODECONUT_GENERATE_HEADER(___CODECONUT_FILE_T *codeconutFile,
                                  uint8_t emptyArray[59]) {
    // write magic number
    ___CODECONUT_COPY_ARRAY((uint8_t *)&___CODECONUT_MAGIC_NUMBER[0], &emptyArray[0], 8);

    // write version
    ___CODECONUT_COPY_ARRAY((uint8_t *)&___CODECONUT_CRI_VERSION[0], &emptyArray[8], 2);

    // write SHA256 hash
    ___CODECONUT_COPY_ARRAY(&codeconutFile->SHA256Hash[0], &emptyArray[10], 32);

    // write instrumentation random
    ___CODECONUT_COPY_ARRAY(
        &codeconutFile->instrumentationRandom[0], &emptyArray[42], 16);

    // new line marker
    emptyArray[58] = 0x0A;
}

void ___CODECONUT_GENERATE_EXECUTION_MARKER(___CODECONUT_FILE_T *codeconutFile) {
    // generate execution marker array
    uint8_t executionMarkerArray[10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT))];

    // fill first 5 bytes with padding
    executionMarkerArray[0] = 0x00;
    executionMarkerArray[1] = 0x00;
    executionMarkerArray[2] = 0x00;
    executionMarkerArray[3] = 0x00;
    executionMarkerArray[4] = 0x00;

    // fill next 4 bytes with execution marker magic number
    executionMarkerArray[5] = 0x52;
    executionMarkerArray[6] = 0x55;
    executionMarkerArray[7] = 0x4E;
    executionMarkerArray[8] = 0x21;

    // fill in execution comment
    char commentString[sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT))] =
        CMD_STRING(CODECONUT_EXECUTION_COMMENT);
    ___CODECONUT_COPY_ARRAY((uint8_t *)commentString,
                            &executionMarkerArray[9],
                            sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)));

    // new line char
    executionMarkerArray[9 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT))] = 0x0A;

    // write to file
    fwrite(&executionMarkerArray[0],
           1,
           10 + sizeof(CMD_STRING(CODECONUT_EXECUTION_COMMENT)),
           codeconutFile->criFile);
}
// !SECTION
/*
 * SECTION   PUBLIC FUNCTION DEFINITIONS
 */
#ifdef CODECONUT_STATEMENT_ANALYSIS_ENABLED
inline void ___CODECONUT_SET_STATEMENT_MARKER(uint8_t markerId_B0,
                                              uint8_t markerId_B1,
                                              uint8_t markerId_B2,
                                              uint8_t markerId_B3,
                                              ___CODECONUT_FILE_T *codeconutFile) {
    // check, if the helper was initialized
    if (codeconutFile->helperInitialized == ___CODECONUT_BOOL_FALSE &&
        ___CODECONUT_SETUP_INSTRUMENTATION(codeconutFile) == ___CODECONUT_BOOL_FALSE) {
        return;
    }

    uint8_t markerData[5] = {markerId_B0, markerId_B1, markerId_B2, markerId_B3, 0x00};
    fwrite(markerData, 1, 5, codeconutFile->criFile);
}
#endif

#ifdef CODECONUT_DECISION_ANALYSIS_ENABLED
inline ___CODECONUT_BOOL_T ___CODECONUT_SET_DECISION_MARKER(
    uint8_t markerId_B0,
    uint8_t markerId_B1,
    uint8_t markerId_B2,
    uint8_t markerId_B3,
    ___CODECONUT_FILE_T *codeconutFile,
    ___CODECONUT_BOOL_T decision) {
    // check, if the helper was initialized
    if (codeconutFile->helperInitialized == ___CODECONUT_BOOL_FALSE &&
        ___CODECONUT_SETUP_INSTRUMENTATION(codeconutFile) == ___CODECONUT_BOOL_FALSE) {
        return decision;
    }

    // create output array
    uint8_t markerData[5] = {markerId_B0, markerId_B1, markerId_B2, markerId_B3, 0x59};
    if (decision == ___CODECONUT_BOOL_TRUE) {
        markerData[4] = 0xA6;
    }

    // write marker to output file
    fwrite(markerData, 1, 5, codeconutFile->criFile);

    // pass on the input data
    return decision;
}
#endif

#ifdef CODECONUT_CONDITION_ANALYSIS_ENABLED
inline ___CODECONUT_BOOL_T ___CODECONUT_SET_CONDITION_MARKER(
    uint8_t markerId_B0,
    uint8_t markerId_B1,
    uint8_t markerId_B2,
    uint8_t markerId_B3,
    ___CODECONUT_FILE_T *codeconutFile,
    ___CODECONUT_BOOL_T condition) {
    // check, if the helper was initialized
    if (codeconutFile->helperInitialized == ___CODECONUT_BOOL_FALSE &&
        ___CODECONUT_SETUP_INSTRUMENTATION(codeconutFile) == ___CODECONUT_BOOL_FALSE) {
        return condition;
    }

    // create output array
    uint8_t markerData[5] = {markerId_B0, markerId_B1, markerId_B2, markerId_B3, 0x59};
    if (condition == ___CODECONUT_BOOL_TRUE) {
        markerData[4] = 0xA6;
    }

    // write marker to output file
    fwrite(markerData, 1, 5, codeconutFile->criFile);

    // pass on the input data
    return condition;
}
#endif
// !SECTION