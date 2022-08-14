####################################
# SPECIFIC conf for Ubuntu WSL
[[ $(uname -a) =~ ^Linux.+Microsoft ]] || return 0
####################################

export DOCKER_HOST=tcp://localhost:2375

alias npp='/c/Program\ Files/Notepad++/notepad++.exe'
