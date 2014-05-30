/*!
    @file DebugMacros.h
    @brief C/C++ preprocessor macros for tracing/asserting
    Because of __VA_ARGS__ this requires -std=c99 or -std=c++0x
    @author CIMON Lucas
    @date 2014
*/
#ifndef _DEF_H_DebugMacros
#define _DEF_H_DebugMacros

#include "ColorMacros.h"

/*!
    @def TRACE(string)
 */
#define TRACE(...)         COLOR_STRM_STRING(STDOUT_STRM, YELLOW_COLOR, __VA_ARGS__)

/*!
    @def SHOW_ERROR(string)
 */
#define SHOW_ERROR(...)        COLOR_STRM_STRING(STDERR_STRM, RED_COLOR, __VA_ARGS__)

/*!
    @def DBG(string)
    @brief Debug track of the execution. Deactivated by defining NODBG.
 */
#ifdef NODBG
    #define DBG(...)
#else
    #define DBG(...)     COLOR_STRM_STRING(STDERR_STRM, GREEN_COLOR, __VA_ARGS__)
#endif

/*!
    @def DBG_ONCE(string)
    @brief Debug track of the execution. Printed only once. Deactivated by defining NODBG.
 */
#define DBG_ONCE(...)\
    do {\
        static int once = 0;\
        if (once) {\
            DBG(__VA_ARGS__);\
            once = 1;\
        }\
    } while(0)

/*!
    @def DUMP(filename, ...)
    @brief Debug macro, very useful with 'tail -f'. Need C99 support.
 */
#define DUMP(filename, ...)\
    if (filename) {\
        static OPEN_STRM(strm_desc, filename);\
        PRINT_TO_STRM(strm_desc, __VA_ARGS__)\
        CLOSE_STRM(strm_desc);\
    }

/*!
    @def CHECK_INT(expected, expression)
    @brief Assertion with rich colored error message
    FROM: "The Pragmatic Programmer" by Hunt & Thomas
 */
#define CHECK_INT(expected, expression) {\
    int result = (expression);\
    if (result != (expected)) {\
        abort_check_int(__FILE__, __LINE__, #expression, result, expected);\
    }\
}

void abort_check_int(const char* filename, int line, const char* expression, int result, int expected) {
    char error_msg[256];
    sprintf(error_msg, "%s line %d : '%s' is evaluating to %d, but %d was expected\n",
            filename, line, expression, result, expected);
    SHOW_ERROR(error_msg);
    exit(42);
}

#endif // _DEF_H_DebugMacros
