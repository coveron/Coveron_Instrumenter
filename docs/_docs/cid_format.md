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
    "title": "Codeconut Instrumentation Data"
    "required": ["source_code_filename", "source_code_hash", "instrumentation_random", "statement_markers_enabled", "decision_markers_enabled", "condition_markers_enabled", "marker_data", "code_data"],
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
        "checkpoint_markers_enabled": {
            "type": "boolean",
            "description": "Defines, if the instrumentation includes checkpoint markers"
        },
        "evaluation_markers_enabled": {
            "type": "boolean",
            "description": "Defines, if the instrumentation includes evaluation markers"
        },
        "marker_data": {
            "type": "object",
            "description": "Marker definitions",
            "required": ["checkpoint_markers", "evaluation_markers"],
            "properties": {
                "checkpoint_markers": {
                    "type": "array",
                    "description": "List of all Checkpoint markers used during the instrumentation process",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Checkpoint marker info",
                        "required": ["checkpoint_marker_id", "code_position"],
                        "properties": {
                            "checkpoint_marker_id": {
                                "type": "integer",
                                "description": "Checkpoint Marker ID",
                                "minimum": 0
                            },
                            "code_position": {
                                "type": "object",
                                "description": "Checkpoint code position",
                                "required": ["line", "column"],
                                "properties": {
                                    "line": {
                                        "type": "integer",
                                        "description": "line position in code",
                                        "minimum": 1
                                    },
                                    "column": {
                                        "type": "integer",
                                        "description": "column position in code",
                                        "minimum": 1
                                    }
                                }
                            }
                        }
                    }
                },
                "evaluation_markers": {
                    "type": "array",
                    "description": "List of all Evaluation markers used during the instrumentation process",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Evaluation marker description",
                        "required": ["evaluation_marker_id", "evaluation_type", "code_section"],
                        "properties": {
                            "evaluation_marker_id": {
                                "type": "integer",
                                "description": "Checkpoint Marker ID",
                                "minimum": 0
                            },
                            "evaluation_type": {
                                "type": "integer",
                                "description": "Checkpoint marker type (1=decision, 2=condition)"
                            },
                            "code_section": {
                                "type": "object",
                                "description": "Code section of the evaluation marker",
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
            }
        },
        "code_data": {
            "type": "object",
            "description": "Code data dictionary",
            "required": ["classes", "functions", "statements", "if_branches", "switch_branches", "loops"],
            "properties": {
                "classes": {
                    "type": "array",
                    "description": "List of all found classes",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Class description object",
                        "required": ["class_id", "class_name"],
                        "properties": {
                            "class_id": {
                                "type": "integer",
                                "description": "Unique ID for the specific class"
                            },
                            "class_name": {
                                "type": "string",
                                "description": "Name of the class"
                            }
                        }
                    }
                },
                "functions": {
                    "type": "array",
                    "description": "List of all found functions",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Function description object",
                        "required": ["function_id", "function_name", "checkpoint_marker_id", "header_code_section", "inner_code_section"],
                        "properties": {
                            "function_id": {
                                "type": "integer",
                                "description": "Unique ID for the specific function"
                            },
                            "function_name": {
                                "type": "string",
                                "description": "Name of the function"
                            },
                            "checkpoint_marker_id": {
                                "type": "integer",
                                "description": "ID of the correlating checkpoint marker"
                            },
                            "header_code_section": {
                                "type": "object",
                                "description": "Code section of the function header",
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
                            "inner_code_section": {
                                "type": "object",
                                "description": "Code section of the function body",
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
                },
                "statements": {
                    "type": "array",
                    "description": "List of all found statements",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Statement description object",
                        "required": ["statement_id", "statement_type", "function_id", "checkpoint_marker_id", "code_section"],
                        "properties": {
                            "statement_id": {
                                "type": "integer",
                                "description": "ID of the specific statement",
                            },
                            "statement_type": {
                                "type": "integer",
                                "description": "Type of the statement (see rest of docs)",
                                "enum": [1, 2, 3, 4, 5]
                            },
                            "function_id": {
                                "type": "integer",
                                "description": "ID of the parent function"
                            },
                            "checkpoint_marker_id": {
                                "type": "integer",
                                "description": "ID of the correlating checkpoint marker"
                            },
                            "code_section": {
                                "type": "object",
                                "description": "Code section of the function body",
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
                },
                "if_branches": {
                    "type": "array",
                    "description": "List of if-type branches",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "If branch description object",
                        "required": ["if_branch_id", "function_id", "branch_results"],
                        "properties": {
                            "if_branch_id": {
                                "type": "integer",
                                "description": "Unique id for the branch"
                            },
                            "function_id": {
                                "type": "integer",
                                "description": "ID of the parent function"
                            },
                            "branch_results": {
                                "type": "array",
                                "description": "List of all branches of the if-branch",
                                "minItems": 1,
                                "items": {
                                    "type": "object",
                                    "description": "If branch result description",
                                    "required": ["evaluation_marker_id", "conditions", "result_evaluation_code_section", "result_body_code_section"],
                                    "properties": {
                                        "evaluation_marker_id": {
                                            "type": "integer",
                                            "description": "ID of the evaluation marker for the decision"
                                        },
                                        "conditions": {
                                            "type": "array",
                                            "description": "Array of contained conditions",
                                            "minItems": 0,
                                            "items": {
                                                "type": "object",
                                                "description": "Condition description",
                                                "required": ["evaluation_marker_id", "code_section"],
                                                "properties": {
                                                    "evaluation_marker_id": {
                                                        "type": "integer",
                                                        "description": "ID of the evaluation marker for the condition"
                                                    },
                                                    "code_section": {
                                                        "type": "object",
                                                        "description": "Code section of the function body",
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
                                        },
                                        "result_evaluation_code_section": {
                                            "type": "object",
                                            "description": "Code section of the result evaluation",
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
                                        "result_body_code_section": {
                                            "type": "object",
                                            "description": "Code section of the result body",
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
                        }
                    }
                },
                "switch_branches": {
                    "type": "array",
                    "description": "List of switch-type branches",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Switch branch description",
                        "required": ["switch_branch_id", "expression_code_section", "cases"],
                        "properties": {
                            "switch_branch_id": {
                                "type": "integer",
                                "description": "Unique ID for the switch branch",
                            },
                            "function_id": {
                                "type": "integer",
                                "description": "ID of the parent function"
                            },
                            "expression_code_section": {
                                "type": "object",
                                "description": "Code section of the switch expression",
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
                            "cases": {
                                "type": "array",
                                "description": "List of possible switch cases",
                                "minItems": 0,
                                "items": {
                                    "type": "object",
                                    "description": "Switch case description",
                                    "required": ["execution_marker_id", "case_type", "evaluation_code_section", "body_code_section"],
                                    "properties": {
                                        "checkpoint_marker_id": {
                                            "type": "integer",
                                            "description": "ID of the according checkpoint marker"
                                        },
                                        "case_type": {
                                            "type": "integer",
                                            "description": "case type (1=normal case, 2=default case)",
                                            "enum": [1, 2]
                                        },
                                        "evaluation_code_section": {
                                            "type": "object",
                                            "description": "Code section of the switch expression",
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
                                        "body_code_section": {
                                            "type": "object",
                                            "description": "Code section of the switch expression",
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
                        }
                    }
                },
                "loops": {
                    "type": "array",
                    "description": "List of all loops",
                    "minItems": 0,
                    "items": {
                        "type": "object",
                        "description": "Loop description",
                        "required": ["loop_id", "loop_type", "evaluation_marker_id", "evaluation_code_section", "body_code_section", "conditions"],
                        "properties": {
                            "loop_id": {
                                "type": "integer",
                                "description": "Unique ID for the loop"
                            },
                            "loop_type": {
                                "type": "integer",
                                "description": "Type of the loop (1=for, 2=while, 3=do-while)",
                                "enum": [1, 2, 3]
                            },
                            "function_id": {
                                "type": "integer",
                                "description": "ID of the parent function"
                            },
                            "evaluation_marker_id": {
                                "type": "integer",
                                "description": "ID of the according evaluation marker",
                            },
                            "evaluation_code_section": {
                                "type": "object",
                                "description": "Code section of the loop evaluation",
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
                            "body_code_section": {
                                "type": "object",
                                "description": "Code section of the loop body",
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
                            "conditions": {
                                "type": "array",
                                "description": "List of loop evaluation conditions",
                                "minItems": 0,
                                "items": {
                                    "type": "object",
                                    "description": "For loop evaluation condition description",
                                    "required": ["evaluation_marker_id", "code_section"],
                                    "properties": {
                                        "evaluation_marker_id": {
                                            "type": "integer",
                                            "description": "ID of the according evaluation marker",
                                        },
                                        "code_section": {
                                        "type": "object",
                                        "description": "Code section of the condition",
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
                    }
                }
            }
        }
    }
}
```

Detailed info on the elements inside the JSON object:

- **source_code_filename**: Filename and relative path to the source code file (path is relative to the execution path of the instrumenter)
- **source_code_hash**: SHA-256 hash of the data inside the source code file
- **instrumentation_random**: Random 8 char string to link CID and CRI files
- **checkpoint_markers_enabled**: Defines, if the instrumentation includes checkpoint markers
- **evaluation_markers_enabled**: Defines, if the instrumentation includes evaluation markers
- **marker_data**: Object with definitions for markers
  - **checkpoint_markers**: Array with definition for checkpoint markers
    - **checkpoint_marker_id**: Unique ID for checkpoint markers
    - **code_position**: Position of the marker in code
      - **line**: Line of code position
      - **column**: Column of code position
  - **evaluation_markers**: Array with definition for evaluation markers
    - **evaluation_marker_id**: Unique ID for evaluation markers
    - **evaluation_type**: Type of the evaluation (enum, 1=decision, 2=condition)
    - **code_section**: Code section for the evaluation
      - **start_line**: Line number (starting from 1) for the start of the code section
      - **start_column**: Column number (starting from 1) for the start of the code section
      - **end_line**: Line number (starting from 1) for the end of the code section
      - **end_column**: Column number (starting from 1) for the end of the code section
  - **code_data**: Object with data for code components
    - **classes**: Array with all classes inside of the parsed code
      - **class_id**: Unique ID for the class
      - **class_name**: Name of the class
    - **functions**: Array with all functions inside of the parsed code
      - **function_id**: Unique ID for the function
      - **function_name**: Name of the function
      - **function_type**: Type of the function (enum, definition below)
      - **parent_function_id**: ID of the parent function (-1 if no parent function)
      - **checkpoint_marker_id**: ID of the according checkpoint marker for execution evaluation
      - **header_code_section**: Code section for the function header (_type name(args)_)
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
      - **inner_code_section"**: Code section for the function body
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
    - **statements**: Array with all statements inside of the parsed code
      - **statement_id**: Unique ID for the statement
      - **statement_type**: Type of the statement (enums, defined below)
      - **function_id**: ID of the parent function
      - **checkpoint_marker_id**: ID of the according checkpoint marker for execution evaluation
      - **code_section**: Code section of the statement
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
    - **if_branches**: Array with all if branches inside of the parsed code
      - **if_branch_id**: Unique ID for the branch
      - **function_id**: ID of the parent function
      - **branch_results**: Array with list of all possible branch results
        - **evaluation_marker_id**: Unique ID for the evaluation marker
        - **conditions**: Array of conditions inside the decision
          - **evaluation_marker_id**: ID of the according evaluation marker
          - **code_section**: Code section for the condition
            - **start_line**: Line number (starting from 1) for the start of the code section
            - **start_column**: Column number (starting from 1) for the start of the code section
            - **end_line**: Line number (starting from 1) for the end of the code section
            - **end_column**: Column number (starting from 1) for the end of the code section
        - **result_evaluation_code_section**: Code section of evaluation
          - **start_line**: Line number (starting from 1) for the start of the code section
          - **start_column**: Column number (starting from 1) for the start of the code section
          - **end_line**: Line number (starting from 1) for the end of the code section
          - **end_column**: Column number (starting from 1) for the end of the code section
        - **result_body_code_section**: Code section of result code body
          - **start_line**: Line number (starting from 1) for the start of the code section
          - **start_column**: Column number (starting from 1) for the start of the code section
          - **end_line**: Line number (starting from 1) for the end of the code section
          - **end_column**: Column number (starting from 1) for the end of the code section
    - **switch_branches**: Array with all switch branches inside of the parsed code
      - **switch_branch_id**: Unique ID for the switch branch
      - **function_id**: ID of the parent function
      - **expression_code_section**: Code section of the evaluated switch expression
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
      - **cases**: Array of cases inside the switch branch
        - **checkpoint_marker_id**: Unique ID for the according checkpoint marker
        - **case_type**: Type of the case (enum, 1=normal case, 2=default case)
        - **evaluation_code_section**: Code section of the evaluation
          - **start_line**: Line number (starting from 1) for the start of the code section
          - **start_column**: Column number (starting from 1) for the start of the code section
          - **end_line**: Line number (starting from 1) for the end of the code section
          - **end_column**: Column number (starting from 1) for the end of the code section
        - **body_code_section**: Code section of the code body
          - **start_line**: Line number (starting from 1) for the start of the code section
          - **start_column**: Column number (starting from 1) for the start of the code section
          - **end_line**: Line number (starting from 1) for the end of the code section
          - **end_column**: Column number (starting from 1) for the end of the code section
    - **loops**: Array with all loops inside of the parsed code
      - **loop_id**: Unique ID for the loop
      - **loop_type**: Loop type (enum, 1=for, 2=while, 3=do-while)
      - **function_id**: ID of the parent function
      - **evaluation_marker_id**: ID of the according evaluation marker
      - **evaluation_code_section**: Code section of the evaluation
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
      - **body_code_section**: Code section of the loop body
        - **start_line**: Line number (starting from 1) for the start of the code section
        - **start_column**: Column number (starting from 1) for the start of the code section
        - **end_line**: Line number (starting from 1) for the end of the code section
        - **end_column**: Column number (starting from 1) for the end of the code section
      - **conditions**: Array of conditions inside the decision
        - **evaluation_marker_id**: ID of the according evaluation marker
        - **code_section**: Code section for the condition
          - **start_line**: Line number (starting from 1) for the start of the code section
          - **start_column**: Column number (starting from 1) for the start of the code section
          - **end_line**: Line number (starting from 1) for the end of the code section
          - **end_column**: Column number (starting from 1) for the end of the code section


### Function type enum

The enum for the function type

1. NORMAL
2. CONSTRUCTOR
3. DESTRUCTOR

### Statement type enum

The enum for the statement type can have the following values:

1. STATEMENT
2. DECISION
3. CONDITION
4. CASE-DECISION