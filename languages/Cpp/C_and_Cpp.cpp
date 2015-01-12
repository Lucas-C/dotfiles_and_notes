gcc -g3 -D_DEBUG -Wall -Wextra -pedantic-errors -Wfloat-equal -Wconversion -Wshadow -Weffc++ # -pg -fstack-protector
-fsanitize=thread -fPIE -pie -g // dynamic ThreadSanitizer
-fsanitize=memory -fPIE -pie -g // dynamic MemorySanitizer
-fsanitize=address -O1 -fno-omit-frame-pointer -g // dynamic AddressSanitizer
valgrind --leak-check=full --track-origins=yes // seemingly > purify
gperftools: -ltcmalloc, HEAPCHECK, HEAPPROFILE, pprof // thread-caching malloc, heap checker/profiler, CPU profiler
plasma-umass/coz // a profiler spotted by jmason
GNU complexity // Alternative to pmccabe to evaluate code complexity
indent // GNU C source beautifier

re2c // tool generating fast code for regular expressions matching
gperf // GNU Perfect Hash Function Generator - http://www.ibm.com/developerworks/library/l-gperf/

tcc, cling, ccons // C interpreters

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

jemalloc > alloca > malloc
stdlib 'realloc' : change the size of an already allocated memory block

mmap // File in memomry mapping, to optimize paging operations
// GOTCHAS: https://bugzilla.mozilla.org/show_bug.cgi?id=1015957#c2

#include <dirent.h> // opendir/closedir, readdir, telldir, rewinddir, seekdir

goto // http://stackoverflow.com/a/2809622 - Edsger Dijkstra's "GoTo Considered Harmful" oftens doesn't apply


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
²// Catching bad_alloc
try {
    obj = new Object;
} catch(std::bad_alloc &e) {
    std::cerr << "oom " << e.what() << std::endl;
    throw;
}

// Pattern from AOSA chapter on LLVM: http://aosabook.org/en/llvm.html
class MyClass : public MyParent { ... }
MyParent *createMyClass() { return new MyClass(); } // Benefits: can easily migrate to custom memory allocation / singleton later on

// Pitfalls
Derived d;
static_cast<Base>(d).foo() // the cast create a tmp obj, so foo() won't be called on d

// Parameter passing optimization: http://www.drdobbs.com/cpp/some-optimizations-are-more-important-th/240159684
string rev(string&& s) { reverse(s.begin(), s.end()); return s; }
// -> compiler will choose this one if the argument is an rvalue, which will reverse that rvalue in place
string rev(const string& s) { string t = s; reverse(t.begin(), t.end()); return t; }
// -> compiler will choose this one if the argument might be used again later, which will safely copy the string's characters

http://en.wikipedia.org/wiki/Streaming_SIMD_Extensions // SSE, MMX high performance instructions, e.g. prefetching with dcbt

3rdparty/stout // includes Option, Result, Stopwatch, Try
folly::fbvector > std::vector + other useful libs in facebook/folly // https://github.com/facebook/folly/blob/master/folly/docs/Overview.md

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

// POGO: Profile Guided Optimizations : optimization is done offline, based on profiling information, but once the binary is shipped there is no ongoing optimization, != JIT runtime optimization
// This is a general technic, but provided by Visual Studio (+ Mpgo.exe & Ngen.exe)
Nana C++ // GUI programming
GNU Nana // assertion checking, logging and performance measurement

// Logging: g2log > glog > log4c (!! memory eater)

// MinGW: http://lynix.digitalpulsesoftware.com/2010/06/gcc-4-4-0-sous-windows-avec-mingw/

cl /analyze // Visual Studio code analysis: http://www.altdev.co/2011/12/24/static-code-analysis/ (John Carmack)
