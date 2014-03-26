# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
fi

# if shell is not interactive, exit, as printing anything at this point will break 'scp'
# also check that [[ =~ ]] is available
if ! [[ $- =~ i ]]; then
    return
fi

# don't put duplicate lines in the history. See bash(1) for more options
# don't overwrite GNU Midnight Commander's setting of 'ignorespace'.
export HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoredups
# ... or force ignoredups and ignorespace
export HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

set -o pipefail

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

if readlink -f ${BASH_SOURCE[0]} >/dev/null 2>&1; then
    export BASHRC_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"
else
    export BASHRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
fi

mkdir -p ~/.vim/undodir

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


########################
# Additionnal .bashrc_*
########################
for f in ${BASHRC_DIR}/.bashrc_*; do
    source $f
done
