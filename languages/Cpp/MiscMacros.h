/*!
    @file Macros.h
    @brief Useful C/C++ preprocessor macros
    @author CIMON Lucas
    @date 2010
*/
#ifndef _DEF_H_MiscMacros
#define _DEF_H_MiscMacros

/*!
    @def DO_PRAGMA(x)
    @brief Apply a compiler pragma
 */
#define DO_PRAGMA(pragma)        _Pragma (#pragma)

/*!
    @def TODO(string)
    @brief Track the compilation and print TODO messages, deactivated by defining NOTODO
 */
#ifdef NOTODO
    #define TODO(string)
#else
    #define TODO(string)    DO_PRAGMA(message ("TODO - " string))
#endif


#ifdef __cplusplus

/*!
    @def DISALLOW_COPY_AND_ASSIGN(TypeName)
    @brief A macro to disallow the copy constructor and operator= functions.
    This should be used in the private: declarations for a class
    FROM: http://google-styleguide.googlecode.com/svn/trunk/cppguide.xml
*/
#define DISALLOW_COPY_AND_ASSIGN(TypeName)\
  TypeName(const TypeName&);              \
  void operator=(const TypeName&)

/*!
    @def FOREACH_IT(stl_iterator, container, var)
    @brief A macro to loop through every standard STL container.
    The container need to have an operator++(), begin() & end() members.
*/
#define FOREACH_IT(stl_iterator, container, var)\
    for (std::stl_iterator (var) = (container).begin();\
    (var) != (container).end();\
    ++(var))

/*!
    @def FOREACH(stl_type, container, var)
    @brief FOREACH_IT specialisation for containers with an \b iterator typedef.
*/
#define FOREACH(stl_type, container, var) FOREACH_IT(stl_type::iterator, container, var)

/*!
    @def FOREACH_C(stl_type, container, var)
    @brief FOREACH_IT specialisation for containers with an \b const_iterator typedef.
*/
#define FOREACH_C(stl_type, container, var) FOREACH_IT(stl_type::const_iterator, container, var)

#endif // __cplusplus

#endif // _DEF_H_MiscMacros
