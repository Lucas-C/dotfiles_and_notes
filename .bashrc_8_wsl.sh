####################################
# SPECIFIC conf for Ubuntu WSL
[[ $(uname -a) =~ ^Linux.+[Mm]icrosoft ]] || return 0
####################################

PATH=$PATH:/c/Windows/System32
PATH=$PATH:/c/Windows

export DOCKER_HOST=tcp://localhost:2375
# Required so that gpg2 can prompt for passphrase in a terminal,
# to avoid git error: gpg failed to sign the data / gpg: signing failed: Inappropriate ioctl for device
export GPG_TTY=$(tty)

NPP_BIN='/c/Program Files/Notepad++/notepad++.exe'
npp () {
    for f in "$@"; do
        "$NPP_BIN" "$(wslpath -w $f)"
    done
}

win_hosts='/c/Windows/System32/drivers/etc/hosts'

unfuncalias nav
nav () {
    local dir="$1"
    [[ $dir == /* ]] || dir="$PWD/$dir"
    explorer.exe /select,$(wslpath -w "$dir/$(ls "$dir" | head -1)")
}
