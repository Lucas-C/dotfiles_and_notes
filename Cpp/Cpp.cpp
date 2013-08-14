// Basic exception
throw runtime_error("invalid type");
// Catching bad_alloc
try {
    obj = new Object;
} catch(std::bad_alloc &e) {
    std::cerr << "oom " << e.what() << std::endl;
    throw;
}

// Parameter passing optimization: http://www.drdobbs.com/cpp/some-optimizations-are-more-important-th/240159684
string rev(string&& s) { reverse(s.begin(), s.end()); return s; }
// -> compiler will choose this one if the argument is an rvalue, which will reverse that rvalue in place
string rev(const string& s) { string t = s; reverse(t.begin(), t.end()); return t; }
// -> compiler will choose this one if the argument might be used again later, which will safely copy the string's characters

// GCC optimization
if(__builtin_expect(entity->extremely_unlikely_flag,0))
    // code that is rarely run

// POGO

// Windows code analysis
cl /analyze
