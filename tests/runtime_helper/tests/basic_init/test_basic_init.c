#include "codeconut_helper.h"
#include "unity.h"

#include "mock_fake_stdio.h"

___CODECONUT_FILE_T testInputData1 = {{
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                      },
                                      {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
                                      ___CODECONUT_BOOL_FALSE,
                                      NULL,
                                      "test_output.cri"};

const ___CODECONUT_FILE_T original_testInputData1 = {
    {
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    },
    {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
    ___CODECONUT_BOOL_FALSE,
    NULL,
    "test_output.cri"};

void test_basic_init_1(void) {
    ___CODECONUT_SET_STATEMENT_MARKER(0, 0, 0, 0, &testInputData1);
    return;
}
