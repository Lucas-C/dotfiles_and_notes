unalias ps 2>/dev/null
ps -p $PPID >/dev/null 2>&1 || return # (ps is not standard under boot2docker)
ps -p $PPID | grep -Eq 'pew|python|tilda|su' && return # SHOULD BE: --no-headers --format comm BUT NOT PORTABLE UNDER CYGWIN - Also: 'python' here is how 'pew' appears under Cygwin

if [ -e ~/.use_tmux ]; then ## use TMUX > SCREEN, because of its "no flush" bug (typically on grep | grep cmds)
    type tmux >/dev/null 2>&1 || return
    if ps -p $PPID | grep -q tmux; then # Alreay running in TMUX
        return
    fi
    if ! ps -e | grep -q tmux; then
        touch $BASHRC_DIR/.tmux_window_0_needs_to_be_restored
        tmux new -d -s tmux_$USER
    fi
    if ! tmux attach -t tmux_$USER; then
        killall -9 tmux
        tmux attach -t tmux_$USER
    fi
elif [ -e ~/.use_screen ]; then
    type screen >/dev/null 2>&1 || return
    if ps -p $PPID | grep -q screen; then # Alreay running in SCREEN
        return
    fi
    if ! ps -e | grep -q screen; then
        screen -wipe
        screen -c $BASHRC_DIR/.screenrc -d -m
    fi
    screen -A -x
fi
