# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# if shell is not interactive, exit, as printing anything at this point will break 'scp'
# also ensure that [[ =~ ]] is available
if ! [[ $- =~ i ]]; then
    return
fi

set -o pipefail

if readlink -f ${BASH_SOURCE[0]} >/dev/null 2>&1; then
    export BASHRC_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"
else
    export BASHRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
fi

########################
# Additionnal .bashrc_*
########################
for f in ${BASHRC_DIR}/.bashrc_*; do
    source $f
done

#------
# Dirs
#------
if [ -r ${BASHRC_DIR}/.bash_dirs ]; then
    for pass in one two; do
        while read unexDir; do
            dir=$(eval echo "${unexDir}")
            export "$dir"
            eval alias ${dir/=/=\'cd \"}\"\'
        done < ${BASHRC_DIR}/.bash_dirs
    done
fi

