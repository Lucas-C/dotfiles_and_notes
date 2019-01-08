<!--Remains:
- try to import a sharedmod in the fuzzer, and check if that works in oss-fuzz Docker container
-->

### cpython

    make sharedmods && ./python.exe Lib/test/test_xxtestfuzz.py

### oss-fuzz

    python infra/helper.py build_image cpython3
    mkdir -p build/out/cpython3 build/work/cpython3
    # Last arg indicates to use local sources files instead of downloading them from GitHub
    python infra/helper.py build_fuzzers --sanitizer address cpython3 ../cpython
    python infra/helper.py check_build --sanitizer address cpython3
    python infra/helper.py run_fuzzer --sanitizer address cpython3 fuzz_builtin_eval

Example output:

    ...
    Running: /out/crash-3facf51d50ccb9dc888cff62cff3c55a13f0eb29
    =================================================================
    ==285==ERROR: AddressSanitizer: heap-buffer-overflow on address ...
    ...

<!-- This is from the oss-fuzz docs and works, but misses debug symbols:
    winpty python infra/helper.py shell base-runner-debug
    gdb --args /out/cpython3/fuzz_builtin_eval /out/cpython3/crash-3facf51d50ccb9dc888cff62cff3c55a13f0eb29

    This was a initial attempt to retrieve libfuzzer source code:
    mkdir -p compiler-rt && cd compiler-rt && git init && git remote add -f origin https://github.com/llvm-mirror/compiler-rt.git && git config core.sparseCheckout true && echo lib/fuzzer >> .git/info/sparse-checkout && git pull origin master && cd -
-->

    # Importing /src directory from gcr.io/oss-fuzz/cpython3 image to host:
    cd build && docker run --rm gcr.io/oss-fuzz/cpython3 tar cz /src | tar xz && cd -
    # Running base-runner image with /out & /src directories mounted, then installing gdb and launchint it on libfuzzer failing test case
    winpty docker run --rm -it --privileged -e FUZZING_ENGINE=libfuzzer -e SANITIZER=address -e RUN_FUZZER_MODE=interactive -v $PWD/build/out/cpython3:/out -v $PWD/build/src:/src gcr.io/oss-fuzz-base/base-runner /bin/bash
    apt install -y gdb
    gdb --args /out/fuzz_builtin_eval /out/crash-3facf51d50ccb9dc888cff62cff3c55a13f0eb29
    start
    # Setting a breakpoint on the last stack frame mentioned by the fuzzer error output
    b /src/cpython/Modules/_xxtestfuzz/fuzzer.c:79
    c

    python infra/helper.py build_fuzzers --sanitizer undefined cpython3
    python infra/helper.py check_build --sanitizer undefined cpython3
