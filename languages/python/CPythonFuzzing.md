<!--Remains:
- test undefined sanitizer
- try to import a sharedmod in the fuzzer, and check if that works in oss-fuzz Docker container
-->

### CPython

https://github.com/python/cpython/

Commands to locally build fuzzer and run Python unit tests:

    make sharedmods && ./python.exe Lib/test/test_xxtestfuzz.py

### oss-fuzz

Historical pull requests concerning CPython:

- [by Jean-PierreDevin on July 2017](https://github.com/google/oss-fuzz/pull/731)
- [by Markus Kusano on December 2018](https://github.com/google/oss-fuzz/pull/2031)

Reference docs: [New project guide - Testing locally](https://github.com/google/oss-fuzz/blob/master/docs/new_project_guide.md#testing-locally)

Commands I use to run the `address` sanitizer locally with Docker:

    python infra/helper.py build_image cpython3
    mkdir -p build/out/cpython3 build/work/cpython3
    # Last arg indicates to use local sources files instead of downloading them from GitHub
    python infra/helper.py build_fuzzers --sanitizer address cpython3 ../cpython

<!-- Manually with DEBUG=1
docker build -t gcr.io/oss-fuzz/cpython3 projects\cpython3 && docker run --rm -it --cap-add SYS_PTRACE -e FUZZING_ENGINE=libfuzzer -e SANITIZER=address -e DEBUG=1 -v %CD%\..\cpython:/src\cpython3 -v %CD%\build\out\cpython3:/out -v %CD%\build\work\cpython3:/work gcr.io/oss-fuzz/cpython3
-->

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

To understand why it fails with GDB:

    # Importing /src directory from gcr.io/oss-fuzz/cpython3 image to host (do it only once):
    cd build && docker run --rm gcr.io/oss-fuzz/cpython3 tar cz /src | tar xz && cd -
    # Running base-runner image with /out & /src directories mounted, then installing gdb and launchint it on libfuzzer failing test case
    docker run --rm -it --privileged -e FUZZING_ENGINE=libfuzzer -e SANITIZER=address -e RUN_FUZZER_MODE=interactive -v $PWD/build/out/cpython3:/out -v $PWD/build/src:/src gcr.io/oss-fuzz-base/base-runner /bin/bash
    apt install -y gdb
    gdb --args /out/fuzz_builtin_eval /out/crash-3facf51d50ccb9dc888cff62cff3c55a13f0eb29
    start
    # Setting a breakpoint on the last stack frame mentioned by the fuzzer error output
    b /src/cpython/Modules/_xxtestfuzz/fuzzer.c:79
    c
