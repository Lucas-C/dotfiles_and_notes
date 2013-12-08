#!/bin/bash

# TODO:
#- generate a cmds / signals caught grid
#- make the lib 'set -eux' proof

trap
# No output => traps are 'bash process specific'
# Return code is always ZERO even if no traps defined

trap 'e=$? ; trap - EXIT ; echo "EXIT - ERR_CODE:$e"; $(exit $e)' EXIT
trap 'e=$? ; trap - RETURN ; echo "RETURN - ERR_CODE:$e"; $(exit $e)' RETURN
trap 'e=$? ; trap - TERM ; echo "TERM - ERR_CODE:$e"; $(exit $e)' TERM
trap 'e=$? ; trap - ERR ; echo "ERR - ERR_CODE:$e"; $(exit $e)' ERR
trap 'e=$? ; trap - INT ; echo "INT - ERR_CODE:$e"; $(exit $e)' INT
trap 'e=$? ; trap - HUP ; echo "HUP - ERR_CODE:$e"; $(exit $e)' HUP
trap 'e=$? ; trap - QUIT ; echo "QUIT - ERR_CODE:$e"; $(exit $e)' QUIT
#trap 'e=$? ; trap - DEBUG ; echo "DEBUG - ERR_CODE:$e"; $(exit $e)' DEBUG

trap

main () {
    signal=$1
    case $signal in
        EXIT) exit 11;;
        RETURN) source empty.sh;;
        TERM) kill $$;;
        ERR) false;;
        KILL9) echo "There will be no end-trap"; kill -9 $$;;
        EXEC) echo "There will be no end-trap"; exec printf '';;
        *) ;;
    esac
}

main "$@"
