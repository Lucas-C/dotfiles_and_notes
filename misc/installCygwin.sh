#!/usr/bin/env bash
set -o pipefail -o errexit -o nounset -o xtrace

# To install without admin rights: setup*.exe --no-admin

if [ -n "${1:-}" ]; then # misc/installCygwin.sh $USER
    cd $code
    chown -R $1 .bash* .current_pwd/ .git* .i* .j* .lighttable.user.* .minttyrc .p* .s* .S* .tmux.conf .vimrc .zshrc
fi

if [ "$TERM" = "cygwin" ]; then
    echo 'Use MinTTY ! Create a Windows shortcut to "C:\path\to\cygwin\bin\mintty.exe /bin/sh --login -i"'
    echo 'or replace "bash" by "start mintty /bin/sh" in Cygwin.bat'
    echo 'and add: set HOME=C:\Users\admin'
    echo "+ don't forget to define a .profile that sources .bashrc"
    exit 1
fi
if [ "$(stat -c '%U' /proc)" != "$USER" ]; then
    echo 'Exiting : need to be admin'
    exit 1
fi

lynx -source rawgit.com/transcode-open/apt-cyg/master/apt-cyg > apt-cyg
mkdir -p ~/bin && install apt-cyg ~/bin && rm apt-cyg
echo 'PATH="$PATH:~/bin"' >> ~/.bashrc && PATH="$PATH:~/bin"
apt-cyg install wget
apt-cyg install curl dos2unix git python3 vim the_silver_searcher
apt-cyg install bind colordiff exiv2 make rlwrap sqlite3 unzip
apt-cyg install procps psmisc # provides 'watch' & 'pstree' respectively
code && git clone git://git.joeyh.name/moreutils && cd moreutils && make # provide ifne, sponge...

python3 -m ensurepip

apt-cyg install GraphicsMagick  # Provides `gm identify`, `gm convert`...
apt-cyg install gcc-g++ libffi-devel libxml2-devel libxslt-devel openssl-devel
pip install --user service_identity scrapy

mkpasswd -c -p "$(cygpath -H)" > /etc/passwd # for .ssh/config to be read: http://superuser.com/a/1145752/255048

cd /
[ -e /c ] || ln -s /cygdrive/c
[ -e /d ] || ln -s /cygdrive/d

echo "Cygwin services configured:"
cygrunsrv --list

exit 0

# In case of "child_info_fork::abort: unable to map **.dll, Win32 error 126"
# As admin:
#    C:\cygwin\bin\ash.exe -c "/usr/bin/rebaseall -v"
#    C:\cygwin\bin\ash.exe -c "/bin/peflagsall -v"
# If pip issue "OSError: [Errno 11] Resource temporarily unavailable",
# simply "pip uninstall $dependency_pkg && pip install $pkg" already saved my ass once

# Cygwin bug with tar: "If you add test.exe and test to a tar archive in that order, you lose test.exe on extraction" - https://www.nu42.com/2016/03/tar-anomaly.html

minidumper --nokill $FILENAME $WIN32PID # create a minidump of a running Windows process

pldd $PID # List dynamic shared objects loaded into a process

