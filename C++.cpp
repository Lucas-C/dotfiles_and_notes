// Basic exception
throw runtime_error("invalid type");
// Catching bad_alloc
try {
    obj = new Object;
} catch(std::bad_alloc &e) {
    std::cerr << "oom " << e.what() << std::endl;
    throw;
}

// GCC optimization
if(__builtin_expect(entity->extremely_unlikely_flag,0))
    // code that is rarely run

// POGO

// Windows code analysis
cl /analyze
