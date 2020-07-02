#include <stdint.h>

// Dummy function
int dummy() { return 10; }
int dummy2() { return 1; }

// Test if-branch
int IfTest(int arg1, int arg2, int arg3[]) {
    // Demo-Kommentar

    int value = 0;

    if (arg1 > arg2) {
        return 1;
    } else if (dummy() == arg2) {
        return 2;
    } else if (dummy2()) {
        return 3;
    } else if ((dummy() < 10 ? 1 : 0) && arg1 > 0) {
        // ternary
        return 4;
    } else if (arg1 < -100 || (arg1 > 5 && arg2<10) || arg2 == 10) {
    } else if ((value = dummy())) {
        // assignment inside evaluation
    } else {
        return 10;
    }

    return 0;
}

// Test switch-branch
int SwitchTest(int arg1) {
    int a = 0;
    switch (arg1) {
        case 0:
            a = 10;
            break;
        case 2:
            a = 5;
        case 3:
            a++;
            break;
        case 4:
        case 5:
            a = 100;
            break;
        default:
        case 10:
            a = 1;
            break;
    }
    return a;
}

// Test for-loop
int ForLoopTest(int arg1, int arg2) {
    int run_var = 0;

    for (int i = 0;i < 20;i++) {
        if (i > arg1) {
            continue;
        }
        if (i > arg2) {
            break;
        }
        run_var += i;
    }

    return run_var;
}

// Test while-loop
int WhileTest(int arg1) {
    int run_var = 0;

    while (run_var < arg1) {
        run_var++;
        run_var = run_var * run_var;
    }

    return run_var;
}

// Test do-while-loop
int DoWhileTest(int arg1) {
    int run_var = 0;

    do {
        run_var++;
        run_var = run_var * run_var;
    } while (run_var < arg1 || run_var > 5);

    return run_var;
}

// Test goto
void GotoTest() {
    goto hello;
    int a = 0;
hello:
    a++;
    int b = 5;
}

// Decision test
int DecisionTest(int arg1, int arg2, int arg3, int arg4) {
    if (arg1 > arg2 || arg3 < 4 || ((arg1 + arg2) >= arg3 && arg4 > 0) && arg1 >= 5) {
        return 10;
    }

    return 0;
}

// Ternary Expression test
int TernaryTest(int arg1, int arg2) {
    int a = arg1 > arg2 ? dummy() : 0;
    return a;
}

// Test all kinds of statements
int StatementTest() {
    // Setup variable
    int a = 0;

    // Increase with a++
    a++;

    // Increase with a += 2
    a += 2;

    // Assignment with a = 3
    a = 3;

    // Assignment with a =+ 4
    a = +4;

    return a;
}

// dummy main function
int main() {
    //let's just do nothing
    return 0;
}