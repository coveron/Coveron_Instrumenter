---
title: Codeconut Runtime Information (CRI) - Specification
permalink: /docs/cri_format/
---

**CRI-SPEC-VERSION: 1**


## Introduction

The Codeconut Runtime Information format is used to measure the amount of code executed during execution of the application.

It contains a header with format and source file specific information as well as the markers itself.

The Codeconut Runtime Information format allows the user to concatenate multiple executions in one file, adding up the marker counts.


## Data representation

### Byte order

The **Big-endian**/**network byte order** is used for the CRI-Format.


### Line break

Line breaks are made with a single byte of the value 0x0A.


## Header format

The header for the CRI format contains the following information:

- Magic number for CRI files (0x49 0x4D 0x41 0x43 0x52 0x49 0x46 0x21)
  - The magic number can be interpreted in UTF-8 to get: IMACRIF! (*I'm a Codeconut Runtime Information File!*)
- Version of the CRI-File (2 bytes wide)
- SHA-256 hash of the contents of the source code file (shall be equal to the hash stored in the respective CID file)
- Instrumentation random (shall be equal to the random value stored in the respective CID file)
- Line break (0x0A)

The header does not feature a specific length. Instead, the line break is the symbol used to define the end of the header. This allows later file revisions to add more information if that should ever be necessary.


## Marker format

A marker consists of 5 bytes:

- The first 4 bytes contain the id of the marker
- The fifth byte contains additional information that depends on the type of the marker


### Statement marker

The statement marker does not contain any additional information.


### Decision marker

The decision marker contains information, if the decision got evaluated to true or false.

- If the result was "true", the byte value is 0b10100110/0xA6.
- If the result was "false", the byte value is 0b01011001/0x59.


### Statement marker

The statement marker contains information, if the statement got evaluated to true or false.

- If the result was "true", the byte value is 0b10100110/0xA6.
- If the result was "false", the byte value is 0b01011001/0x59.


## Concatenated executions


### Checks before enabling concatenated executions

The Runtime Helper checks eventually existing files for the following information to validate, if a concatenated execution is possible:

- Equal header (magic number, CRI file version, checksum)


### New execution marker

A new execution is marked by a specific execution header. The header contains the following information:

- 5 bytes start padding (0x00 0x00 0x00 0x00 0x00)
- Magic number for new execution (0x52 0x55 0x4E 0x21)
  - The magic number can be interpreted in UTF-8 to get: *RUN!*
- The comment in UTF-8 encoded format (NULL-Terminated string)
- Comment string terminator NULL (0x00)
- A line break character (0x0A)

The execution header does not feature a specific length. Instead, the line break is the symbol used to define the end of the header. This allows later file revisions to add more information if that should ever be necessary.


### Execution-specific note

It is possible to add a note for each execution run by setting the value of the CODECONUT_EXECUTION_COMMENT define to a specific string during compilation time (passing a argument to the compiler).

### Footer after execution

After each execution, a line break (0x0A) byte has to be set at EOF.


### Disable concatenated executions

By defining CODECONUT_NO_CONCATENATED_EXECUTIONS in your source code or during compilation time, the Codeconut runtime helper won't try to append the new information into a existing coverage file, but instead force the creation of a new file (old information will be over-written).
