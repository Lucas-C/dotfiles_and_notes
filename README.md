Linux configuration files
=========================

Compatible with Ubuntu, Red Hat, OSX and Cygwin.


## Installation

    git clone https://github.com/Lucas-C/dotfiles_and_notes.git
    BASHRC_DIR=$PWD/dotfiles_and_notes
    cd $HOME
    for f in .gemrc .gitconfig .inputrc .minttyrc .vimrc; do [ -e $f ] && echo "Backing up $f" && mv $f{,.bak}; ln -s $BASHRC_DIR/$f; done
    echo "source $BASHRC_DIR/.bashrc" >> .bashrc

Any .bashrc_* file in $BASHRC_DIR will be sourced.

Optionally you may need to add the following in `~/.profile` (and maybe create this file),
but beware that this once broke the session start step and got me stuck on the login screen with a CentOS VM:

    exec /bin/bash

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

<!--
#### ToDo ####

Move all .* files in a subdir
and use stow: http://sametmax.com/regrouper-ses-fichiers-de-settings-avec-stow/
or https://github.com/deadc0de6/dotdrop
-->
