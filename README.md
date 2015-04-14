
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

   for f in .bashrc .gitconfig .inputrc .vimrc; do ln -s linux_configuration/$f; done
   echo 'exec /bin/bash' > .profile

To use **screen**, create a *~/.use_screen* file. Similarly, you can create *~/.use_tmux*.

As an alternative setup, you can source the versioned .bashrc from your own ~/.bashrc :

    source /path/to/.bashrc

    alias a=alias # added alias

Any other .bashrc_* file in the same directory will be sourced.

The .zshrc file is here to invoke _bash_ even if _zsh_ is the default shell.

#### ToDo ####

Move all .* files in a subdir.
