// Copyright 2020 Glenn Töws
//
// This file is part of the Coveron project
//
// The Coveron project is licensed under the LGPL-3.0 license

#ifndef ___COVERON_HELPER_
#define ___COVERON_HELPER_

/*
 * SECTION   INCLUDES
 */
// !SECTION

/*
 * SECTION   UNIT TESTING SETUP
 */
#ifdef ___COVERON_DEV_RUNTIME_HELPER_UNIT_TEST
#include "fake_stdio.h"
#define fopen FOPEN
#define freopen FREOPEN
#define fseek FSEEK
#define fread FREAD
#define fwrite FWRITE
#define fflush FFLUSH
#endif
// !SECTION

/*
 * SECTION   TYPEDEFS
 */
typedef unsigned char uint8_t;

typedef enum
{
    ___COVERON_BOOL_FALSE,
    ___COVERON_BOOL_TRUE
} ___COVERON_BOOL_T;

/* NOTE The coveron file variable name should include the instrumentation random
 *      to prevent duplicate variable names when directly including c files
 */
typedef struct ___COVERON_FILE_S
{
    // SHA256 hash of uninstrumented source code (length = 32 bytes)
    uint8_t SHA256Hash[32];

    // Instrumentation random (length = 16 bytes)
    uint8_t instrumentationRandom[16];

    // Status variable to see, if the helper is initialized for this file
    ___COVERON_BOOL_T helperInitialized;

    // File pointer
    void *criFile;

    // Filename for the output file (last item because of variable size)
    char outputFilename[];
} ___COVERON_FILE_T;
// !SECTION

/*
 * SECTION   PUBLIC FUNCTION DECLARATIONS
 */
#ifdef ___COVERON_CHECKPOINT_ANALYSIS_ENABLED
void ___COVERON_SET_CHECKPOINT_MARKER(uint8_t markerId_B0,
                                      uint8_t markerId_B1,
                                      uint8_t markerId_B2,
                                      uint8_t markerId_B3,
                                      ___COVERON_FILE_T *coveronFile);
#endif

#ifdef ___COVERON_EVALUATION_ANALYSIS_ENABLED
___COVERON_BOOL_T ___COVERON_SET_EVALUATION_MARKER(uint8_t markerId_B0,
                                                   uint8_t markerId_B1,
                                                   uint8_t markerId_B2,
                                                   uint8_t markerId_B3,
                                                   ___COVERON_FILE_T *coveronFile,
                                                   ___COVERON_BOOL_T evaluation);
#endif
// !SECTION

#endif // ___COVERON_HELPER_
