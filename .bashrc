# Source global definitions
[ -e /etc/bashrc ] && source /etc/bashrc
[ -e /etc/bash_completion ] && source /etc/bash_completion

# if shell is not interactive, exit, as printing anything at this point will break 'scp'
# also ensure that [[ =~ ]] is available
[[ $- =~ i ]] || return

set -o pipefail

stty -ixon # disable C-s & C-q being caught by 'flow control' artifact feature

if readlink -f ${BASH_SOURCE[0]} >/dev/null 2>&1; then
    export BASHRC_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"
else
    export BASHRC_DIR="$(builtin cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
fi

source ${BASHRC_DIR}/.bash_colors

########################
# Additionnal .bashrc_*
########################
for f in ${BASHRC_DIR}/.bashrc_*; do
    source $f
done; unset f

#------
# Dirs
#------
if [ -r ${BASHRC_DIR}/.bash_dirs ]; then
    for pass in one two; do
        while read unexDir; do # last line won't be read if file does not end with a newline
            dir=$(eval echo "${unexDir}")
            export "$dir"
            eval alias ${dir/=/=\'cd \"}\"\'
        done < ${BASHRC_DIR}/.bash_dirs
    done
fi

