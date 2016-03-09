#!/usr/bin/env bash
set -o pipefail -o errexit -o nounset -o xtrace

if [ -n "${1:-}" ]; then # misc/installCygwin.sh $USER
    cd $code
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
apt-cyg install procps # provides 'watch'
apt-cyg install bind colordiff curl git make python3 rlwrap unzip vim

python3 -m ensurepip

apt-cyg install GraphicsMagick  # Provides `gm identify`, `gm convert`...
apt-cyg install gcc-g++ libffi-devel libxml2-devel libxslt-devel openssl-devel
pip install --user service_identity scrapy

cd /
[ -e /c ] || ln -s /cygdrive/c
[ -e /d ] || ln -s /cygdrive/d

echo "Cygwin services configured:"
cygrunsrv --list

# In case of "child_info_fork::abort: unable to map **.dll, Win32 error 126"
# As admin:
#    G:\devhome\tools\cygwin\bin\ash.exe -c '/usr/bin/rebaseall -v'
#    G:\devhome\tools\cygwin\bin\ash.exe -c '/bin/peflagsall -v'
# If pip issue "OSError: [Errno 11] Resource temporarily unavailable",
# simply "pip uninstall $dependency_pkg && pip install $pkg" already saved my ass once

# Cygwin bug with tar: "If you add test.exe and test to a tar archive in that order, you lose test.exe on extraction" - https://www.nu42.com/2016/03/tar-anomaly.html