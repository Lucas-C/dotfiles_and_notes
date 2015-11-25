# Author: Lucas Cimon (github.com/Lucas-C/linux_configuration)

# Source global definitions
[ -e /etc/bashrc ] && source /etc/bashrc
[ -e /etc/bash_completion ] && source /etc/bash_completion

# if shell is not interactive, exit, as printing anything at this point will break 'scp'
# also ensure that [[ =~ ]] is available
[[ $- =~ i ]] || return

set -o pipefail

stty -ixon # disable C-s & C-q being caught by 'flow control' artifact feature

if readlink -f ${BASH_SOURCE[0]} >/dev/null 2>&1; then  # if 'readlink' command exists -> resolve symlinks
    export BASHRC_DIR="$(dirname "$(readlink -f "${BASH_SOURCE[0]}" )" )"
else  # fallback
    export BASHRC_DIR="$(builtin cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
fi

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Downloading .bashrc_* fragments
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
download_bashrc_files () {
    echo "Downloading .bashrc* from GitHub"
    local bashrc
    for bashrc in .bashrc_0_term_multiplex .bashrc_1_prompt .bashrc_2_fcts_aliases_exports .bashrc_3_ssh .bashrc_8_mac .bashrc_8_windows; do
        curl "https://raw.githubusercontent.com/Lucas-C/linux_configuration/master/$bashrc" > ${BASHRC_DIR}/$bashrc
    done
    curl 'https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash' > ${BASHRC_DIR}/.bashrc_git_completion
}
[ -z "$(ls ${BASHRC_DIR}/.bashrc_*)" ] && download_bashrc_files

##############################
# Sourcing .bashrc_* fragments
##############################
for f in ${BASHRC_DIR}/.bashrc_*; do
    source $f
done; unset f
source ${BASHRC_DIR}/.bash_colors

#------------------------------
# Directory aliases / variables
#------------------------------
if [ -r ${BASHRC_DIR}/.bash_dirs ]; then
    for pass in one two; do
        while read unexDir; do # last line won't be read if file does not end with a newline
            dir=$(eval echo "${unexDir}")
            export "$dir"
            eval alias ${dir/=/=\'cd \"}\"\'
        done < ${BASHRC_DIR}/.bash_dirs
        unset unexDir
    done; unset pass
fi
