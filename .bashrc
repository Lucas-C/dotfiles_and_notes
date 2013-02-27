# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
    . /etc/bashrc
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

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

export BASHRC_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null )" 2>/dev/null )" && pwd)"

# PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$'
source ${BASHRC_DIR}/.bash_prompt

###########
# EXPORTS
###########
export EDITOR=vim

export PATH=/bin:$PATH
export PATH=/sbin:$PATH
export PATH=/usr/bin:$PATH
export PATH=/usr/sbin:$PATH
export PATH=/usr/local/bin:$PATH
export PATH=/usr/local/bsin:$PATH
export PATH=$BASHRC_DIR/bin:$PATH

##########
# ALIASES
##########
pa () {
    grep --color -h '^[[:space:]]*[[:alnum:]._-]* () {\|^[[:space:]]*alias [[:alnum:]._-]*=' ${BASHRC_DIR}/.bash*
    grep --color '[[:alnum:]]*=' ${BASHRC_DIR}/.bash_dirs
}

#----
# ls
#----
unset ls; unalias ls 2>/dev/null
export LS_COLORS="ln=target" # Avoid mixing all symlinks in same color, and anyway we alias ls with -F
alias l='ls -BF --color=always'
alias la='l -A'
alias ll='l -lhA'
alias lk='ll -Sr'       # sort by size, biggest last
alias lr='ll -lR'       # recursive ls
alias lc='ll -tc'       # sort by and show change time, most recent first
alias lu='ll -tu'       # sort by and show access time, most recent first
alias lt='ll -t'        # sort by date, most recent first
lsp () {                # group files by their prefix
    ls -AB1 $@ | sed 's/\(.[^.]\+\).*/\1/' | sort | uniq -c
}
lse () {                # group files by their extension
    ls -AB1 $@ | awk -F'.' '{print $NF}' | sort | uniq -c
}

#------
# grep
#------
unset grep; unalias grep 2>/dev/null
alias grep='grep -i --color=auto'
alias grepc='grep -i --color=always'
unset zgrep; unalias zgrep 2>/dev/null
alias zgrep='zgrep -i --color=auto' # zgrep also works on plain text files, but '-r' isn't supported
alias zgrepc='zgrep -i --color=always'
rzgrep () {
    local pattern=$1
    shift
    find -L $@ -type f | xargs zgrep $pattern
}
alias hgrep='history | grep'

#-----
# git
#-----
alias gs='git status'
alias ga='git add'
alias gb='git branch'
alias gc='git checkout'
alias gd='git diff'
alias gdc='git diff --cached'
alias gdp='git diff -U999999999 --no-color origin/mainline..HEAD'
alias gl='git log'
alias gll='git log origin/mainline..HEAD' # local commits only
alias gri='git rebase --interactive origin/mainline'
alias gpr='git pull --rebase'
giti () {
    cat >>.gitignore <<EOF

# Universal
nohup.out
.project
.classpath
*.pyc
*.o
*.class
*~
EOF
}

#--------
# Redefs
#--------
unset diff; unalias diff 2>/dev/null
alias diff='diff -b'    # !! Won't work with sudo
unset df; unalias df 2>/dev/null
alias df='df -h'        # !! Won't work with sudo
unset du; unalias du 2>/dev/null
alias du='du -sh'       # !! Won't work with sudo
unset make; unalias make 2>/dev/null
alias make='make -j3 '
unset tkcon; unalias tkcon 2>/dev/null
alias tkcon='tkcon -load Tk'

#------------
# One-letter
#------------
alias e='$EDITOR'
alias b='cd $OLDPWD'
alias f='firefox'
alias h='history'
alias p='pwd'
alias t='tree'

#--------
# Others
#--------
alias pg='ps -ef | grep -i' # using -l make it not portable on Mac
alias tF='tail -F'
alias t5='tail -500'
alias utf8='iconv -f ISO-8859-1 -t UTF-8 '
alias py='python'
alias rmpyc='find -L . -name "*.pyc" | xargs rm -f'

alias nav='nautilus $(pwd)/'
alias pdf='evince'


fopen () { ( firefox file://$(pwd)/$1 ) }


############
# FUNCTIONS
############

source ${BASHRC_DIR}/.bash_ssh_conf


noalias () {            # which' without aliases
    which $1 | tail -1
}

unset man; unalias man 2>/dev/null
man () { $(which man) $@ || ( help $@ 2> /dev/null && help $@ | less ) }

unset touch; unalias touch 2>/dev/null
touch () {              # touch [EPOCH] [+/-<modifier>] <files>
    local yymm=$(date +%y%m) dd=$(date +%d) HHMM=$(date +%H%M)
    if [ "$(echo $1 | tr '[A-Z]' '[a-z]')" = "epoch" ]; then
        yymm=7001
        dd=01
        HHMM=0000
        shift
    fi
    if [[ $1 =~ ^[+-][0-9] ]]; then
        dd=$(($dd$1))
        [ ${#dd} -eq 1 ] && dd=0$dd
        shift
    fi
    local stamp=$yymm$dd$HHMM
    (! [[ $dd =~ ^[0-3][0-9]$ ]] || [ "$dd" -eq 0 ] || [ "$dd" -gt 31 ]) && echo "Day modifier cannot be applied: $stamp" && return
    $(which touch) -t $stamp $@
}

is_true () { ! ( [ -z "$1" ] || [[ "$1" =~ 0+ ]] || [[ "$1" =~ [Ff][Aa][Ll][Ss][Ee] ]] ) }

is_file_open () { ( lsof | grep $(readlink -f "$1") ) }

fqdn () { ( python -c "import socket ; print socket.getfqdn(\"$@\")" ) }

findTxt () { ( find -L "$@" -type f -exec file {} \; | grep text | cut -d':' -f1 ) }

notabs () {             # Replace tabs by 4 spaces & remove trailing ones & spaces
    for f in $(findTxt "$@"); do
        sed -i -e 's/[     ]*$//g' "$f"
        sed -i -e 's/    /    /g' "$f"
    done
}

tstp () {               # timestamp converter
    echo $@ | gawk '{print strftime("%c", $0)}'
    # Or date -d @$TIMESTAMP but neither work on OSX
}

resolve_alias () {      # handle pipes and nested aliases
    local cmd=$1
    local params
    while alias $cmd >/dev/null 2>&1; do
        local aliased=$(alias $cmd | sed "s/.*\([\'\"]\)\(.*\)\1/\2/")
        cmd=$(echo $aliased | awk '{ print $1 }')
        local end_of_cmd=$(echo $aliased | awk '{ $1 = ""; print }') # still contain delim=<space>
        while echo $end_of_cmd | grep -q '|'; do
            local intermediate_cmd=${end_of_cmd##*|}
            end_of_cmd=${end_of_cmd#*|}
            intermediate_cmd=$(resolve_alias $intermediate_cmd)
            params="| $intermediate_cmd $params"
        done
        params="$end_of_cmd $params"
    done
    echo $cmd $params
}
#TEST: alias ec='echo' ; alias dog='cat' ; alias boo='ec BOO | dog'

kill_cmd ()             # WIP - Kill every process starting with the pattern passed as a parameter
{
    while true; do
        pid=$(ps -eo pid,args | egrep -e "[0-9]* /bin/bash $1" | grep -v grep | grep -o '[0-9]*')
        echo "Killing $(ps -eo pid,args | egrep -e "[0-9]* /bin/bash $1" | grep -v grep)"
        if [ -n "$pid" ]; then
            kill "$pid"
        else
            break
        fi
    done
}


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
