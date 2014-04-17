~°~°~°~°~°~°~°~°~°~°~
### SHELL & misc  ###
~°~°~°~°~°~°~°~°~°~°~

# Useful key bindings
<CTRL>+u : remove part of current line "a gaUche"
<CTRL>+k : remove "Klosing" part of current line
<CTRL>+w : remove previous "Word"
<CTRL>+r : search bash history, powerful to use with cmd #tags

# replace word from 'last command'
^command^user^

<ALT>+. # insert preceding line's final parameter
!$ # select the last arg
!!:n # selects the nth argument of the last command

xclip [-selection clipboard] # copy & paste clipboard
ranger # text-based file manager written in Python with vi key bindings

time read # chrono
man ascii # display ASCII table
cal # quick calendar - Also: calcurse, wyrd
look # find English words (or lines in a file) beginning with a string

write / mesg # 2nd control write access
wall # broadcast message

# 'top' < 'htop'
* display full command path of processes : "c"
* killing : Press "k", then pid, then signal (15, 9...)
* sorting : press "O" and select the column
* display /cores stats : "1"
* colors : 'Z'; then save config: 'W'
VIRT: how much memory the program is able to access at the present moment
RES: resident size, how much actual physical memory a process is consuming (heap memory that is currently in RAM) + (non heap memory in RAM) + (thread stack memory * number of threads) + (direct/mapped buffer memory)
DATA is the amount of VIRT used that isn't shared and that isn't code-text; i.e., it is the virtual stack and heap of the process
SHR: how much of the VIRT size is actually sharable memory or libraries
SWAP: bogus
pstree -p [$OPT_PID] # hierarchy of processes

pid -o comm= -p $PPID # get process name
pwdx $pid # get process working directory

nohup $cmd # detach command
disown -h $pid # detach running process

kill -15 # (TERM) then wait 2sec, then -2 (INT) then -1 (HUP) THEN -9 (KILL)
# Because then: no sockets shutdown / no tmp files cleanup / children not informed / no terminal reset
kill -l # list signals

xkill # kill window by clicking
xprop # get window infos by cliking
xdpyinfo / xwininfo -children -id $ID # get X11 windows infos

# Follow program system calls (!! -f => follow fork)
strace -f -p $pid -e open,access,poll,select,connect,recvfrom,sendto [-c] #stats
strace -f -e trace=network -s 10000 $cmd # capture network traffic
# Bug: http://lethargy.org/~jesus/writes/beware-of-strace ; https://bugzilla.redhat.com/show_bug.cgi?id=590172
kill -CONT $pid # strace bug fix
ltrace -ttS -s 65535 -o $logfile -p $pid # log system calls and library calls

cat /proc/pid/smaps # get resources infos
pmap -x $pid # get memory usage
valgrind --tool=massif $cmd # get memory usage with details & graph
valgrind --leak-check=full --track-origins=yes # --tool=callgrind / kcachegrind

# get a core file for a running program
gdb -batch -quiet -ex 'generate-core-file' -p PROGRAMPID # then manipulate with pstack, pmap
# get a stack trace for all threads
gdb -batch -quiet -ex "thread apply all bt full" -p PROGRAMPID > program-backtrace.log

hexdump -c # aka 'hd', use 'bvi' for editing
strings -n $min_length exec.bin # extract strings of length >= 4
objdump
/dev/mem # Physical memory, useful to strings | grep pswd. Ubuntu limit this to 1Mb
dd if=/dev/fmem of=/tmp/fmem_dump.dd bs=1MB count=10 # don't forget 'count'
nm *.o # list symbols
readelf -Ws *.so
ldd $executable # list dynamically linked libs

# LD_PRELOAD trick
man ld.so
gcc -Wall -fPIC -shared -o myfopen.so myfopen.c
LD_PRELOAD=./myfopen.so cat $file

# Youtube playlist query - Start from 1, max paging 50, max playlist size 200
playlist=FLF8xTv55ZmwikWWmWLPEAZQ
rm yt_playlist_$playlist
for i in {1..4}; do
    index=$(( (i-1)*50 + 1 ))
    curl -s "https://gdata.youtube.com/feeds/api/playlists/$playlist?start-index=$index&amp;max-results=50&amp;v=2" >> yt_playlist_$playlist
done

ttyrec, ipbt, ttygif # record & playback terminal sessions 

: () { : | : & } ; : # Fork bomb

perl -wle 'exit 1 if (1 x shift) !~ /^1?$|^(11+?)\1+$/' # Primality testing with a REGEX !

a(){ echo $2 \\$1 $1 $2 $1 ;};a \' ' a(){ echo $2 \\$1 $1 $2 $1 ;};a '


##################
  Bash scripting
##################

# Standard warnings
set -o pipefail -o errexit -o nounset -o xtrace
export PS4='+ ${FUNCNAME[0]:+${FUNCNAME[0]}():}line ${LINENO}: '

bash -n $script # Check syntax without executing
bash --debugger $script

parent_func=$(caller 0 | cut -d' ' -f2) # "$line $subroutine $filename"
source ~/sctrace.sh # FROM: http://stackoverflow.com/questions/685435/bash-stacktrace/686092

EXEC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )" # Script file parent dir
exec >>$EXEC_DIR/logs/$(basename $0).log.$(date +%Y-%m-%d-%H) 2>&1 # Redirect logs
date "+%F %T,%N" | cut -c-23 # Standard logs date
date -u +%s # Seconds since EPOCH
date -d @$seconds_since_epoch "+%F" # under OSX: date -jf "%s" $secs "+%F"

# !! aliases used in functions definitions are immediately substituted,
# NOT resolved dynamically !
alias foo='echo A'
bar () { foo; }
alias foo='echo B'
bar # echo A

# Set positional parameters $0 $1 ...
set - A B C

: ${1:?'Missing or empty parameter'}
: ${var:="new value set if empty"}
local var=${1:-"default value"}
# !! 'local' is a command, and its return code will shadow the one of the cmd in the right part of an assignment

echo ${PWD//\//-} # Variables substitutions (http://tldp.org/LDP/abs/html/parameter-substitution.html)
${var%?} # Remove the final character of var

for pair in $whatever; do key=${pair%:*}; value=${pair#*:}; ...
for f in ./*.txt; do; [[ -f "$f" ]] || continue # Safe 'for' loop - http://bash.cumulonim.biz/BashPitfalls.html

readonly CONST=42 # works with arrays & functions too

# Q: Can we find a function 'identity' that satisfies the following 2 properties ? stackoverflow.com/q/21635301
identity () { for arg in "$@"; do echo "$arg"; done; }
identity "$(identity a\ b c\ d)"
# a b
# c d # expected output: OK
argv_count () { echo "argv_count($@):$#" >&2; }
argv_count $(identity a\ b c\ d)
# 4 # NOT 2 : KO
# ANSWER: NO, because $() mangle the output in one string
# => use | over $() for list of strings containing spaces

# Q: How to store the output of a command in a variable without spawning a subshell ? stackoverflow.com/q/21632126
bar () { echo "$BASH_SUBSHELL $BASHPID"; }
mapfile -t bar_output < <(foo) # STILL creates a new process + only available since bash 4
# -> use a non-blocking FIFO !

local argv=("$@") # Convert to array
"${argv[*]}" # expands to a single word with the value of each array member separated by the first character of the IFS variable
"${name[@]}" # expands each element of name to a separate word
${#argv[@]} != ${#argv} # array size VS char-length of 1st elem
${argv[@]:(-1)} # last element
echo ${argv[@]:1:2} # Array slice
unset argv[0] # remove element, WITHOUT-INDEX-SHIFTING

# Parsing *=* args (unsecure) by pushing elements in an array
declare -a argFiles # optional
for arg in "$@"; do
    case $arg in
        *=*) eval $argi ;;
        *) argFiles[${#argFiles[*]}]="$arg" ;;
    esac
done
# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":ab:" opt; do
    case $opt in
    a) echo "-a was triggered." >&2 ;;
    b) echo "-b was triggered. Parameter: $OPTARG" >&2 ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2 ; exit 1 ;;
    esac
done

declare -A hash_table # Associative arrays
# Or, with built-in arrays and cksum-based hashing function (FROM: http://stackoverflow.com/questions/1494178/how-to-define-hash-tables-in-bash)
hf () { local h=$(echo "$*" |cksum); echo "${h//[!0-9]}"; } # hashing function
table[$(hf foo bar)]="x42"
echo ${table[$(hf foo bar)]}
echo ${table[@]}
# With /dev/shm in-memory files (+persistent)
hinit() { rm -rf "/dev/shm/hashmap.$1" ; mkdir -p "/dev/shm/hashmap.$1" ; }
hput() { echo "$3" > "/dev/shm/hashmap.$1/$2" ; } # or printf to avoid \n
hget() { cat "/dev/shm/hashmap.$1/$2" ; }
hkeys() { ls -1 "/dev/shm/hashmap.$1" ; }
hvalues() { cat "/dev/shm/hashmap.$1/*" ; }
hcount() { hkeys $1 | wc -l ; }
hdestroy() { rm -rf "/dev/shm/hashmap.$1" ; }

# Powerful regex
[[ "some string" =~ "$regex" ]]
group1="${BASH_REMATCH[1]}"

# Simulating 'pipefail', from gzip:zgrep source code
r=$(
    exec 4>&1
    (eval "$cmd1" 4>&-; echo $? >&4) | sed "$cmd2" 4>&-
) && exit $r

# Create and set permissions
install -o ${SUDO_USER:-$USER} -m 644 $file
install -d -m 777 $directory

# Floating point arithmetic
echo "$((RANDOM%6+1)) + 1/3" | bc -l # or specify "scale=X;" instead of flag - Also: qalc
factor $really_long_int # decompose in factors

is_true () { ! { [ -z "$1" ] || [[ "$1" =~ 0+ ]] || [[ "$1" =~ [Ff][Aa][Ll][Ss][Ee] ]] ; } ; }

is_file_open () { lsof | grep $(readlink -f "$1") ; }

cat <<EOF
EOF

exec 8<>filename # Open file descriptors #8 for reading and writing
echo BlaBlaBla
exec 8>&- # Close file descriptor

/var/tmp is better than /tmp # as filling it is less system impacting
tdir="$(mktemp -d ${TMPDIR:-/tmp}/$0_XXXXXX)" # mktemp dir & default value
/dev/shmi # Use RAM for tmp files - monitor usage with ipcs -m

tput setaf [1-7] / tput sgr0 # enable colored terminal output / reset it
# 1:red, 2:green, 3:yellow, 4:blue, 5:purple, 6:cyan, 7:white
# But colors can be set like this: tput initc 2 500 900 100 # RGB values between 0 & 1000
# Also: setab [1-7], setf [1-7], setb [1-7], bold, dim, smul, rev
for i in {0..255}; do printf "\x1b[38;5;${i}mcolour${i}\x1b[0m\n"; done # display all 256 colours
tput sc;tput cup 0 $(($(tput cols)-29));date;tput rc # put a clock in the top right corner

select value in choice1 choice2; do break; done # multiple choices
# ask a yes or no question, with a default of no.
echo -n "Do you ...? [y/N]: "
read answer
if expr "$answer" : ' *[yY].*' > /dev/null; then
   echo OK
else
   echo KO
fi

# Ask for a password without echoing the characters. The trapping ensures that an interrupt does not leave the echoing off.
stty -echo
trap "stty echo ; echo 'Interrupted' ; exit 1" 1 2 3 15
echo -n "Enter password: "
read password
stty echo

# disable wildcard expansion
set -o noglob
# Extended bash globbing
shopt -s extglob # http://www.linuxjournal.com/content/bash-extended-globbing
shopt [-o] # list options values. Alt: $- E.g. check if shell is interactive: [[ $- =~ i ]]

( set -o posix; set ) # List all defined variables
# Get all commands prefixed by (useful for unit tests)
compgen -abck unit_test_
# Control readline auto-completion : http://linuxcommand.org/man_pages/complete1.html
# can be enable by '-e' flag of 'read'
complete -f -X '!*.ext' command # exclude files using a filter
complete -F _compfunc command
_compfunc() {
    local cmd="${1##*/}"
    local word=${COMP_WORDS[COMP_CWORD]}
    local line=${COMP_LINE}
    local xpat='!*.foo'

    COMPREPLY=($(compgen -f -X "$xpat" -- "${word}"))
}
hash # frequently used commands cache

# Syslog (port: 514)
logger -is -t SCRIPT_NAME -p user.warn "Message"
echo "<15>My logline" | nc -u -w 1 $HOSTNAME 514 # <15> means 'user.debug', see RFC3164: Facility*8 + Severity, default:13 <-> user.notice

mv $file ${file%.*}.bak # Change extension
mv --backup=numbered new target # !! --suffix/SIMPLE_BACKUP_SUFFIX can be broken on some distros
logrotate -s /var/log/logstatus /etc/logrotate.conf [-d -f] # Logrotate (to call in a cron job) Examples: http://www.thegeekstuff.com/2010/07/logrotate-examples/
# !! $@ not supported if < v.7.5

flock -n /pathi/to/lockfile -c cmd # run cmd only if lock acquired, useful for cron jobs
lockfile-create/remove/check # file locks manipulation

# Launch command at a specified time or when load average is under 0.8
echo $cmd | at midnight
echo $cmd | batch

nice / ionice / renice # Control process priority (useful in cron job)
# control the resources available to the shell and to processes it starts
ulimit -v # max virtual memory
ulimit -s # max stack size
ulimit -t # max of cpu time
ulimit -u # max number of processes


++++++++++++++++++
# Text stream filtering
++++++++++++++++++

>| # '>' that overrides 'set -o noclobber'

grep -q # silent, !! FAIL with SIGPIPE if 'pipefail' is used: http://stackoverflow.com/a/19120674/636849
grep '\<word\>' # match word-boundaries
grep -I # ignore binary files
grep -R --include='*.py' --exclude='/build/'
grep -o # output only matching parts
grep -C3 # output 3 lines of context, see also -B/-A
grep -H/-h # output with/without filename
grep -L $pattern $files # Get only filenames where PATTERN is not present
grep -P '^((?!b).)*a((?!b).)*$' # Grep 'a' but not 'b' -> PCRE ;  awk '/a/ && !/b/'
grep -P -n "[\x80-\xFF]" file.xml # Find non-ASCII characters
LANG=C grep -F # faster grep : fixed strings + no UTF8 multibyte, ASCII only (significantly better if v < 2.7)
sed -n '/FOO/,/BAR/p' # Print lines starting with one containing FOO and ending with one containing BAR.
perl -ne '/r[eg](ex)p+/ && print "$1\n"' # print only matching groups

pdftotext $file.pdf - | grep # from xpdf-utils
gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite [-dPDFSETTINGS=/screen|/ebook|/printer|/prepress] -sOutputFile=$out.pdf $in.pdf # reduce pdf size with ghostscript - Also: http://compress.smallpdf.com

tr -c '[:alnum:]' _

cat -vET # shows non-printing characters as ascii escapes.
printf "\177\n" # echo non-ascii, here 'DEL' in octal. echo $'\177' is equivalent, BUT:
# echo $'A\0B' -> A
# printf 'A\0B\n' -> AB

make 2>&1 | colout -t cmake | colout -t g++ # from nojhan github: "Color Up Arbitrary Command Output"

# filter outpout : not lines 1-3 and last one
type ssh_setup | sed -n '1,3!p' | sed '$d'| sed 's/local //g'
# this is also a crazy hack : put the output in ORIG_CMD, then redefine ssh_setup () { eval $ORIG_CMD $@; ... }

perl -ne 'if (length > $w) { $w = length; print $ARGV.":".$_ };  END {print "$w\n"}' *.py # Longest line of code
cloc # count lines of code

comm -12 #or uniq -d - Sets intersec - See also: "Set Operations in the Unix Shell"
join # join lines of two files on a common field

tee -a $file # display input to stdout + append to end of $file
echo ECHO | sed s/$/.ext/ # Append at the end of stdout (or beginning with ^)
sed -i "1i$content" $file # append at the beginning of $file

sed ':a;N;$!ba;s/PATTERN\n/PATTERN/g' # remove newlines after PATTERN
seq 1 10 | paste -s -d+ | bc # Replace newlines by a separator, aka 'join' - Also, for arrays: OLD_IFS=$IFS; IFS=+; echo "${argv[*]}"; IFS=$OLD_IFS
# paste is also useful to interlace files: paste $file1 $file2

perl -pe 's/\s+/\n/g' # Break on word per line
awk [-F":|="] '{ print $NF }' # Print last column. Opposite: awk '{$NF=""; print $0}'. Only last elems: awk -F' ' '{for (i = 3; i <= NF; i++) printf "%s ",$i; print ""}'
fold # breaks lines to proper width
fmt # reformat lines into paragraphs
printf "%-8s\n" "${value}" # 8 spaces output formatting
| xargs -n 1 sh -c 'echo ${0:0:3}' # 3 first characters of $string

zcat /usr/share/man/man1/man.1.gz | groff -mandoc -Thtml > man.1.html # also -Tascii
txt2man -h 2>&1 | txt2man -T # make 'man' page from txt file
pandoc -s -f markdown -t man foo.md | man -l - # md2man : man pandoc_markdown
markdown foo.md | lynx -stdin # alternative using HTML an an intermediate instead of groff


=#=#=#=#=#=
   FILES
#=#=#=#=#=#

ls | cut -d . -f 1 | funiq # Sum up kind of files without ext

find / -xdev -size +100M -exec ls -lh {} \; # find big/largest files IGNORING other partitions - One can safely ignore /proc/kcore
find . -type d -name .git -prune -o -type f -print # Ignore .git
find -regex 'pat\|tern' # >>>way>more>efficient>than>>> \( -path ./pat -o -path ./tern \) -prune -o -print
find . \( ! -path '*/.*' \) -type f -printf '%T@ %p\n' | sort -k 1nr | sed 's/^[^ ]* //' | xargs -n 1 ls -l # list files by modification time
find . -mtime +730 -exec rm -f {} \;

rename \  _ * # Replace whitespaces by underscores

# To see all files open in a directory structure:
lsof +D /some/dir
# To see all files jeff has open:
sudo lsof -u jeff
# Additional useful option : -r $t : repeat the listing every $t second

namei / readlink -f # Shows Where a File/Directory Comes From (links, etc.)

killall -HUP $process_name # To tell a process to reload its file descriptors, e.g. when deleting a log file

sudo dd if=/dev/urandom of=FAKE-2012Oct23-000000.rdb bs=1M count=6000 # Create fake file
truncate -s $size_in_bytes $file # from coreutils

# setuid: When an executable file has been given the setuid attribute, normal users on the system who have permission to execute this file gain the privileges of the user who owns the file within the created process.
# setgid: Setting the setgid permission on a directory (chmod g+s) causes new files and subdirectories created within it to inherit its group ID
setcap # man capabilities
umask # Control the permissions a process will give by default to files it creates; useful to avoid temporarily having world-readable files before 'chmoding' them

# Forbid file deletion
sudo chattr +i [-R] $file # to check a file attributes : lsattr

debugfs -R "stat <$(ls -i $file | awk '{print $1}')>" $(df $file | tail -n 1 | awk '{print $1}') # Get $file creation time ('crtime') on ext4 filesystems

# Bring back deleted file from limbo (ONLY if still in use in another process)
lsof | grep myfile # get pid
cp /proc/$pid/fd/4 myfile.saved

# http://www.cyberciti.biz/tips/linux-audit-files-to-see-who-made-changes-to-a-file.html
auditctl -w $file -p wax -k $tag
ausearch -k $tag [-ts today -ui 506 -x cat]

rsync -v --compress --exclude=".*" $src $dst
--archive # recursive + preserve mtime, permissions...
--delete # remove extra remote files
--append # resume interrupted rsync/cp
--backup --backup-dir=/var/tmp/rsync # keep a copy of the dst file

tar -J... # instead of -z, .xz compression format support
pigz # paralell gzip
yum install p7zip # for .7z files

sha{1,224,256,384,512}sum
md5sum


&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*
* Parallellism, queueing, caching... *
&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*&*
xargs -P 0 # or GNU parallel

memcached

mkfifo # Named pipes: https://en.wikipedia.org/wiki/Named_pipe
exec 3<> /tmp/myfifo # Über trick: dummy FD => non-blocking named-pipe
python -c "from fcntl import ioctl ; from termios import FIONREAD ; from ctypes import c_int ; from sys import argv ; size_int = c_int() ; fd = open(argv[1]) ; ioctl(fd, FIONREAD, size_int) ; fd.close() ; print size_int.value" $fifo # readble bytes in a fifo -> NOT RELIABLE, e.g. always return 0 with non-blocking named-pipe
ulimit -p # should get max pipe size, but WRONG : defined in pipe_fs_i.h
fcntl(fd, F_SETPIPE_SZ, size) # to change max size, if Linux > 2.6.35 (/proc/sys/fs/pipe-max-size)

man mq_overview # POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code
beanstalk # Better alternative queuing system, with lots of existing tools & libs in various labguages
ActiveMQ, RQ(Redis), RestMQ(Redis), RabittMQ # Message queue using AMPQ
Celery/Kombu # Framework to use any of the above ones - note: Celery using 100% CPU is OK say developpers

BerkeleyDB, SQLite, LMDB, LevelDB # embedded database

redis-cli ping
redis-cli -h HOST -p PORT -n DATABASE_NUMBER llen QUEUE_NAME
redis-cli -h HOST -p PORT -n DATABASE_NUMBER keys \*

RRDtool (the ancestor) and its followers: RRDCached, Graphite Whisper, OpenTSDB, reconnoiter, chriso/gauged # storage layer for numeric data series over time


|°|°|°|°|°|°|°|°
== NETWORKING
|°|°|°|°|°|°|°|°

mtr $host > ping / traceroute
paris-traceroute > traceroute

socat > nc (netcat) > telnet
socat - udp4-listen:5000,fork # create server redirecting listening on port 5000 output to terminal
nc -l -u -k -w 1 5000
echo hello | socat - udp4:127.0.0.1:5000 # send msg to server
echo hello | nc -u -w 1 127.0.0.1 5000

# Port scanning
nmap -sS -O 127.0.0.1 # Guess OS !! Also try -A
nmap $host -p $port --reason [-sT|-sU] # TCP/UDP scanning ; -Pn => no host ping, only scanning
nmap 192.168.1.* # Or 192.168.1.0/24, scan entire subnet
nmap -DdecoyIP1,decoyIP2 ... # cloak your scan

# Locally
lsof -i -P -p $pid # -i => list all Internet network files ; -P => no conversion of port numbers to port names for network files ; -n => no IP->hostname resolution
lsof -i -n | grep ssh # list SSH connections/tunnels

ss -nap # -a => list both listening and non-listening sockets/ports ; -n => no DNS resolution for addresses, use IPs ; -p => get pid & name of process owning the socket
ss -lp [-t|-u] # list only listening TCP/UDP sockets/ports

# Even if 'ss' is the replacement for deprecated 'netstat', the following has no equivalent
netstat --statistics [--udp] # global network statistics

ip n[eighbour] # ARP or NDISC cache entries - replace deprecated 'arp'
ip a[ddr] [show|add $ip] dev eth0 # replace deprecated 'ifconfig'
ip link set eth0 [up|down] # enable/disable the[interface specified
ip tunnel list # list ssh stunnels replace deprecated 'iptunnel'
ip route # host routing tables - replace deprecated 'route'
iw # details about wireless interfaces - replace deprecated 'iwconfig'
MACADDR=$(ip address show eth0 | grep link/ether | awk '{print $2 }') # can be used to get a unique machine id number instead of using $RANDOM:
echo $((  16#$(echo $MACADDR | sed 's/://g') % 10000 )) # use base16 - ALT: use md5sum

# On RedHat / CentOS / Fedora
$EDITOR /etc/sysconfig/network-scripts/ifcfg-eth0
$EDITOR /etc/sysconfig/network
/etc/init.d/network restart
ifup, ifdown # bring a network interface up

ls /var/lib/dhc* # check what DHCP client is used
# Query DNS cmds > deprecated 'nslookup'
host [-t txt] $hostname # -a (all records) -v
dig +short txt $dns_server
dig +short -x $ip # Reverse DNS
avahi-resolve -n $USER.local # Multicast DNS == mDNS - from avahi-tools pkg
# Caching
/etc/resolv.conf # manual / basic
bind / dnsmasq / lwresd / nscd (broken: ignore TTL) # daemon
getent ahostsv4 www.google.com # whole query through NSS
rndc # display various DNS cache control commands, part of Bind9 tools suite
rndc -p 954 dumpdb -cache # dump the cache in $(find /var -name named_dump.db) ; lwresd $port can be figured out with lsof/nmap
# View queries bypassing lwresd
/usr/sbin/tcpdump -pnl -s0 -c150 udp and dst port 53 and src port not \
    $(/usr/sbin/lsof -n -i4udp | awk '$1 == "lwresd" && $NF !~ /:921$/ { print substr($NF,3); exit }')

sudo service restart ssh
ssh $host "$cmds ; /bin/bash -i" # Keep ssh session open after executing commands
ssh -f $host -L 2034:$host:34 -N # port forwarding
[ENTER] ~. # Exit a hung SSH session
# How to change your login on a specified acces: http://orgmode.org/worg/worg-git-ssh-key.php
# SSH daemon config to allow UNIX user/pswd auth:
/etc/ssh/sshd_config # PasswordAuthentication yes, UsePAM yes OR AllowGroups sshusers
/etc/pam.d/* # use pam_unix.so
knockd # port knocking server
openssl s_client # bare SSL client cmd
openssl x509 -text -noout -in $cert.pem # get certs details
openssl x509 -inform der -in $cert.cer -out $cert.pem # convert .cer to .pem
keytool -printcert -file $cert.pem # get certs details

iptables -A INPUT -s $host -j DROP
iptables -n -L -v

snmpget -v2c -c "$community_string" $device sysDescr.0 # or sysUpTime.0, sysName.0
# SNMP port : 161
# LAG == Link Aggregation

# Dump all tcp transmission to a specific IP :
sudo tcpdump -i $interface host $IP [ip proto icmp|udp|tcp] -A -s 0 # last flag remove the limit on the captured packet size | Use -X for hex-dump | -n to disable dns resolution

grep -Eo '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}' # grep an IP

# Find wireless driver
lspci -vv -s $(lspci | grep -i wireless | awk '{print $1}')

# Non portable tools
slurm, iptraf, ntop, iftop, nethogs
mininet # realistic virtual network, running real kernel, switch and application code, on a single machine

ipcalc < cidr $ip/X # get netmask, network address - FROM http://fossies.org/linux/privat/cidr-2.3.2.tar.gz/

# Configure 'mail' command
/etc/ssmtp/revaliases
/etc/ssmtp/ssmtp.conf

lynx -dump -stdin # convert HTML to text
wget --random-wait -r -p -e robots=off -U mozilla http://www.example.com # aspire web page
  -p --page-requisites : download all the files necessary to properly display a page: inlined images, sounds, CSS...
  -k --convert-links : convert the links in the document to make them suitable for local viewing
  --no-parent : do not ever ascend to the parent directory when retrieving recursively
  -A --accept acclist -R --reject rejlist : comma-separated list of filename suffixes or patterns to accept or reject
  -l --level=depth : default = 5
  -c --continue : continue getting a partially-downloaded file
curl # http://curl.haxx.se/docs/httpscripting.html
# Web scrapping:
httrack
PhantomJS
Scrapbook, iMacros # FF extensions
Scrapy, RoboBrowser, FlexGet # python crawling libs


=cCcCcCc=
# Cisco #
=cCcCcCc=

enable # unlock more comnmands
show version
exit

show logging [buffered]

sh run
sh int
sh ip int [brief]
sh ip rou 1.2.3.4

# for Fastpath, e.g. QuantaLB:
show logging hosts
show logging buffered
traceroute $regional_syslog_ip


-%-%-%-%-%-
 =SYSTEM=
-%-%-%-%-%-

powertop # diagnose issues with power consumption 
sysctl

cat /etc/*-release
lsb_release -a
uname -a
cat /etc/issue*

/proc/version
/proc/cpuinfo # Number of cores, cache size & alignement...
/proc/loadavg : # graph in TTY: tload
- first 3 fields : number of jobs in the run queue (state R) or waiting for disk I/O (state D) averaged over 1, 5, and 15 minutes
- 4th field : number of currently executing kernel scheduling entities (processes, threads) / number of existing kernel scheduling entities
- 5th field : PID of last process created

stap # SystemTap
perf # need a version of linux-tools-* mathcing the kernel
    top -G
    stat -e cycles,instructions,cache-misses,dTLB-load-misses -p $PID

watch -d 'cat /proc/meminfo' # Watch system stats

# System errors
dmesg -s 500000 | grep -i -C 1 "fail\|error\|fatal\|warn\|oom"
# Enable dmesg timestamps
echo 1 > /sys/module/printk/parameters/printk_time

iostat # + iotop, non portable
mpstat 5 # cpu usage stats every 5sec
dstat, glances # non portables

# Checking Swap Space Size and Usage
free -m # how much free ram I really have ? -> look at the row that says "-/+ buffers/cache"
vmstat 2
sar
# + to consult history : https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Swap_Space-Checking_Swap_Space_Size_and_Usage.html

# People previous logged
last [-f /var/log/wtmp.1]

# Message of the day
/etc/motd

# Get uid / groups infos
id $USER # for primary group, use -ng flag
adduser / usermod -a -G # DO NOT FORGET THE -a !!!
useradd -m -G sudo,sshusers -p $(openssl passwd ******)

# Add a Linux secondary group without logging out
newgroup $new_secondary_group
newgroup $original_primary_group

# List system users
awk -F":" '{ print "username: " $1 "\t\tuid:" $3 }' /etc/passwd

sudo su -l # login as user root
sudo -K # Remove sudo time stamp => no more sudo rights
fakeroot # runs a command in an environment wherein it appears to have root privileges for file manipulation

lspci -v # list devices
lshw -C disk # list disks : ata, cdrom, dvdrom
blkid # list UUIDs
dmidecode
/sbin/mdadm --examine --scan --verbose # need root - RAID config

# Find what package a command belong to:
apt-file search /path/to/anyfile
yum provides $cmd
dpkg -S /path/to/cmd
rpm -qif $(which cmd)
rpm -Uvh pkg.rpm # upgrade RPM

apt-key fingerprint # display imported keys fingerprints
sudo dpkg -D1 -i *.deb

rpm --qf "%{INSTALLTIME:date} %{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm\n" -qa *regex* # list rpm
rpmbuild file.spec
alien # transformer un .rpm en .deb

init q # Reload /etc/inittab
chkconfig, service # control & check /etc/init.d scripts

shutdown -r -F now # force FCSK disk check - Or: touch /forcefsck


##################
~= Issues Fixes =~
##################
# Resurect computer : http://en.wikipedia.org/wiki/Magic_SysRq_key

echo <ctrl-v><ctrl-o> # or 'reset', fix terminal frenzy

sudo ldconfig

killall gnome-settings-daemon # Fix crazy numpad (no '-')
# Frozen X server
sudo service lightdm restart
killall gnome-panel

xev # Listen to keyboard events
loadkeys fr # Change keyboard to FR
install myspell-fr # LibreOffice SpellCheck
rm ~/.config/user-dirs.locale # can fix broken locale

# Audio/mike issues
pulseaudio -D
pavucontrol
alsamixer
gstreamer-properties

mplayer -identify -vo null -ao null -frames 0 $file | grep "Video stream found" # Identify video
mencoder vid.wmv -o vid.avi -ofps 25 -ni -ovc lavc -oac mp3lame # Convert .wmv to .avi
avconv -i vid%02d.mp4 -vcodec copy -acodec copy vid.avi # .mp4 to .avi

sudo /usr/share/doc/libdvdread4/install-css.sh # Install libdvdcss

# Rescan for memory card
sudo su -l
echo 1 > /sys/bus/pci/rescan

~/.mozilla/firefox/*.default/mimeTypes.rdf # FIREFOX 'open with' mapping
about:cache # Firefox cache infos: location, size, number of entries
$ff_profile_dir/.parentlock # fix "Firefox is already running but is not responding" error

xhost local:root # Xlib: connection to ":0.0" refused by server

grep -a # when grep returns "Binary file (standard input) matches"


=\/=/\=\/=/\=\/=
=  Virtualbox
=\/=/\=\/=/\=\/=
sudo adduser $USER vboxusers # then logout
VBoxManage list vms
VBoxManage controlvm $name poweroff

# Cool features : remote display (VRDS), shared folders & clipboard, seamless mode


]_]_]_]_]_]_]_]
] ImageMagick
]_]_]_]_]_]_]_]
# Compile IM with HDRI:
# - http://www.imagemagick.org/script/install-source.php
# - sudo aptitude install libmagickcore-dev liblcms2-dev libtiff4-dev libfreetype6-dev libjpeg8-dev liblqr-1-0-dev libglib2.0-dev libfontconfig-dev libxext-dev libz-dev libbz2-dev
# - ./configure --enable-hdri
# - identify -version # to check HDRI is enabled
# Scripts: http://www.fmwconcepts.com/imagemagick/
display $img_file
convert img.png -adaptive-resize 800x600 -auto-orienti -crop 50x100+10+20 img.jpg
mogrify ... *.jpg # for f in *.jpg; do convert $f ... ; done
identify -v $img_file # get PPI: -format "%w x %h %x x %y"
import # screenshot
animate -delay 5 *.png
compare img1 img2
composite # merge images


()()()()()()()()()()
() Synthèse vocale
()()()()()()()()()()
espeak -s 180 -p 40 "Hey ! Look behind you"
espeak -s 180 -p 40 -ven+12 "Hi ! My name is Colossus."
espeak -s 150 -p 20 -vfr "Je vais te péter la gueule"
espeak -v mb/mb-fr1 -s 50 'Je peux parler plus lentement' | mbrola /usr/share/mbrola/voices/fr1 - -.au | aplay
#FROM:   http://doc.ubuntu-fr.org/synthese_vocale
#        http://linux.byexamples.com/archives/303/text-to-speech-synthesizer/
#        http://cookerspot.tuxfamily.org/wikka.php?wakka=SyntheseVocaleEspeak


@@@@@@@@@@
@ MAC OSX
@@@@@@@@@@

curl http://google.com/ | base64 | say # FUN

dns-sd -Q $USER.local # mDNS query

sudo softwareupdate -i -a # Manual software update

Finder > Applications > Utilities > Disk Utility # Repair permissions

system_profiler # list system components, ports...
pmset -g # power management settings

pbpaste | pbcopy # clipboard

textutil -convert txt # or -info : convert / get infos on files

xattr -l $file # File listed with '@' => extended attributes

sudo dseditgroup -o edit -a $USER -t user $GROUP # Add user to group

find $(ls | grep -Ev 'Library|Documents|Downloads|httrack|phantomjs|vitavermis') \( ! -path '*/.*' \) -type f -print0 | xargs -0 stat -f '%m %N' | sort -k 1nr | while read timestamp file; do echo $(date -jf "%s" $timestamp "+%F") $file; done | less # illustrate how to replace find -printf + timestamp conversion + find non-hidden files only ; GOAL: list files by modification date

# DTrace scripts: man -k dtrace
iosnoop # or better hfsslower.d from the DTrace book, available online
execsnoop # trace processes created
opensnoop -ve # trace open files, also maclife.d from DTrace book to trace files creation/deletion
dtruss -d # strace
soconnect_mac.d # trace TCP connections, from DTrace book
errinfo # trace system call fail
bitesize.d # trace I/O
iotop

# C#
NUNITLIB=/Library/Frameworks/Mono.framework/Versions/2.10.11/lib/mono/2.0/nunit.framework.dll
gmcs -debug -t:library -r:$NUNITLIB *.cs
nunit-console *.dll
mono *.exe

# AppleScript
#!/usr/bin/osascript
on log(msg)
  set log_line to (do shell script "date  +'%Y-%m-%d %H:%M:%S'" as string) & " " & msg
  do shell script "echo " & quoted form of log_line
end log
log "HELLO WORLD !"


=======
= Wiki
=======
dig +short txt $keyword.wp.dg.cx # Wikipedia query over DNS

<!-- Comment -->

#REDIRECT[[United States]]

# To see child pages, try to delete the page !

{{:Transclude_an_arbitrary_page{{{with_template_param_subst|default_value}}}}}

{{ {{{|safesubst:}}}lc:THIS LOWERCASE TEXT}} # uc for UPPERCASE
x<sup>2</sup>, x<sub>2</sub>

<includeonly>bgcolor="#1F78B4"|[https://{{{1}}} <span style="color:black">{{{1}}}</span>]</includeonly>
<noinclude>
Explanations...
Example:
{| {{my_template}}
| What you type
| What you get
|-
| <nowiki>{{my_template|42}}</nowiki>
| {{my_template|42}}
|}
[[Category:Template|{{PAGENAME}}]]
</noinclude>

{{!}}, {{=}} # escape pipe & equal signs

<nowiki>https://my.url/app/</nowiki>{{MyTemplate}} # URL with template

{{#if:{{{variable_foo|}}} # http://www.mediawiki.org/wiki/Help:Extension:ParserFunctions - use {{{1|}}} for positional params
|foo is set to '''{{{variable_foo}}}'''
|foo is ''blank''}}

Multi-Line <pre></pre> within list (* or #) : use  &#10; (Line Feed) or &#13; (Carriage Return) for newlines

---- # horizontal separator

<pre&lt;noinclude&gt;&lt;/noinclude&gt;>
Include {{templates}} in pre blocks
</pre&lt;noinclude&gt;&lt;/noinclude&gt;>
{{#tag:pre|
alt{{ernative}}
}}

http://en.wikipedia.org/wiki/Help:Magic_words


::=::=::=::
:: MySQL / SQLite
::=::=::=::
LIKE >faster> REGEXP

sqlite3 places.sqlite "select a.url, b.title from moz_places a, moz_bookmarks b where a.id=b.fk;" # no cmd => interactive - Firefox
.help
.tables
.schema moz_places

mysql -h $HOST -u $USER -p [--ssl-ca=$file.pem] # default port 3306
mytop # watch mysql

show tables;
show table status;
show columns from $table;
show processlist;
kill $thread_to_be_killed;

# How to start a file to make it executable AND runnable with mysql < FILE.mysql :
/*/cat <<NOEND | mysql #*/
USE ...;
WITH
    subquery AS ( SELECT ... ),
    ...
SELECT
    id, name
FROM
    subquery,
    ... # "inline" SELECT are also allowed
WHERE
    ...
ORDER BY
    ...;
