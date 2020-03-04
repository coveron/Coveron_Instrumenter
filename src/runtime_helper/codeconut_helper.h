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

/*
 * SECTION   TYPEDEFS
 */

typedef enum
{
    ___CODECONUT_BOOL_FALSE,
    ___CODECONUT_BOOL_TRUE
} ___CODECONUT_BOOL_T;

typedef struct ___CODECONUT_FILE_S
{
    // SHA256 hash of uninstrumented source code (length = 32 bytes)
    uint8_t SHA256Hash[32];

    // Instrumentation random (length = 16 bytes)
    uint8_t instrumentationRandom[16];
} ___CODECONUT_FILE_T;

/*
 * SECTION   PUBLIC FUNCTION DECLARATIONS
 */

#ifdef ___CODECONUT_STATEMENT_ANALYSIS_ENABLED
void ___CODECONUT_SET_STATEMENT_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T flushBuffer);
#endif

#ifdef ___CODECONUT_DECISION_ANALYSIS_ENABLED
void ___CODECONUT_SET_DECISION_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T decision);
#endif

#ifdef ___CODECONUT_CONDITION_ANALYSIS_ENABLED
void ___CODECONUT_SET_CONDITION_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T condition);
#endif

#endif // ___CODECONUT_HELPER_