####################################
# SPECIFIC conf for Windows (Cygwin or Git Bash)
[[ $(uname -s) =~ ^CYGWIN_NT ]] \
    || [[ $(uname -s) =~ ^MINGW32_NT ]] \
    || return 0
####################################

PATH=$PATH:/c/Windows/System32
PATH=$PATH:/c/Windows

if ! [ -s ~/.dir_colors ]; then
    curl -s 'https://raw.githubusercontent.com/seebi/dircolors-solarized/master/dircolors.256dark' > ~/.dir_colors
fi
eval $(SHELL=$SHELL dircolors ~/.dir_colors)

unfuncalias touch

alias ps='echo "Use \`pstree -a\` or \`procps -wwFAH\` to display commands arguments !" && ps'
alias psf='ps -ef'
alias casperjs=cyg-casperjs  # in ~/bin
#alias node=cyg-node  # in ~/bin
alias sudo='cygstart --action=runas'
alias java_home_win_exec='JAVA_HOME=$(cygpath -w "$JAVA_HOME") '

convertWinArgs () {
    while [ "$1" ]; do
        case $1 in
        /*) echo "$(cygpath -w $1)" ;;
        [A-Z]:*) echo "$1" ;;
        *) echo "$(cygpath -w $PWD/$1)" ;;
        esac
        shift
    done
}

win_hosts=$(cygpath -w "C:\Windows\System32\drivers\etc\hosts")

swap_win_hosts () {
    if ! [ -r $win_hosts.bak ]; then
        echo "Creating $win_hosts.bak"
        echo "127.0.0.1       localhost" > $win_hosts.bak
    fi
    cp $win_hosts tmp1 || return 1
    cp $win_hosts.bak tmp2 || return 2
    mv tmp1 $win_hosts.bak || return 3
    mv tmp2 $win_hosts || return 4
}

[ -r "/cygdrive/c/Program Files (x86)" ] && export X86=\ \(x86\)

atom () {
    $(cygpath "$LOCALAPPDATA\atom\bin\atom.cmd") $(convertWinArgs "$@")
}

NPP_BIN='/cygdrive/c/Program Files/Notepad++/notepad++.exe'
test -e "$NPP_BIN" || NPP_BIN="/cygdrive/c/Program Files$X86/Notepad++/notepad++.exe"
npp () {
    for f in "$@"; do
        "$NPP_BIN" $(convertWinArgs "$f")
    done
}

pspad () {
    "/cygdrive/c/Program Files$X86/PSPad editor/PSPad" $(convertWinArgs "$@")
}

bat () {
    cmd /c "set PATH=%OLD_PATH% && $@"
}

cdw () {
    cd $(cygpath "$1")
}

firefox () {
    "/cygdrive/c/Program Files$X86/Mozilla Firefox/firefox" $(convertWinArgs "$@")
}

freeplane () {
    "/cygdrive/c/Program Files$X86/Freeplane/freeplane" $(convertWinArgs "$@")
}

unfuncalias nav
nav () {
    local dir="$1"
    [[ $dir == /* ]] || dir="$PWD/$dir"
    explorer /select,$(cygpath -w "$dir/$(ls "$dir" | head -1)")
}

unfuncalias pdf
pdf () {
    "/cygdrive/c/Program Files/SumatraPDF/SumatraPDF" $(convertWinArgs "$@")
}
pdf_history () {
    grep -F 'FilePath = ' $APPDATA/SumatraPDF/SumatraPDF-settings.txt | sed 's/.*FilePath = //' | tr '\n' '\0' | xargs -0 -n 1 cygpath
}

img () {
    if [ -f "C:\Program Files\Windows Photo Viewer\PhotoViewer.dll" ]; then
        rundll32 "C:\Program Files\Windows Photo Viewer\PhotoViewer.dll" ImageView_Fullscreen $(convertWinArgs "$@")
    else
        rundll32 "C:\Program Files\Windows Photo Gallery\PhotoViewer.dll" ImageView_Fullscreen $(convertWinArgs "$@")
    fi
}

#FROM: http://smecsia.me/blog/65/killall+for+cygwin
killall () {
    if [ "$1" = "-9" ]; then
        taskkill /F /IM $2.exe
    else
        taskkill /IM $1.exe
    fi
}

jar_java_version () {
    local jar=$(readlink -f $1)
    cd /tmp
    local a_class=$(jar tf "$(cygpath -w "$jar")" | grep '^[^$]\+.class$' | head -n 1)
    local a_class_main_dir=$(echo "$a_class" | tr '/' '\n' | head -n 1)
    jar xf "$(cygpath -w "$jar")" "$a_class"
    javap -v "$a_class" | grep version
    rm -r $a_class_main_dir
    cd - >/dev/null
}

convert_win_cmd_output_encoding () { # USAGE: _ netstat --help
    local stdout=$(mktemp)
    local stderr=$(mktemp)
    "$@" >$stdout 2>$stderr
    iconv -f cp850 -t utf8 <$stdout
    iconv -f cp850 -t utf8 <$stderr >&2
}
alias _=convert_win_cmd_output_encoding

alias tcpdump="WinDump.exe" # or RawCap + Wireshark


# USING PHP/COMPOSER/DRUSH WITH CYGWIN IS A BAD IDEA
# (and by the way, it invokes bash through msysgit\bin\sh == MINGW32_NT)
#alias composer='php $(cygpath -w $PHP_HOME/composer.phar)'
#alias drush='DRUSH_PHP=php drush'  # Trick from https://github.com/drush-ops/drush/issues/375
