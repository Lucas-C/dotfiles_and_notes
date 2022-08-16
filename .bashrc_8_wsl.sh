####################################
# SPECIFIC conf for Ubuntu WSL
[[ $(uname -a) =~ ^Linux.+[Mm]icrosoft ]] || return 0
####################################

export DOCKER_HOST=tcp://localhost:2375

alias npp='/c/Program\ Files/Notepad++/notepad++.exe'
