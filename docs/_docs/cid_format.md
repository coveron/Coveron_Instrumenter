---
title: Codeconut Instrumentation Data (CID) - Specification
permalink: /docs/cid_format/
---

**CID-SPEC-VERSION: 1**


## Introduction

The Codeconut Instrumentation Data Format provides the information necessary to link the runtime output to the according source code file.

The file consists of a header and a gzip-compressed JSON object, whose structure and content details are explained in a later section.

The link between source code and runtime metrics is established by providing a dictionary that links every unique marker's ID integrated into the final source code with 1 or more elements (statements, decisions and conditions) in the uninstrumented source code and specifies the type of the marker (more info found in the documentation for the [Codeconut Runtime Information specification]({{site.baseurl}}{% link _docs/cri_format.md %})).

The file is encoded in UTF-8.

## File header

The header contains the following information:

- Magic number for CID files (0x49 0x4D 0x41 0x43 0x49 0x44 0x46 0x21)
  - The magic number can be interpreted in UTF-8 to get: IMACIDF! (*I'm a Codeconut Instrumentation Data File!*)
- Version of the CID-File (2 bytes wide)
- Line break (0x0A)

The header for the current version of the CID-Format looks like this:

```
0x49  0x4D  0x41  0x43  0x49  0x44  0x46  0x21  0x00  0x01  0x0A 
```

Opening a CID file in a editor with UTF-8 encoding results in the following output for the first line:

```
IMACIDF!\x00\x01
```


## Main file contents

The main file content is a gzip compressed string representation of a JSON object. The compression level for the gzip is not specified.

The structure of the contained JSON object is explained in the following section.


### JSON Schema for definition and validation

To define and validate the JSON object of the CID-File, the following JSON schema is used:

```json
{
    "$schema": "http://json-schema.org/draft/2019-09/schema",
    "title": "Codeconut Instrumentation Data",
    "type": "object",
    "required": ["source_code_filename", "source_code_hash", "instrumentation_random", "statement_markers_enabled", "decision_markers_enabled", "condition_markers_enabled", "marker_data"],
    "properties": {
        "source_code_filename": {
            "type": "string",
            "description": "Filename and relative path to the source code file (path is relative to the execution path of the instrumenter)",
            "pattern": "^[\\\/]*([A-z0-9-_+.]+\\\/)*([A-z0-9]+\\.([a-zA-Z+]+))$"
        },
        "source_code_hash": {
            "type": "string",
            "description": "SHA-256 hash of the data inside the source code file",
            "pattern": "^[0-9a-fA-F]{64}$"
        },
        "instrumentation_random": {
            "type": "string",
            "description": "Random 8 char string generated during instrumentation time (link to CRI file)",
            "pattern": "^[0-9a-fA-F]{8}$"
        },
        "statement_markers_enabled": {
            "type": "boolean",
            "description": "Defines, if the instrumentation includes statement markers"
        },
        "decision_markers_enabled": {
            "type": "boolean",
            "description": "Defines, if the instrumentation includes decision markers"
        },
        "condition_markers_enabled": {
            "type": "boolean",
            "description": "Defines, if the instrumentation includes condition markers"
        },
        "marker_data": {
            "type": "array",
            "description": "Array of definitions for markers",
            "minItems": 0,
            "items": {
                "type": "object",
                "required": ["marker_id", "marker_type", "code_section_data"],
                "properties": {
                    "marker_id": {
                        "type": "integer",
                        "description": "Unique id for the marker",
                        "minimum": 0
                    },
                    "marker_type": {
                        "type": "integer",
                        "description": "Type of marker",
                        "enum": [1, 2, 3]
                    },
                    "parent_id": {
                        "type": "integer",
                        "description": "marker id of a parent element (i.e. necessary for condition markers)",
                        "minimum": 0
                    },
                    "code_section_data": {
                        "type": "array",
                        "description": "Array of definitions for code sections that refer to the marker",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["start_line", "start_column", "end_line", "end_column"],
                            "properties": {
                                "start_line": {
                                    "type": "integer",
                                    "description": "Line number (starting from 1) for the start of the code section",
                                    "minimum": 1
                                },
                                "start_column": {
                                    "type": "integer",
                                    "description": "Column number (starting from 1) for the start of the code section",
                                    "minimum": 1
                                },
                                "end_line": {
                                    "type": "integer",
                                    "description": "Line number (starting from 1) for the end of the code section",
                                    "minimum": 1
                                },
                                "end_column": {
                                    "type": "integer",
                                    "description": "Column number (starting from 1) for the end of the code section",
                                    "minimum": 1
                                }
                            }
                        }
                    }
                }
            }
        },
        "markup_data": {
            "type": "array",
            "description": "Array of markup definitions (including links to relevant marker-ids)",
            "minItems": 0,
            "items": {
                "type": "object",
                "required": ["markup_id", "markup_type"],
                "properties": {
                    "markup_id": {
                        "type": "integer",
                        "description": "Unique id for the specific marker",
                        "minimum": 0
                    },
                    "markup_type": {
                        "type": "integer",
                        "description": "Type of marker",
                        "enum": [1, 2, 3, 4, 5, 6]
                    },
                    "function_markup": {
                        "type": "object",
                        "required": ["function_header_code_section", "marker_id"],
                        "properties": {
                            "function_header_code_section": {
                                "type": "object",
                                "required": ["start_line", "start_column", "end_line", "end_column"],
                                "properties": {
                                    "start_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "start_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "end_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    },
                                    "end_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    }
                                }
                            },
                            "marker_id": {
                                "type": "integer",
                                "description": "id for the related marker",
                                "minimum": 0
                            }
                        }
                    },
                    "code_block_markup": {
                        "type": "object",
                        "required": ["code_block_section", "marker_id"],
                        "properties": {
                            "code_block_section": {
                                "type": "object",
                                "required": ["start_line", "start_column", "end_line", "end_column"],
                                "properties": {
                                    "start_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "start_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "end_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    },
                                    "end_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    }
                                }
                            },
                            "marker_id": {
                                "type": "integer",
                                "description": "id for the related marker",
                                "minimum": 0
                            }
                        }
                    },
                    "if_branch_markup": {
                        "type": "object",
                        "description": "Markup info for if-branch",
                        "required": ["branch_code_section", "branches"],
                        "properties": {
                            "branch_code_section": {
                                "type": "object",
                                "required": ["start_line", "start_column", "end_line", "end_column"],
                                "properties": {
                                    "start_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "start_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "end_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    },
                                    "end_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    }
                                }
                            },
                            "branches": {
                                "type": "array",
                                "description": "Array of if-branch markups",
                                "minItems": 1,
                                "items": {
                                    "type": "object",
                                    "required": ["if_type", "header_code_section", "code_block_section", "marker_id"],
                                    "properties": {
                                        "if_type": {
                                            "type": "integer",
                                            "description": "Type of branch (1=if, 2=else if, 3=else)",
                                            "enum": [1, 2, 3]
                                        },
                                        "header_code_section": {
                                            "type": "object",
                                            "required": ["start_line", "start_column", "end_line", "end_column"],
                                            "properties": {
                                                "start_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "start_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "end_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                },
                                                "end_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                }
                                            }
                                        },
                                        "core_decision_code_section": {
                                            "type": "object",
                                            "required": ["start_line", "start_column", "end_line", "end_column"],
                                            "properties": {
                                                "start_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "start_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "end_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                },
                                                "end_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                }
                                            }
                                        },
                                        "code_block_section": {
                                            "type": "object",
                                            "required": ["start_line", "start_column", "end_line", "end_column"],
                                            "properties": {
                                                "start_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "start_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the start of the code section",
                                                    "minimum": 1
                                                },
                                                "end_line": {
                                                    "type": "integer",
                                                    "description": "Line number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                },
                                                "end_column": {
                                                    "type": "integer",
                                                    "description": "Column number (starting from 1) for the end of the code section",
                                                    "minimum": 1
                                                }
                                            }
                                        },
                                        "marker_id": {
                                            "type": "integer",
                                            "description": "id for the related marker",
                                            "minimum": 0
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "switch_branch_markup": {
                        "type": "object",
                        "description": "Markup for switch type branch",
                        "required": ["branch_code_section", "head_expression", "branches"],
                        "properties": {
                            "branch_code_section": {
                                "type": "object",
                                "required": ["start_line", "start_column", "end_line", "end_column"],
                                "properties": {
                                    "start_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "start_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the start of the code section",
                                        "minimum": 1
                                    },
                                    "end_line": {
                                        "type": "integer",
                                        "description": "Line number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    },
                                    "end_column": {
                                        "type": "integer",
                                        "description": "Column number (starting from 1) for the end of the code section",
                                        "minimum": 1
                                    }
                                }
                            },
                            ""
                        }
                    },
                    "for_loop_markup": {

                    },
                    "while_loop_markup": {

                    },
                    "do_while_loop_markup": {

                    }
                }
            }
        }
    }
}
```


### Explanatory example for the JSON object format

The JSON object has the following structure:

```json
{
    "source_code_filename": string,
    "source_code_hash": string,
    "instrumentation_random": string,
    "statement_markers_enabled": boolean,
    "decision_markers_enabled": boolean,
    "condition_markers_enabled": boolean,
    "marker_data": [
        {
            "marker_id": integer,
            "marker_type": integer,
            "parent_id": integer,
            "code_section_data": [
                {
                    "start_line": integer,
                    "start_column": integer,
                    "end_line": integer,
                    "end_column": integer
                }
            ]
        }
    ]
}
```

Detailed info on the elements inside the JSON object:

- **source_code_filename**: Filename and relative path to the source code file (path is relative to the execution path of the instrumenter)
- **source_code_hash**: SHA-256 hash of the data inside the source code file
- **instrumentation_random**: Random 8 char string to link CID and CRI files
- **statement_markers_enabled**: Defines, if the instrumentation includes statement markers
- **decision_markers_enabled**: Defines, if the instrumentation includes decision markers
- **condition_markers_enabled**: Defines, if the instrumentation includes condition markers
- **marker_data**: Array of 0-* definitions for markers
  - **marker_id**: Unique id for the marker
  - **marker_type**: Type of marker (enum is defined in a later section)
  - **parent_id**: *(optional)* marker id of a parent element (i.e. necessary for condition markers)
  - **code_section_data**: Array of 1-* definitions for code sections that refer to this marker
    - **start_line**: Line number (starting from 1) for the start of the code section
    - **start_column**: Column number (starting from 1) for the start of the code section
    - **end_line**: Line number (starting from 1) for the end of the code section
    - **end_column**: Column number (starting from 1) for the end of the code section


### Marker type enum

The enum for the marker type can have the following values:

1. STATEMENT
2. DECISION
3. CONDITION