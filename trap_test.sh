#!/bin/bash

# TODO:
#- generate a cmds / signals caught grid
#- implement a trap stack, based on calling function name (using 'caller')
#- add checks to the lib to verify consistent usage, i.e. not other calls to 'trap' are made before/in-between
#- make the lib 'set -eux' proof
#- do extra script checking if sourced with the script name as a parameter $(readlink -f $0) : grep '[A-Za-z0-9]exec '

# Garbage cleaner proto
garbage_cleaner () { # USAGE: eval $(garbage_cleaner cleanup_func)
    echo trap "'"err_code=\$? \; trap - RETURN EXIT INT TERM HUP QUIT \; $@ \; \$\(exit \$err_code\)"'" RETURN EXIT INT TERM HUP QUIT
}
example () {
    cleanup () { echo CLEANUP ; rm $file ; } # variables will be accesible as this will be called before leaving the function
    eval $(garbage_cleaner cleanup)
    local file=$(mktemp)
    sleep 5
}
# Pros: self-sufficient: no need to untrap, or call the cleanup function at the end of the function its defined
# Cons: cannot be nested, 'set -o nounset' trapped warnings can trigger multiple cleanup : this function MUST be robust
# BIG CON: 'nounset' trigger an EXIT, and there is no way to make a distinction based on $err_code to distinguish between normal & erroneous terminations

trap 'e=$? ; trap - HUP ; echo "HUP - ERR_CODE:$e"; $(exit $e)' HUP
trap 'e=$? ; trap - INT ; echo "INT - ERR_CODE:$e"; $(exit $e)' INT
trap 'e=$? ; trap - QUIT ; echo "QUIT - ERR_CODE:$e"; $(exit $e)' QUIT
trap 'e=$? ; trap - ILL ; echo "ILL - ERR_CODE:$e"; $(exit $e)' ILL
trap 'e=$? ; trap - TRAP ; echo "TRAP - ERR_CODE:$e"; $(exit $e)' TRAP
trap 'e=$? ; trap - ABRT ; echo "ABRT - ERR_CODE:$e"; $(exit $e)' ABRT
trap 'e=$? ; trap - KILL ; echo "KILL - ERR_CODE:$e"; $(exit $e)' KILL
# There is no much point in catching Bash segfault. This won't catch e.g. a C program segfault (see commented tests below)
# trap 'e=$? ; trap - SEGV ; echo "SEGV - ERR_CODE:$e"; $(exit $e)' SEGV
trap 'e=$? ; trap - CONT ; echo "CONT - ERR_CODE:$e"; $(exit $e)' CONT
trap 'e=$? ; trap - STOP ; echo "STOP - ERR_CODE:$e"; $(exit $e)' STOP
#trap 'e=$? ; trap - DEBUG ; echo "DEBUG - ERR_CODE:$e"; $(exit $e)' DEBUG
trap 'e=$? ; trap - ERR ; echo "ERR - ERR_CODE:$e"; $(exit $e)' ERR
trap 'e=$? ; trap - RETURN; echo "RETURN - ERR_CODE:$e"; $(exit $e)' RETURN
trap 'e=$? ; trap - EXIT ; echo "EXIT - ERR_CODE:$e"; $(exit $e)' EXIT
trap 'e=$? ; trap - TERM ; echo "TERM - ERR_CODE:$e"; $(exit $e)' TERM

trap

# NOTES:
# - 'trap' return code is ZERO even if no traps defined
# - for all the signals above, there is often (if not always) a way to have an null ERR_CODE
# - traps scope is the current bash process

main () {
    signal=$1
    case $signal in
        LIST) kill -l;
            echo -e 'NSIG) DEBUG (can be equal to SIGRTMAX)\nNSIG+1) ERROR\nNSIG+2) RETURN';
            echo 'EXTRAS: EXIT TERM (EXEC)';
            echo 'For details: locate signal.h';;
        HUP) kill -HUP $$;;
        INT) kill -INT $$;; # raised by CTRL+C => raise an ERR
        QUIT) kill -QUIT $$;;
        ILL) kill -ILL $$;;
        TRAP) kill -TRAP $$;;
        ABRT) kill -ABRT $$;;
        KILL) echo "This won't be caught by the matching trap"; kill -9 $$;;
#        SEGV) echo 'int main(){ int*p = 0; return *p; }' > segfault.c; gcc segfault.c; ./a.out;;
#        SEGV) echo -e '#include <csignal>\nint main() { raise(SIGSEGV); }' > segfault.cpp; g++ segfault.cpp; ./a.out;;
        CONT) echo "'Resumes the process (all threads in the group) from TASK_STOPPED state and also clears any pending/queued stop signals. This happens regardless of blocking, catching, or ignoring SIGCONT.'";
            kill -CONT $$;;
        STOP) echo "This won't be caught by the matching trap + process will be put in background"; kill -STOP $$;;
        DEBUG) :;;
        ERR) $(exit 255);;
        RETURN) echo -e 'foo () { return 12; }\nfoo' > return12 ; source return12 ; rm return12;; # DOES NOT WORK !
        EXIT) exit 11;;
        TERM) kill $$;;
        EXEC) echo "This won't be caught by any trap"; exec printf '';;
        *) ;;
    esac
}

[ "x${@}x" = xRETURNx  ] && { echo -e 'foo () { return 12; }\nfoo' > return12 ; source return12 ; rm return12; } # also raise en ERR12 with bash 3.2
#[ "x${@}x" = xRETURNx  ] && { echo 'return 12' > return12 ; source return12 ; rm return12; } # SHOULD also work but ERR_CODE is 0
main "$@"
