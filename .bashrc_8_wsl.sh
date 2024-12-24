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

export BROWSER=firefox.exe
unset -f f
f () { $BROWSER "${@:-$(cat)}"; }
# Not enough for Python, this is also required:
# from webbrowser import register, Mozilla
# register("firefox.exe", None, Mozilla("firefox.exe"))

VSCODE_BIN='/mnt/c/Program Files/Microsoft VS Code/Code.exe'
unfuncalias vscode
vscode () {
    if [ -n "$WSL_DISTRO_NAME" ]; then
        case $PWD in
            /mnt*|/c*|/d*)
                "$VSCODE_BIN" "$@";;
            *)
                for f in "$@"; do
                    "$VSCODE_BIN" --remote "wsl+$WSL_DISTRO_NAME" "$(wslpath -a $f)"
                done;;
            esac
    else
        "$VSCODE_BIN" "$@"
    fi
}

win_hosts='/c/Windows/System32/drivers/etc/hosts'

unfuncalias nav
nav () {
    local dir="$1"
    [[ $dir == /* ]] || dir="$PWD/$dir"
    explorer.exe /select,$(wslpath -w "$dir/$(ls "$dir" | head -1)")
}

img () {
    local PhotoViewerDLLPath="C:\Program Files\Windows Photo Viewer\PhotoViewer.dll"
    local PhotoGalleryDLLPath="C:\Program Files\Windows Photo Gallery\PhotoViewer.dll"
    if [ -f "$(wslpath "$PhotoViewerDLLPath")" ]; then
        rundll32.exe "$PhotoViewerDLLPath" ImageView_Fullscreen $(wslpath -w "$@")
    else
        rundll32.exe "$PhotoGalleryDLLPath" ImageView_Fullscreen $(wslpath -w "$@")
    fi
}

alias vid='/c/Program\ Files/VideoLAN/VLC/vlc.exe'
alias vlc='/c/Program\ Files/VideoLAN/VLC/vlc.exe'

unfuncalias message
message () { # USAGE: $message* [$header]
    local message="${1?'Missing message'}"
    local header="${2:-ALERT}"
    cmd.exe /c $(wslpath -w $BASHRC_DIR/bin/win_alert_powershell.bat) "$message" "$header"
}
