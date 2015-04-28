
Linux configuration files
=========================

Compatible for Ubuntu, Red Hat, OSX and Cygwin.


## Installation

    CONFIG_DIR=~/linux_configuration/
    cd
    for f in .gitconfig .inputrc .vimrc; do ln -s $CONFIG_DIR/$f; done
    echo "source $CONFIG_DIR/.bashrc" > .bashrc
    echo 'exec /bin/bash' > .profile

Any .bashrc_* file in $CONFIG_DIR will be sourced.

To use **screen**, create an empty *~/.use_screen* file. Similarly, you can create *~/.use_tmux*.

The .zshrc file is here to invoke _bash_ even if _zsh_ is the default shell.

### Notepad++

As admin:

    CONFIG_DIR=$BASHRC_DIR
    for f in $CONFIG_DIR/npp/*.xml; do cmd /c mklink $(cygpath -w $h/AppData/Roaming/Notepad++/$(basename $f) $(cygpath -w $f); done

<!--
#### ToDo ####

Move all .* files in a subdir.
-->