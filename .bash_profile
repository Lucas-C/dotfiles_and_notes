# .bash_profile

if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi

export DESK=$USER.desktop.amazon.com

if [ $(uname -s) = Darwin ]; then
    ssh -t $DESK
    return
fi

[ "$HOSTNAME" != "$DESK" ] && return

if [ $TERM == "screen" ]; then
    echo "WARNING: Screen got invoked, something weird's going on"
    return
fi

if ! ps -eo args | grep '^screen'; then
    screen -d -m
fi
screen -A -x

# screen -ls
# screen -r
# DOC: http://www.bangmoney.org/presentations/screen.html
