
Linux configuration files
=========================

Compatible for Ubuntu, Red Hat, OSX and Cygwin.


### INSTALLATION

Clone the repository and create symlinks from your $HOME to :

* .bashrc

* .gitconfig

* .inputrc

* .vimrc

* .tmux.conf

To launch **screen**, you need to source .bash-screen.

As an alternative setup, you can source the versioned .bashrc from your own ~/.bashrc :

    source /path/to/.bashrc

    alias a=alias # added alias

Any other .bashrc_* file in the same directory will be sourced.

The .zshrc file is here to invoke _bash_ even if _zsh_ is the default shell.
