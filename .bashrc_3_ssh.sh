# Suggestion: switch to Russell91/sshrc and ccontavalli/ssh-ident
SSH_EXPORT_FILES=".bash_colors .bash_dirs .bash_profile .bashrc* .gitconfig .inputrc .js*rc .screenrc .tmux.conf .vimrc* .zshrc"
SSH_EXPORT_TMP_DIR="/tmp/$USER"
SSH_LOG_DIR=~/ssh_logs
VISITED_HOSTS_LOG_FILE=~/.visited
SSH_AUTH_SOCK_LINK=~/.ssh/ssh-agent-auth-sock
SSH_AGENT_CONFIG_FILE_REL=.ssh/ssh-agent.sh
SSH_AGENT_CONFIG_FILE=~/$SSH_AGENT_CONFIG_FILE_REL

# TODO/FLAWS: make up to FOUR ssh connections (with 'visit')
# Will create a remote $HOME dir if needed
# If it fails, config files will still be kept int remote $SSH_EXPORT_TMP_DIR
# DO NOT use sshl in that cmd.
exportSshFiles () {      # export $SSH_EXPORT_FILES to a remote host $1
    local prev_dir=$PWD
    cd $BASHRC_DIR

    if [ "$1" = "--cleanup" ]; then
        local del_flag="--delete"
        shift
    fi

    local tmp_dir=$(mktemp -d /tmp/BashConf_$USER.XXXXXX)
    cp -r $SSH_EXPORT_FILES $tmp_dir

    exportSshFilesCleanup () { rm -rf $tmp_dir ; cd $prev_dir ; }
    trap 'e=$? ; trap - RETURN EXIT INT TERM HUP QUIT ; exportSshFilesCleanup ; $(exit $e)' RETURN EXIT INT TERM HUP QUIT

    for dst in "$@"; do
        local dst_host=${dst%:*}
        local dst_dir=\$HOME
        if [[ $dst =~ : ]]; then
            dst_dir=${dst#*:}
            [[ $dst_dir =~ ^/ ]] || dst_dir="\$HOME/$dst_dir"
        fi

        local install_bash_cmd="
find $tmp_dir -type f -exec chmod -w {} + ;
[ -e $SSH_EXPORT_TMP_DIR ] || mkdir $SSH_EXPORT_TMP_DIR || exit 1 ;
rsync -a $del_flag $tmp_dir/ $SSH_EXPORT_TMP_DIR ;
rm -rf $tmp_dir ;
[ -e $dst_dir ] || ( sudo mkdir $dst_dir && sudo chown $USER $dst_dir ) || exit 1 ;
rsync -a $del_flag $SSH_EXPORT_TMP_DIR/ $dst_dir ;
cd $dst_dir ;
chmod 444 $SSH_EXPORT_FILES ;
rm -rf $SSH_EXPORT_TMP_DIR ;
"

        rsync -avz $del_flag $tmp_dir $dst_host:/tmp || return 1
        # WARNING: ssh does NOT behave the same when cmd is piped as stdin
        ssh -t $dst_host "$install_bash_cmd" || return 1
    done
}

ssh_setup () { # '-f' force a new ssh-agent creation
    IS_SSH_FORWARDED=false
    if [ -r $SSH_AGENT_CONFIG_FILE ]; then
        source $SSH_AGENT_CONFIG_FILE >/dev/null
        [ $(wc -l $SSH_AGENT_CONFIG_FILE | awk '{print $1}') -eq 1 ] && IS_SSH_FORWARDED=true
        rm -f $SSH_AUTH_SOCK_LINK
        ln -s $SSH_AUTH_SOCK $SSH_AUTH_SOCK_LINK
        export SSH_AUTH_SOCK=$SSH_AUTH_SOCK_LINK # required by tmux_ssh, to be able to load the latest ssh agent
    fi

    # We create a new ssh-agent if '-f' is used or 'ssh-add -l' fails (=> no agent running OR no keys loaded)
    if [ "${1:-}" = "-f" ] || ! ssh-add -l >/dev/null 2>&1; then
        echo "Creating new ssh-agent"
        killall ssh-agent
        ssh-agent >$SSH_AGENT_CONFIG_FILE
        source $SSH_AGENT_CONFIG_FILE >/dev/null
        for pub_file_key in $(ls ~/.ssh/id_*.pub 2>/dev/null); do
            local priv_file_key=${pub_file_key%.pub}
            [ -r $priv_file_key ] && ssh-add $priv_file_key
        done
    fi
}

ssh_forward () {
    ssh -A -t "$@" "echo unset SSH_AGENT_PID \&\& export SSH_AUTH_SOCK=\$SSH_AUTH_SOCK > \$HOME/$SSH_AGENT_CONFIG_FILE_REL; bash -i; rm \$HOME/$SSH_AGENT_CONFIG_FILE_REL"
}

pre_ssh () { ssh_setup; }

unfuncalias ssh
ssh () { pre_ssh; [ "$#" -eq 1 ] && set_term_window_name "$1"; $(nofuncalias ssh) "$@"; }
unfuncalias scp
scp () { pre_ssh; $(nofuncalias scp) "$@"; }
unfuncalias rsync
rsync () { pre_ssh; $(nofuncalias rsync) "$@"; }

visit () {              # ssh to a host after calling 'exportSshFiles'. List visited hosts in ~/.visited
    local dst=$(fqdn $1 2>/dev/null || echo $1) ; [ -z $dst ] && echo "MISSING ARG: Specifiy a remote host" && return 1
    if exportSshFiles $dst; then
        sed -i "/$dst/d" $VISITED_HOSTS_LOG_FILE
        echo $dst >> $VISITED_HOSTS_LOG_FILE
        ssh $dst
    else
        echo "${_RED}exportSshFiles FAILED: ${_END} sudo rights probably missing on $dst, fallback to a /tmp \$HOME"
        ssh_with_tmp_home $dst
    fi
}

ssh_with_tmp_home () {
    local dst=$(fqdn $1 2>/dev/null || echo $1) ; [ -z $dst ] && echo "MISSING ARG: Specifiy a remote host" && return 1
    ssh -t $dst "HOME=$SSH_EXPORT_TMP_DIR ; cd ; bash --rcfile .bashrc"
}

rmRemoteHome () {       # remove remote /home/$USER
    local dst=$1 ; [ -z $dst ] && echo "MISSING ARG: Specifiy a remote host" && return 1
    # Backup .*history files
        local logdir=$SSH_LOG_DIR/$1 ; [ -x $logdir ] || mkdir -p $logdir
        scp $dst:~/.*history $logdir
        for f in $logdir/.*history; do mv $f $logdir/$(date +%Y-%m-%d-%Hh_%Mm_%Ss)$(basename $f) ; done
    ssh -t $dst "rm -rf /home/$USER/* && sudo rmdir /home/$USER" || return 1
    [ -w $VISITED_HOSTS_LOG_FILE ] && sed -i -e /$1/d $VISITED_HOSTS_LOG_FILE
}

# FROM: http://dmytro.github.io/2012/10/31/ssh-multi.html
tmux_ssh() {
    local hosts="$@"
    if [ -z "$hosts" ]; then
        echo -n "Please provide of list of hosts separated by spaces [ENTER]: "
        local host
        while read host; do hosts="$host $hosts"; done
    fi
    hosts=($hosts)
    tmux new-window "ssh ${hosts[0]}"
    unset hosts[0];
    for i in "${hosts[@]}"; do
        tmux split-window -h "ssh $i"
        tmux select-layout tiled > /dev/null
    done
    tmux select-pane -t 0
    tmux set-window-option synchronize-panes on > /dev/null
}

sshl () { # Ssh with console logs, useful but not good for security
    local params="$*"
    while [ "${1:0:1}" = "-" ]; do
        [[ ${1:${#1}-1} =~ "[bcDeFiLlmOopRSw]" ]] && shift
        shift
    done
    local logdir=$SSH_LOG_DIR/$1 ; [ -x $logdir ] || mkdir -p $logdir
    local logfile=$logdir/$(date +"%Y-%m-%d-%Hh_%Mm_%Ss").log
    script -c "ssh $params" $logfile
    gzip $logfile &
}
