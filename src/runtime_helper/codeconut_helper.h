// Copyright 2020 Glenn Töws
//
// This file is part of the Codeconut project
//
// The Codeconut project is licensed under the LGPL-3.0 license

#ifndef ___CODECONUT_HELPER_
#define ___CODECONUT_HELPER_

/*
 * SECTION   INCLUDES
 */
#include <stdint.h>
#include <stdio.h>
// !SECTION

/*
 * SECTION   UNIT TESTING SETUP
 */
#ifdef ___CODECONUT_DEV_RUNTIME_HELPER_UNIT_TEST
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
typedef enum { ___CODECONUT_BOOL_FALSE, ___CODECONUT_BOOL_TRUE } ___CODECONUT_BOOL_T;

/* NOTE The codeconut file variable name should include the instrumentation random
 *      to prevent duplicate variable names when directly including c files
 */
typedef struct ___CODECONUT_FILE_S {
    // SHA256 hash of uninstrumented source code (length = 32 bytes)
    uint8_t SHA256Hash[32];

    // Instrumentation random (length = 16 bytes)
    uint8_t instrumentationRandom[16];

    // Status variable to see, if the helper is initialized for this file
    ___CODECONUT_BOOL_T helperInitialized;

    // File pointer
    FILE *criFile;

    // Filename for the output file (last item because of variable size)
    char outputFilename[];
} ___CODECONUT_FILE_T;
// !SECTION

/*
 * SECTION   PUBLIC FUNCTION DECLARATIONS
 */
#ifdef CODECONUT_STATEMENT_ANALYSIS_ENABLED
void ___CODECONUT_SET_STATEMENT_MARKER(uint8_t markerId_B0,
                                       uint8_t markerId_B1,
                                       uint8_t markerId_B2,
                                       uint8_t markerId_B3,
                                       ___CODECONUT_FILE_T *codeconutFile);
#endif

#ifdef CODECONUT_DECISION_ANALYSIS_ENABLED
___CODECONUT_BOOL_T ___CODECONUT_SET_DECISION_MARKER(uint8_t markerId_B0,
                                                     uint8_t markerId_B1,
                                                     uint8_t markerId_B2,
                                                     uint8_t markerId_B3,
                                                     ___CODECONUT_FILE_T *codeconutFile,
                                                     ___CODECONUT_BOOL_T decision);
#endif

#ifdef CODECONUT_CONDITION_ANALYSIS_ENABLED
___CODECONUT_BOOL_T ___CODECONUT_SET_CONDITION_MARKER(uint8_t markerId_B0,
                                                      uint8_t markerId_B1,
                                                      uint8_t markerId_B2,
                                                      uint8_t markerId_B3,
                                                      ___CODECONUT_FILE_T *codeconutFile,
                                                      ___CODECONUT_BOOL_T condition);
#endif
// !SECTION

#endif  // ___CODECONUT_HELPER_
