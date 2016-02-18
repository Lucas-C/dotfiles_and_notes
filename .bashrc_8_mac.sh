####################################
# SPECIFIC conf for Mac
[ $(uname -s) = Darwin ] || return 0
####################################

PATH=/usr/X11/bin:$PATH
PATH=/opt/local/bin:/opt/local/sbin:$PATH # Macports

alias l='ls -BFG'
alias df='df -h'
alias psf='ps -eo user,pid,%cpu,%mem,ppid,tty,stat,rss,etime,start,nice,psr,args 2>/dev/null'

alias f='open -a /Applications/Firefox.app'
alias pdf='open -a /Applications/Preview.app'
nav () { open -a /System/Library/CoreServices/Finder.app "${@:-.}"; }
alias js=/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Resources/jsc

alias freeplane='open -a /Applications/Freeplane.app'
alias eclipse='open -a /Applications/eclipse/Eclipse.app'
alias st='open -a /Applications/Sublime\ Text.app'
alias dia='open -a /Applications/Dia.app'
alias xcode='echo No, use Sublime Text && st' #'open -a /Applications/Xcode.app'
word () { open -a "$(echo /Applications/Microsoft\ Office*/Microsoft\ Word.app | tail -n 1)" "$@"; }

unfuncalias touch

slocate() { # Spotlight search
    mdfind "kMDItemDisplayName == '$@'wc";
}

