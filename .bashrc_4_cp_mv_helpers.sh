#mv () {
#    rsync_massive_mv_tip "$@" || /bin/mv "$@"
#}

rsync_massive_mv_tip () { # 'mv' suggesting 'rsync' for 'massive' src files & different partitions
    _get_cp_mv_src_args "$@" >/dev/null || return 1
    _is_massive_cp_mv_src "$@" || return 2
    local src_args_partitions=$(_get_cp_mv_src_args "$@" | xargs df -P | sort | uniq | sed '$d' | awk '{print $1}')

    _get_cp_mv_dst_arg "$@" || return 3
    local dst_arg_partition=$(_get_cp_mv_dst_arg "$@" | xargs -n 1 dirname | xargs df -P | sort | uniq | sed '$d' | awk '{print $1}')

    local non_common_partitions=$(comm -23 <(echo $src_args_partitions | sort) <(echo "$dst_arg_partition" | sort))
    [ -z "$non_common_partitions" ] && return 4

    cat <<EOF
You're about to move a MASSIVE amount of files to another partition.
To first copy files and follow this task progress, I suggest using:
rsync -r --partial --progress --human-readable --ignore-times --rsh=/dev/null $@
If you want to ignore my advice, simply run:
/bin/mv $@
EOF
}

#cp () { # 'cp' suggesting 'rsync' to follow progress for 'massive' src files
#    rsync_massive_cp_tip "$@" || /bin/cp "$@"
#}

rsync_massive_cp_tip () {
    _is_massive_cp_mv_src "$@" || return 1
    cat <<EOF
You're about to copy a MASSIVE amount of files. To follow this task progress, I suggest using:
rsync --partial --progress --human-readable --ignore-times --rsh=/dev/null $@
If you want to ignore my advice, simply run:
/bin/cp $@
EOF
}

_is_massive_cp_mv_src () { # 'massive' means >1000 files OR >100Mo
    [ -z "$1" ] && return 1
    local files_count_max_1000=$(_get_cp_mv_src_args "$@" | while read file; do find "$file" -type f; done | head -n 1000 | wc -l)
    [ ${files_count_max_1000:-0} -eq 1000 ] && return 0
    local src_args_size=$(_get_cp_mv_src_args "$@" | while read file; do du -sm "$file" | cut -f1; done | awk '{s+=$1} END {print s}')
    [ ${src_args_size:-0} -gt 100 ] && return 0
    return 1
}

_get_cp_mv_src_args () {
    while [[ "$1" =~ ^-[^t] ]]; do
        shift
    done
    if [ "$1" = "-t" ]; then
        shift; shift # removing -t $dst
        for arg in "$@"; do echo "$arg"; done
    else
        local argv=("$@")
        unset argv[${#argv[@]}-1] # removing last element: $dst
        for arg in "${argv[@]}"; do echo "$arg"; done
    fi
}

_get_cp_mv_dst_arg () {
    while [[ "$1" =~ -[^t] ]]; do
        shift
    done
    if [ "$1" = "-t" ]; then
        echo "$2"
    else
        local argv=("$@")
        echo "${argv[-1]}"
    fi
}

cp_p () { # 'cp' showing progress, but slower than rsync and less portable. Alt: Xfennec/cv
    strace -q -e write cp -- "${1}" "${2}" 2>&1 | awk '{
        if (NR % int(total_size / 409600) == 0) {
            percent = NR * 409600 / total_size
            printf "%3d%% [", percent
            for (i=0;i<=percent;i++)
               printf "="
            printf ">"
            for (i=percent;i<100;i++)
               printf " "
            printf "]\r"
        }
    } END { print "" }' total_size=$(stat -c '%s' "${1}")
}

