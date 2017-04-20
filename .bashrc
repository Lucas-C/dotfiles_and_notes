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
# !! When using `pew`, $BASHRC_DIR will be /tmp or pip install pre-commit && pre-commit install -f/tmp/tmp??????

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# Downloading .bashrc_* fragments
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
download_bashrc_files () {
    local fragment bashrc
    for fragment in 0_term_multiplex 1_prompt 2_fcts_aliases_exports 3_ssh 8_mac 8_windows; do
        bashrc=.bashrc_${fragment}.sh
        echo "# Downloading $bashrc from GitHub"
        curl -s "https://raw.githubusercontent.com/Lucas-C/linux_configuration/master/$bashrc" > ${BASHRC_DIR}/$bashrc
    done
    echo "# Downloading git-completion.bash from GitHub"
    curl -s 'https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash' > ${BASHRC_DIR}/.bashrc_git_completion
}

if [ -z "$(ls ${BASHRC_DIR}/.bashrc_* 2>/dev/null)" ]; then
    download_bashrc_files
fi

if [ -r ${BASHRC_DIR}/.bash_aliases ]; then
    source ${BASHRC_DIR}/.bash_aliases
fi

##############################
# Sourcing .bashrc_* fragments
##############################
for f in ${BASHRC_DIR}/.bashrc_*; do
    source $f
done; unset f

if [ -r ${BASHRC_DIR}/.bash_colors ]; then
    source ${BASHRC_DIR}/.bash_colors
fi
