# INSPIRATION: jeremy-bash@batray.net ; http://www.dreaming.org/~giles/bashprompt/prompts/dan.html


# Minimal PS1 to copy/paste on machines without this .bashrc :
#  prompt_command() { EXIT_CODE=${?/#0/}; }; export PROMPT_COMMAND=prompt_command; export PS1='\[\e[0;34m\]\u\[\e[0m\]@\[\e[1;35m\]\h\[\e[0m\]:\[\e[0;32m\]\W\[\e[0m\]\[\e[1;31m\] $EXIT_CODE\[\e[0m\]\$ '



# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

export T_normal=0
export T_bold=1
export T_underline=4
export C_owner='0;32' # green
export C_write='0;36' # cyan
export C_nowrite='0;31' # red
export C_error='1;31' # bold red
export C_branch='0;33' # yellow
export C_chrooted='0;36' # cyan
export C_virtualenv='0;34' # blue

export HOST_COLOR='1;35' # magenta
export DIRCOLOR=$T_normal
export USER_STYLE=$T_normal
export EXIT_CODE=0

# FROM: http://stackoverflow.com/a/88716
IS_CHROOTED_PROMPT='{}'
if stat -c %i / >/dev/null 2>&1; then # Ensuring 'stat' command exists (it is not under boot2docker)
    ROOT_INODE=$(stat -c %i /)
    if [ $ROOT_INODE -ne 2 -a $ROOT_INODE -ne 128 ] && [ -z "${WINDIR:-}" ]; then
        IS_CHROOTED_PROMPT='{chrooted}'
    fi
fi

export PS1=\
'\[\e[${USER_STYLE}m\]\u\[\e[${T_normal}m\]'\
'\[\e[${C_chrooted}m\]${IS_CHROOTED_PROMPT}\[\e[${T_normal}m\]'\
'\[\e[${C_branch}m\][${GIT_BRANCH}]\[\e[${T_normal}m\]'\
'\[\e[${C_virtualenv}m\]('$(basename "${VIRTUAL_ENV:-}")')\[\e[${T_normal}m\]'\
':\[\e[${DIRCOLOR}m\]\W\[\e[${T_normal}m\]'\
'\[\e[${C_error}m\] $EXIT_CODE\[\e[${T_normal}m\]\$ '

export PROMPT_COMMAND=prompt_command
prompt_command ()
{
    EXIT_CODE=${?/#0/}
    DIRCOLOR=$T_normal
    if [ -O "$PWD" ]; then
        DIRCOLOR=$C_owner
    elif [ -w "$PWD" ]; then
        DIRCOLOR=$C_write
    else
        DIRCOLOR=$C_nowrite
    fi

    if [ -S "$SSH_AUTH_SOCK" ]; then # exists and is a socket
        USER_STYLE=$T_underline
    else
        USER_STYLE=$T_normal
    fi

    if type git >/dev/null 2>&1; then
        GIT_BRANCH=$(git branch --no-color 2>/dev/null | sed -ne 's/^* //p')
    fi

    history -a # flush history => shared between term sessions

    [ -n "${TMUX:-}" ] && tmux list-windows | awk -F: '{print $1}' > $CURRENT_PWD_DIR/tmux_live_windows
}

CURRENT_PWD_DIR=$BASHRC_DIR/.current_pwd
mkdir -p $CURRENT_PWD_DIR

cd () {                 # zsh-like, USAGE: cd $path | cd $old_path_snippet $new_path_subst
    local error_code
    if [ -z "${1:-}" ]; then
        builtin cd
    elif [ -z "${2:-}" ]; then
        builtin cd "$1"
    else
        local stringified_path="$@"
        local subsituted_path="${PWD/$1/$2}"
        if [ -d "$stringified_path" ]; then
            builtin cd "$stringified_path"
        elif [ -d "$subsituted_path" ]; then
            builtin cd "$subsituted_path"
        else
            builtin cd "$@"
        fi
    fi
    error_code=$?
    [ $error_code -ne 0 ] && return $error_code
    if [ -n "${TMUX:-}" ]; then
        set_term_window_name "#[fg=colour$((RANDOM%230+1))]$(hostname | cut -d. -f1):$(pwd | awk -F/ '{print $NF}')#[default]"
        local tmux_window=$(tmux display -pt $TMUX_PANE '#I')
        pwd > $CURRENT_PWD_DIR/tmux_window_${tmux_window}_pwd
    else
        set_term_window_name "$(hostname | cut -d. -f1):$(pwd | awk -F/ '{print $NF}')"
    fi
    [ "$PWD" != "$HOME" ] && pwd > $CURRENT_PWD_DIR/last_pwd
    return 0
}

set_term_window_name () {  # Valid for Tmux AND Screen
    [ "${TERM:-}" = screen ] && printf "\033k$@\033\\"
    return 0
}

_tmux_restore_windows () {
    [ -n "${TMUX:-}" ] || return 1
    local tmux_window=$(tmux display -pt $TMUX_PANE '#I')
    [ -e $BASHRC_DIR/.tmux_window_${tmux_window}_needs_to_be_restored ] || return 2
    if [ $tmux_window -eq 0 ]; then
        local is_first_window=true
        while read window_id; do
            if $is_first_window; then
                [ $window_id -ne 0 ] && tmux move-window -t $window_id
                is_first_window=false
            else
                touch $BASHRC_DIR/.tmux_window_${window_id}_needs_to_be_restored
                tmux new-window -t $window_id
            fi
        done < $CURRENT_PWD_DIR/tmux_live_windows
    fi
    cd $(cat $CURRENT_PWD_DIR/tmux_window_${tmux_window}_pwd)
    rm $BASHRC_DIR/.tmux_window_${tmux_window}_needs_to_be_restored
}

_tmux_restore_windows || builtin cd "$(cat $CURRENT_PWD_DIR/last_pwd 2>/dev/null)"

