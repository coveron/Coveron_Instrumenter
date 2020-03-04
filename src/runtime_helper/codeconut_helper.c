// Copyright 2020 Glenn Töws
//
// This file is part of the Codeconut project
//
// The Codeconut project is licensed under the LGPL-3.0 license

/*
 * SECTION   INCLUDES
 */
#include "codeconut_helper.h"
#include <stdio.h>

/*
 * SECTION   VERSION INFORMATION
 */
#define ___CODECONUT_CRI_VERSION_HB 0x00 // High-Byte of the CRI version
#define ___CODECONUT_CRI_VERSION_LB 0x01 // Low-Byte of the CRI version

/*
 * SECTION   MAGIC NUMBER
 */
#define ___CODECONUT_MAGIC_NUMBER_B0 0x49
#define ___CODECONUT_MAGIC_NUMBER_B1 0x4D
#define ___CODECONUT_MAGIC_NUMBER_B2 0x41
#define ___CODECONUT_MAGIC_NUMBER_B3 0x43
#define ___CODECONUT_MAGIC_NUMBER_B4 0x52
#define ___CODECONUT_MAGIC_NUMBER_B5 0x49
#define ___CODECONUT_MAGIC_NUMBER_B6 0x46
#define ___CODECONUT_MAGIC_NUMBER_B7 0x21

/*
 * SECTION   PRIVATE FUNCTION DECLARATIONS
 */

void ___CODECONUT_SETUP_INSTRUMENTATION(___CODECONUT_FILE_T *codeconutFile); // configures the setup

/*
 * SECTION   RUNTIME VARIABLES
 */
___CODECONUT_BOOL_T instrumenterInitialized = ___CODECONUT_BOOL_FALSE;
FILE *criFile;

/*
 * SECTION   FUNCTION DEFINITIONS
 */

void ___CODECONUT_SETUP_INSTRUMENTATION(___CODECONUT_FILE_T *codeconutFile)
{
}

void ___CODECONUT_SET_STATEMENT_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T flushBuffer)
{
}

void ___CODECONUT_SET_DECISION_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T decision)
{
}

void ___CODECONUT_SET_CONDITION_MARKER(uint32_t markerId, ___CODECONUT_FILE_T *codeconutFile, ___CODECONUT_BOOL_T condition)
{
}
