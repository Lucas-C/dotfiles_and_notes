Linux configuration files
=========================

Compatible for Ubuntu, Red Hat, OSX and Cygwin.


## Installation

    git clone https://github.com/Lucas-C/linux_configuration.git
    BASHRC_DIR=$PWD/linux_configuration
    cd $HOME
    for f in .gitconfig .inputrc .vimrc; do ln -s $BASHRC_DIR/$f; done
    echo "source $BASHRC_DIR/.bashrc" >> .bashrc
    echo 'exec /bin/bash' > .profile

Any .bashrc_* file in $BASHRC_DIR will be sourced.

To use **screen**, create an empty *~/.use_screen* file. Similarly, you can create *~/.use_tmux*.

The .zshrc file is here to invoke _bash_ even if _zsh_ is the default shell.

### Enabling pre-commit hooks

[Install Yelp pre-commit hooks](http://pre-commit.com/#install) and then :

    cd $BASHRC_DIR
    pre-commit install

### Defining git user identity

Keep it separate from your git configuration by putting it in a file named _.gitconfig_user_, in `$BASHRC_DIR`:

    [user]
        name = ...
        email = ...

If such file exists, it will be sourced from the main _.gitconfig_.


## Notepad++

As admin:

    for f in $BASHRC_DIR/npp/*.xml; do cmd /c mklink $(cygpath -w $HOME/AppData/Roaming/Notepad++/)$(basename $f) $(cygpath -w $BASHRC_DIR/$f); done
    cmd /c mklink /d $(cygpath -w $h/AppData/Roaming/Notepad++/themes) $(cygpath -w $BASHRC_DIR/npp/themes)

<!--
#### ToDo ####

Move all .* files in a subdir.
-->
