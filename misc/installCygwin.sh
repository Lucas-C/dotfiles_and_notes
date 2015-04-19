#!/usr/bin/env bash
set -o pipefail -o errexit -o nounset -o xtrace

if [ -n "${1:-}" ]; then # misc/installCygwin.sh $USER
    cd /cygdrive/d/code
    chown -R $DOTFILES_USER .bash* .current_pwd/ .git* .i* .j* .lighttable.user.* .minttyrc .p* .s* .S* .tmux.conf .vimrc .zshrc
fi

if [ "$TERM" = "cygwin" ]; then
    echo 'Use MinTTY ! Create a Windows shortcut to "D:\devhome\tools\cygwin\bin\mintty.exe /bin/sh --login -i"'
    exit 1
fi
if [ "$(stat -c '%U' /proc)" != "$USER" ]; then
    echo 'Exiting : need to be admin'
    exit 1
fi

lynx -source rawgit.com/transcode-open/apt-cyg/master/apt-cyg > apt-cyg
sed -i 's/md5sum/sha512sum/g' apt-cyg
install apt-cyg ~/bin
apt-cyg install wget
apt-cyg install git

cd /
[ -e /c ] || ln -s /cygdrive/c
[ -e /d ] || ln -s /cygdrive/d
