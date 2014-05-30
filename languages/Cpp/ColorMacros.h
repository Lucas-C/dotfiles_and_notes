/*!
    @file ColorMacros.h
    @brief C/C++ preprocessor macros to color strings
    Because of __VA_ARGS__ this requires -std=c99 or -std=c++0x
    @author CIMON Lucas
    @date 2014
*/
#ifndef _DEF_H_ColorMacros
#define _DEF_H_ColorMacros

/*!
 UNIX colors "\033[3"_c_"m" :
    _c_ = 0 => black
    _c_ = 1 => red
    _c_ = 2 => green
    _c_ = 3 => yellow
    _c_ = 4 => dark blue
    _c_ = 5 => purple
    _c_ = 6 => soft blue
    _c_ = 7 => grey
WINDOWS colors "0x??" :
    bit 0 => foreground intensity
    bit 1 => foreground red
    bit 2 => foreground green
    bit 3 => foreground blue
    bit 4 => background intensity
    bit 5 => background red
    bit 6 => background green
    bit 7 => background blue
 */
#if defined(__unix__)
    #define RED_COLOR        "\033[31m"
    #define GREEN_COLOR    "\033[32m"
    #define YELLOW_COLOR    "\033[33m"
    #define BLUE_COLOR    "\033[34m"
    #define END_COLOR        "\033[0m"
#elif defined(WIN32)
    #define RED_COLOR        0x0C
    #define GREEN_COLOR    0x02
    #define YELLOW_COLOR    0x06
    #define BLUE_COLOR    0x01
    #define END_COLOR        0x07
#endif

/*!
    @def STDERR_STRM, STDOUT_STRM, PRINT_TO_STRM
*/
#ifdef __cplusplus
    #include <cstdlib>
    #include <iostream>
    #include <fstream>
    #define STDERR_STRM std::cerr
    #define STDOUT_STRM std::cout
    #define OPEN_STRM(new_strm_varname, filename)   std::ofstream new_strm_varname(filename, std::ofstream::app)
    #define PRINT_TO_STRM(strm_desc, ...)           strm_desc << __VA_ARGS__
    #define CLOSE_STRM(strm_desc)
#else
    #include <stdlib.h>
    #include <stdio.h>
    #define STDERR_STRM stderr
    #define STDOUT_STRM stdout
    #define OPEN_STRM(new_strm_varname, filename)   FILE* new_strm_varname = fopen(filename, "a+")
    #define PRINT_TO_STRM(strm_desc, ...)           fprintf(strm_desc, __VA_ARGS__)
    #define CLOSE_STRM(strm_desc)                   fclose(strm_desc)
#endif

/*!
    @def COLOR_STRM
    @brief Turn on/off colored output for an ostream.
    "color" parameters : RED GREEN YELLOW BLUE END.
*/
#if defined(WIN32)
    #define WIN32_LEAN_AND_MEAN // Reduce the size of the Win32 header files.
    #define VC_EXTRALEAN // Ditto, for Visual C++
    #include <windows.h>
    #define GET_WIN32_HANDLE(strm_desc)     ( (strm_desc == SDERR_STRM) ? GetStdHandle( STD_ERROR_HANDLE ) : GetStdHandle( STD_OUTPUT_HANDLE ) )
    #define COLOR_STRM(strm_desc, color)    SetConsoleTextAttribute(GET_WIN32_HANDLE(strm_desc), color)
#else
    #define COLOR_STRM                      PRINT_TO_STRM
#endif

/*!
    @def COLOR_STRM_STRING(strm, color, string)
    @brief Put a colored text in a specified file descriptor or ostream, on Linux or Windows.
    Available colors : RED/GREEN/YELLOW/BLUE_COLOR
*/
#define COLOR_STRM_STRING(strm_desc, color, ...) \
    do {\
        COLOR_STRM(strm_desc, color);\
        PRINT_TO_STRM(strm_desc, __VA_ARGS__);\
        COLOR_STRM(strm_desc, END_COLOR);\
    } while (0)

#endif // _DEF_H_ColorMacros
