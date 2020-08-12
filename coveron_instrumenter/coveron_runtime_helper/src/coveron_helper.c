// Copyright 2020 Glenn Töws
//
// This file is part of the Coveron project
//
// The Coveron project is licensed under the LGPL-3.0 license

/*
 * SECTION   INCLUDES
 */
#include "coveron_helper.h"
#include <stdio.h>
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
#ifndef COVERON_EXECUTION_COMMENT
#define COVERON_EXECUTION_COMMENT ""
#endif
// !SECTION

/*
 * SECTION   VERSION INFORMATION
 */
___COVERON_BYTE ___COVERON_CRI_VERSION[2] = {
    0x00, // High byte
    0x01  // Low byte
};
// !SECTION

/*
 * SECTION   MAGIC NUMBER
 */
const ___COVERON_BYTE ___COVERON_MAGIC_NUMBER[8] = {
    0x49, // I
    0x4D, // M
    0x41, // A
    0x43, // C
    0x52, // R
    0x49, // I
    0x46, // F
    0x21  // !
};
// !SECTION

/*
 * SECTION   PRIVATE FUNCTION DECLARATIONS
 */
// initializes the instrumentation helper for one source file
___COVERON_BOOL_T ___COVERON_SETUP_INSTRUMENTATION(
    ___COVERON_FILE_T *coveronFile);

// creates new output file in case old is damaged or not existing
___COVERON_BOOL_T ___COVERON_CREATE_NEW_OUTPUT_FILE(
    ___COVERON_FILE_T *coveronFile);

// compares arrays (useful for validation of existing files)
___COVERON_BOOL_T ___COVERON_EQUAL_ARRAYS(___COVERON_BYTE *Array1,
                                          ___COVERON_BYTE *Array2,
                                          int byteCount);

// copies array contents to another array for given length
void ___COVERON_COPY_ARRAY(___COVERON_BYTE *SrcArray, ___COVERON_BYTE *DestArray, int byteCount);

// generates correct header out of the given coveronFile pointer
void ___COVERON_GENERATE_HEADER(___COVERON_FILE_T *coveronFile,
                                ___COVERON_BYTE emptyArray[59]);

// generates execution marker
void ___COVERON_GENERATE_EXECUTION_MARKER(___COVERON_FILE_T *coveronFile);
// !SECTION

/*
 * SECTION   PRIVATE FUNCTION DEFINITIONS
 */
___COVERON_BOOL_T ___COVERON_SETUP_INSTRUMENTATION(
    ___COVERON_FILE_T *coveronFile)
{
#ifdef COVERON_NO_CONCATENATED_EXECUTIONS
    // shortcut to just create a new file
    return ___COVERON_CREATE_NEW_OUTPUT_FILE(coveronFile);
#endif
    /*
     * load input file
     */
    // load file as read and append
    coveronFile->criFile = fopen(coveronFile->outputFilename, "ab+");

    // check if file wasn't successfully opened
    if (coveronFile->criFile == NULL)
    {
        // try to create a new file
        return ___COVERON_CREATE_NEW_OUTPUT_FILE(coveronFile);
    }

    /*
     * check header
     */
    // create correct header to compare to
    ___COVERON_BYTE headerSample[59];
    ___COVERON_GENERATE_HEADER(coveronFile, headerSample);

    // read header from input file
    ___COVERON_BYTE headerRead[59];
    fseek(coveronFile->criFile, 0, SEEK_SET);
    fread(&headerRead[0], 1, 59, coveronFile->criFile);

    // compare header
    if (___COVERON_EQUAL_ARRAYS(&headerSample[0], &headerRead[0], 59) ==
        ___COVERON_BOOL_FALSE)
    {
        // if not equal, try to create a new file
        return ___COVERON_CREATE_NEW_OUTPUT_FILE(coveronFile);
    }

    /*
     * set reader to end of file
     */
    fseek(coveronFile->criFile, 0, SEEK_END);

    /*
     * generate execution marker
     */
    ___COVERON_GENERATE_EXECUTION_MARKER(coveronFile);

    /*
     * set initialization var to true
     */
    coveronFile->helperInitialized = ___COVERON_BOOL_TRUE;

    return ___COVERON_BOOL_TRUE;
}

___COVERON_BOOL_T ___COVERON_CREATE_NEW_OUTPUT_FILE(
    ___COVERON_FILE_T *coveronFile)
{
    /*
     * load input file
     */
    // load file as read and write
    coveronFile->criFile =
        freopen(coveronFile->outputFilename, "wb+", coveronFile->criFile);

    // check if file was successfully opened
    if (coveronFile->criFile == NULL)
    {
        // if not, return bad
        return ___COVERON_BOOL_FALSE;
    }

    /*
     * generate header
     */
    // create header in array
    ___COVERON_BYTE headerArray[59];
    ___COVERON_GENERATE_HEADER(coveronFile, headerArray);

    // write to file
    fwrite(&headerArray[0], 1, 59, coveronFile->criFile);

    /*
     * generate execution marker
     */
    ___COVERON_GENERATE_EXECUTION_MARKER(coveronFile);

    /*
     * set initialization var to true
     */
    coveronFile->helperInitialized = ___COVERON_BOOL_TRUE;
}

___COVERON_BOOL_T ___COVERON_EQUAL_ARRAYS(___COVERON_BYTE *Array1,
                                          ___COVERON_BYTE *Array2,
                                          int byteCount)
{
    // iterate over arrays for given byte length
    for (int i = 0; i < byteCount; i++)
    {
        // compare array items
        if (Array1[i] != Array2[i])
        {
            return ___COVERON_BOOL_FALSE;
        }
    }

    return ___COVERON_BOOL_TRUE;
}

void ___COVERON_COPY_ARRAY(___COVERON_BYTE *SrcArray, ___COVERON_BYTE *DestArray, int byteCount)
{
    // iterate over arrays for given byte length
    for (int i = 0; i < byteCount; i++)
    {
        // set destination array value equal to source array
        DestArray[i] = SrcArray[i];
    }
}

void ___COVERON_GENERATE_HEADER(___COVERON_FILE_T *coveronFile,
                                ___COVERON_BYTE emptyArray[59])
{
    // write magic number
    ___COVERON_COPY_ARRAY((___COVERON_BYTE *)&___COVERON_MAGIC_NUMBER[0], &emptyArray[0], 8);

    // write version
    ___COVERON_COPY_ARRAY((___COVERON_BYTE *)&___COVERON_CRI_VERSION[0], &emptyArray[8], 2);

    // write SHA256 hash
    ___COVERON_COPY_ARRAY(&coveronFile->SHA256Hash[0], &emptyArray[10], 32);

    // write instrumentation random
    ___COVERON_COPY_ARRAY(
        &coveronFile->instrumentationRandom[0], &emptyArray[42], 16);

    // new line marker
    emptyArray[58] = 0x0A;
}

void ___COVERON_GENERATE_EXECUTION_MARKER(___COVERON_FILE_T *coveronFile)
{
    // generate execution marker array
    ___COVERON_BYTE executionMarkerArray[10 + sizeof(CMD_STRING(COVERON_EXECUTION_COMMENT))];

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
    char commentString[sizeof(CMD_STRING(COVERON_EXECUTION_COMMENT))] =
        CMD_STRING(COVERON_EXECUTION_COMMENT);
    ___COVERON_COPY_ARRAY((___COVERON_BYTE *)commentString,
                          &executionMarkerArray[9],
                          sizeof(CMD_STRING(COVERON_EXECUTION_COMMENT)));

    // new line char
    executionMarkerArray[9 + sizeof(CMD_STRING(COVERON_EXECUTION_COMMENT))] = 0x0A;

    // write to file
    fwrite(&executionMarkerArray[0],
           1,
           10 + sizeof(CMD_STRING(COVERON_EXECUTION_COMMENT)),
           coveronFile->criFile);
}
// !SECTION
/*
 * SECTION   PUBLIC FUNCTION DEFINITIONS
 */
#ifdef ___COVERON_CHECKPOINT_ANALYSIS_ENABLED
inline void ___COVERON_SET_CHECKPOINT_MARKER(___COVERON_BYTE markerId_B0,
                                             ___COVERON_BYTE markerId_B1,
                                             ___COVERON_BYTE markerId_B2,
                                             ___COVERON_BYTE markerId_B3,
                                             ___COVERON_FILE_T *coveronFile)
{
    // check, if the helper was initialized
    if (coveronFile->helperInitialized == ___COVERON_BOOL_FALSE &&
        ___COVERON_SETUP_INSTRUMENTATION(coveronFile) == ___COVERON_BOOL_FALSE)
    {
        return;
    }

    ___COVERON_BYTE markerData[5] = {markerId_B0, markerId_B1, markerId_B2, markerId_B3, 0x00};
    fwrite(markerData, 1, 5, coveronFile->criFile);
}
#endif

#ifdef ___COVERON_EVALUATION_ANALYSIS_ENABLED
inline ___COVERON_BOOL_T ___COVERON_SET_EVALUATION_MARKER(
    ___COVERON_BYTE markerId_B0,
    ___COVERON_BYTE markerId_B1,
    ___COVERON_BYTE markerId_B2,
    ___COVERON_BYTE markerId_B3,
    ___COVERON_FILE_T *coveronFile,
    ___COVERON_BOOL_T evaluation)
{
    // check, if the helper was initialized
    if (coveronFile->helperInitialized == ___COVERON_BOOL_FALSE &&
        ___COVERON_SETUP_INSTRUMENTATION(coveronFile) == ___COVERON_BOOL_FALSE)
    {
        return evaluation;
    }

    // create output array
    ___COVERON_BYTE markerData[5] = {markerId_B0, markerId_B1, markerId_B2, markerId_B3, (___COVERON_BYTE) !(!evaluation)};

    // write marker to output file
    fwrite(markerData, 1, 5, coveronFile->criFile);

    // pass on the input data
    return evaluation;
}
#endif
// !SECTION