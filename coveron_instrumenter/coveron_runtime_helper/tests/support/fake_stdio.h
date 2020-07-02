// Copyright 2020 Glenn Töws
//
// This file is part of the Coveron project
//
// The Coveron project is licensed under the LGPL-3.0 license

// MOCK FILE FOR STDIO SIMULATION

#include "stdint.h"
#include "stdio.h"

FILE *FOPEN(const char *, const char *);

FILE *FREOPEN(const char *, const char *, FILE *);

int FSEEK(FILE *, long, int);

size_t FREAD(void *, size_t, size_t, FILE *);

size_t FWRITE(const void *, size_t, size_t, FILE *);
