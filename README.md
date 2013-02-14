
Linux configuration files
=========================

Compatible for Ubuntu, Red Hat, OSX and Cygwin.


INSTALLATION
------------

Clone the repository and create symlinks from your $HOME to :
  .bashrc
  .gitconfig
  .inputrc
  .vimrc

To launch *screen*, you need to source .bash_screen.

Alternatively, you can source the .bashrc :

    source /path/to/.bashrc

    alias a=alias # added alias

    # Invoke screen if not in a *tilda* terminal
    ps -eo pid,comm | grep $PPID | grep -q 'tilda' || source ${BASHRC_DIR}/.bash_screen

Any other .bashrc_* file in the same directory will be sourced.

Invoke _bash_ even if _zsh_ is the default shell.
