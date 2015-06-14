#!/usr/bin/env bash
set -o pipefail -o errexit -o nounset -o xtrace

if [ -n "${1:-}" ]; then # misc/installCygwin.sh $USER
    cd /cygdrive/d/code
    chown -R $1 .bash* .current_pwd/ .git* .i* .j* .lighttable.user.* .minttyrc .p* .s* .S* .tmux.conf .vimrc .zshrc
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
install apt-cyg $BASHRC_DIR/bin && rm apt-cyg
apt-cyg install wget
apt-cyg install bind curl git make python rlwrap unzip vim

wget https://bootstrap.pypa.io/ez_setup.py -O - | python
easy_install pip

apt-cyg install gcc-g++ libffi-devel libxml2-devel libxslt-devel openssl-devel
pip install --user service_identity scrapy

cd /
[ -e /c ] || ln -s /cygdrive/c
[ -e /d ] || ln -s /cygdrive/d
