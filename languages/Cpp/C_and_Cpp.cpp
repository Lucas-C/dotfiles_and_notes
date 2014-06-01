gcc -g3 -D_DEBUG -Wall -Wextra -pedantic-errors -Wfloat-equal -Wconversion -Wshadow -Weffc++ # -pg -fstack-protector
gcc -dM -E </dev/null // dump the list of predefined macros; e.g. unix & linux

// Use ‘const’ as much as possible.
const int *p;           // pointer to const int
int * const p;          // const pointer to int
const int * const p;    // const pointer to const int
// Don’t use:
int const *p;

// GCC optimization
if(__builtin_expect(entity->extremely_unlikely_flag,0))
    // code that is rarely run

#include "errno.h"
if (errno == EACCES) // or e.g. when an 'open' function return NULL
    perror("Acces to STUFF forbidden : ")

alloca > malloc
stdlib 'realloc' : change the size of an already allocated memory block

mmap // File in memomry mapping, to optimize paging operations
// GOTCHAS: https://bugzilla.mozilla.org/show_bug.cgi?id=1015957#c2

#include <dirent.h> // opendir/closedir, readdir, telldir, rewinddir, seekdir


////////////
// C only
///////////
int main(void); // C standard to use void to indicate no parameters
// + program should end with a newline following C standard

// Interview test
int a=41; a++; printf("%d\n", a); // 42
int a=41; a++ & printf("%d\n", a); // undefined
int a=41; a++ && printf("%d\n", a); // 42
int a=41; if (a++ < 42) printf("%d\n", a); // 42
int a=41; a = a++; printf("%d\n", a); // undefined


/***********/
// C++ only
/**********/

// "Rule of three"
#define DISALLOW_COPY_AND_ASSIGN(TypeName) TypeName(const TypeName&); void operator=(const TypeName&)

// Basic exception
throw runtime_error("invalid type");
// Catching bad_alloc
try {
    obj = new Object;
} catch(std::bad_alloc &e) {
    std::cerr << "oom " << e.what() << std::endl;
    throw;
}

// Pitfalls
Derived d;
static_cast<Base>(d).foo() // the cast create a tmp obj, so foo() won't be called on d

// Parameter passing optimization: http://www.drdobbs.com/cpp/some-optimizations-are-more-important-th/240159684
string rev(string&& s) { reverse(s.begin(), s.end()); return s; }
// -> compiler will choose this one if the argument is an rvalue, which will reverse that rvalue in place
string rev(const string& s) { string t = s; reverse(t.begin(), t.end()); return t; }
// -> compiler will choose this one if the argument might be used again later, which will safely copy the string's characters

// NVWA:
  * boolarray.h
  * class_level_lock.h
  * cont_ptr_utils.h
  * debug_new.h
  * fast_mutex.h
  * fixed_mem_pool.h
  * mem_pool_base.h
  * object_level_lock.h
  * pctimer.h
  * set_assign.h
  * static_mem_pool.h

// POGO: Profile Guided Optimizations
Nana // GUI programming

// Logging: g2log > glog > log4c (!! memory eater)

// MinGW: http://lynix.digitalpulsesoftware.com/2010/06/gcc-4-4-0-sous-windows-avec-mingw/

cl /analyze // Visual Studio code analysis
