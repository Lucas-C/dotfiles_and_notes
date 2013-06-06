#========
### SHELL

# Resurect computer : http://en.wikipedia.org/wiki/Magic_SysRq_key

# Fixing terminal frenzy
echo <ctrl-v><ctrl-o>

# Change keyboard to FR
loadkeys fr

# 'top'
* killing : Press "k", then pid, then signal (15, 9...)
* sorting : press "O" and select the column
* display absolute path of commands : "c"

# get process name
pid -o comm= -p $PPID
# get process working directory
pwdx <pid>
get_parent_pid ()
{
    local pid=$1 ; [ -z "$pid" ] && pid=$$
    ps --no-headers --format ppid --pid $pid
}

# detach process
nohup <cmd>
disown -h <pid>

# replace chars from last command
ls docs
^docs^web^

<ALT>+. # insert preceding line's final parameter
!$ # select the last arg
!!:n # selects the nth argument of the last command

mesg
write
wall # broadcast message


##################
# Bash scripting
##################

# Standard warnings
set -eux # -u won't exit in case of a pipe : echo $cmd | grep '.*'
# Check syntax without executing
bash -n <script>

# Redirect logs
exec >>logs/$(basename $0).log.$(date +%Y-%m-%d-%H) 2>&1

# Set positional parameters $0 $1 ...
set - A B C

# Create and set permissions
install -o $USER -m 644 <file>
install -d -m 777 <directory>

: ${1?'Missing parameter'}
: ${var:="default value"}

# Floating point arithmetic
echo "scale=3; 1/3" | bc [-l] # for the std math lib

# Change extension
mv $file ${file%.*}.bak

# Garbage cleaner
garbage_cleaner () { # USAGE: eval $(garbage_cleaner cleanup_func)
    echo trap "'"e=\$? \; trap - RETURN EXIT INT TERM HUP QUIT \; $@ \; \$\(exit \$e\)"'" RETURN EXIT INT TERM HUP QUIT
}
foo () {
    cleanup () { echo CLEANUP ; rm $file ; } # variables will be accesible as this will be called before leaving the function
    eval $(garbage_cleaner cleanup)
    local file=$(mktemp)
    sleep 5
}
# Pros: self-sufficient: no need to untrap, or call the cleanup function at the end of the function its defined
# Cons: cannot be nested, 'set -u' trapped warnings can trigger multiple cleanup : this function MUST be robust

# Script file parent dir
EXEC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Standard logs date
date "+%F %T,%N" | cut -c-23

# Abort <CMD> after a timeout
( cmdpid=$BASHPID; (sleep 10; kill $cmdpid) & exec <CMD> )

is_true () { ! [ -z "$1" ] && ! [[ "$1" =~ 0+ ]] && ! [[ "$1" =~ [Ff][Aa][Ll][Ss][Ee] ]] ; }

is_file_open () { lsof | grep $(readlink -f "$1") ; }

# Associative arrays (FROM: http://stackoverflow.com/questions/1494178/how-to-define-hash-tables-in-bash)
# With built-in arrays and cksum-based hashing function
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

cat <<EOF
EOF

exec 8<>filename # Open file descriptors #8 for reading and writing
echo BlaBlaBla
exec 8>&- # Close file descriptor

# mktemp dir & default value
tdir="$(mktemp -d ${TMPDIR:-/tmp}/$0_XXXXXX)"
# Use RAM for tmp files:
/dev/shm

# http://wiki.bash-hackers.org/howto/getopts_tutorial
while getopts ":ab:" opt; do
    case $opt in
    a) echo "-a was triggered." >&2 ;;
    b) echo "-b was triggered. Parameter: $OPTARG" >&2 ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ; exit 1 ;;
    :) echo "Option -$OPTARG requires an argument." >&2 ; exit 1 ;;
    esac
done

# Parsing *=* args (unsecure)
# Push element in an array
declare -a argFiles
for arg in "$@"; do
    case $arg in
        *=*) eval $argi ;;
        *) argFiles[${#argFiles[*]}]="$arg" ;;
    esac
done

# Convert to array
declare -a array
IFS=' ' read -ra array #<<< "$string"
# Back to string
string="${array[*]}"

# Variables substitutions (http://tldp.org/LDP/abs/html/parameter-substitution.html)
echo ${PWD//\//-}

# Powerful regex
[[ "some string" =~ "$regex" ]]
group1="${BASH_REMATCH[1]}"

# disable wildcard expansion
set -f
# list options values
echo $-

tput
# setaf 1:red, 2:green, 3:yellow, 4:blue, 5:purple, 6:cyan, 7:white
# Also: setab [1-7], setf [1-7], setb [1-7], bold, dim, smul, rev
# sgr0: reset

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

# Syslog
logger -is -t SCRIPT_NAME -p user.warn "Message"

# Logrotate (to call in a cron job)
# Examples: http://www.thegeekstuff.com/2010/07/logrotate-examples/
logrotate -s /var/log/logstatus /etc/logrotate.conf [-d -f]

# Control process priority (useful in cron job)
nice / ionice / renice

# Get all commands prefixed by (useful for unit tests)
compgen -abck unit_test_


#################
# Text filtering
#################

# filter outpout : not lines 1-3 and last one
type ssh_setup | sed -n '1,3!p' | sed '$d'| sed 's/local //g'
# this is also a crazy hack : put the output in ORIG_CMD, then redefine ssh_setup () { eval $ORIG_CMD $@; ... }

# Print lines starting with one containing FOO and ending with one containing BAR.
sed -n '/FOO/,/BAR/p'

# Replace newlines by a separator
seq 1 10 | paste -s -d+ | bc
# Break on world per line
perl -pe 's/\s+/\n/g'
# paste is also usefule to interlace files: paste <file1> <file2>

printf "%-8s\n" "${value}" # 8 spaces output formatting

# Print nth column
awk [-F":"] '{ print $NF }'

# Sets intersec
comm -12 #or uniq -d

# display input to stdout + append to end of <file>
tee -a <file>

# Find non-ASCII characters
grep --color='auto' -P -n "[\x80-\xFF]" file.xml

# fold breaks lines to proper width, and fmt will reformat lines into paragraphs 

# shows non-printing characters as ascii escapes. 
cat -v


#=============
### FILES

find
# Tip: ! -regex 'pat\|tern' >>>way>more>efficient>>> \( -path ./pat -o -path ./tern \) -prune -o -print

# append at the beginning of <file>
sed -i "1i$content" <file>

# Replace whitespaces by underscores
rename \  _ *

# To see all files open in a directory structure:
lsof +D /some/dir
# To see all files jeff has open:
sudo lsof -u jeff
# Additional useful option : -r <t> : repeat the listing every t second

# Shows Where a File/Directory Comes From (links, etc.)
namei
readlink -f

# Sum up kind of files without ext
ls | cut -d . -f 1 | sort | uniq -c

# Forbid file deletion
sudo chattr +i [-R] <file> # to check a file attributes : lsattr

# Create fake file
sudo dd if=/dev/urandom of=FAKE-2012Oct23-000000.rdb bs=1M count=6000

# Bring back deleted file from limbo (ONLY if still in use in another process)
lsof | grep myfile # get pid
cp /proc/<pid>/fd/4 myfile.saved

# http://www.cyberciti.biz/tips/linux-audit-files-to-see-who-made-changes-to-a-file.html
auditctl -w <file> -p wax -k <tag>
ausearch -k <tag> [-ts today -ui 506 -x cat]

# Named pipes: https://en.wikipedia.org/wiki/Named_pipe
mkfifo
python -c "from fcntl import ioctl ; from termios import FIONREAD ; from ctypes import c_int ; from sys import argv ; size_int = c_int() ; fd = open(argv[1]) ; ioctl(fd, FIONREAD, size_int) ; fd.close() ; print size_int.value" <file> # readble bytes in a fifo
ulimit -a | grep pipe # max size
fcntl(fd, F_SETPIPE_SZ, size) # to change max size, if Linux > 2.6.35 (/proc/sys/fs/pipe-max-size)

nm *.o

readelf -Ws *.so

hexdump -c

#Append at the end of stdout (or beginning with ^)
echo ECHO | sed s/$/.ext/

# Convert .wmv to .avi
mencoder vid.wmv -o vid.avi -ofps 25 -ni -ovc lavc -oac mp3lame
# .mp4 to .avi
ffmpeg -i vid.mp4 -f avi -vcodec copy -acodec copy vid.avi

rsync -avz --exclude=".*"

sha{1,224,256,384,512}sum
md5sum


#=============
### NETWORKING

ping <host/ip>
traceroute <host/ip>

# How to grep IPs
grep '[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}'

curl
#See: http://curl.haxx.se/docs/httpscripting.html

# Iptables
iptables -A INPUT -s <IP_OR_HOSTNAME> -j DROP
iptables -n -L -v

snmpget -v2c -c '<community_string>' <device> SNMPv2-MIB::sysDescr.0
# or sysUpTime, sysName
# The community string can be found in the 'Variables' tab in an AutoNOC device page

# Dump all tcp transmission to a specific IP :
sudo tcpdump host -X $IP

# Attribute IP to interface
ifconfig eth0 192.168.0.1

# Query DNS
dig txt [+short] <hostname>
host -t txt <hostname>

# List packet exchanges
netstat [--statistics --udp]

# Checking ports
netstat -nap <port>
nmap -sS -O 127.0.0.1 # Guess OS !!
lsof -i -P -p <pid> # -n => no IP->hostname resolution

# Keep ssh session open after executing commands
ssh $host "$cmds ; /bin/bash -i"
# How to change your login on a specified acces: http://orgmode.org/worg/worg-git-ssh-key.php
.ssh/config



#cCcCcCc#
# Cisco #
#cCcCcCc#
sh run
sh int
sh ip int [brief]
sh ip rou 1.2.3.4
sh version
exit


#=========
### SYSTEM

cat /proc/version
cat /etc/*-release
uname -a
cat /etc/issue*
lsb_release -a

# System errors
dmesg -s 500000 | grep -i "fail\|error\|oom"

# Message of the day
/etc/motd

# Virtualbox
sudo adduser $USER vboxusers # then logout
VBoxManage list vms
VBoxManage controlvm <name> poweroff

# Get uid / groups infos
id $USER # for primary group, use -ng flag
adduser / moduser -a -G # DO NOT FORGET THE -a !!!

# Add a Linuxsecondary group without logging out
newgroup <new secondary group>
newgroup <original primary group>

# List system users
awk -F":" '{ print "username: " $1 "\t\tuid:" $3 }' /etc/passwd

# Sudo user
sudo su -l

# Remove sudo time stamp => no more sudo rights
sudo -K

# setuid: When an executable file has been given the setuid attribute, normal users on the system who have permission to execute this file gain the privileges of the user who owns the file within the created process.
# setgid: Setting the setgid permission on a directory (chmod g+s) causes new files and subdirectories created within it to inherit its group ID

# Watch system stats
watch -d 'cat /proc/meminfo'

iostat
mpstat 5 # cpu usage stats every 5sec

# Checking Swap Space Size and Usage
vmstat 2
sar
# + to consult history : https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Swap_Space-Checking_Swap_Space_Size_and_Usage.html

# Frozen X server
sudo service lightdm restart

# list devices
lspci -v
# list disks
lshw -C disk
# list UUIDs
blkid

# transformer un .rpm en .deb
alien


##~]]%/_°*|-----
# Synthèse vocale
espeak -s 180 -p 40 "Hey ! Look behind you"
espeak -s 180 -p 40 -ven+12 "Hi ! My name is Colossus."
espeak -s 150 -p 20 -vfr "Je vais te péter la gueule"
espeak -v mb/mb-fr1 -s 50 'Je peux parler plus lentement' | mbrola /usr/share/mbrola/voices/fr1 - -.au | aplay
#FROM:   http://doc.ubuntu-fr.org/synthese_vocale
#        http://linux.byexamples.com/archives/303/text-to-speech-synthesizer/
#        http://cookerspot.tuxfamily.org/wikka.php?wakka=SyntheseVocaleEspeak


#=============
### Various

sudo ldconfig

# Use 'apt-file' to see which package provides that file you're missing
sudo dpkg -D1 -i *.deb

# Follow program system calls (!! -f => follow fork)
strace -f -c -p <pid> -e open,access,poll,select,connect,recvfrom,sendto

# Configure 'mail' command
/etc/ssmtp/revaliases
/etc/ssmtp/ssmtp.conf

# Launch command at a specified time or when load average is under 0.8
echo <cmd> | at midnight
echo <cmd> | batch

# Audio/mike issues
pulseaudio -D
pavucontrol
alsamixer
gstreamer-properties

# Rescan for memory card
sudo su -l
echo 1 > /sys/bus/pci/rescan


@@@@@@@@@@
@ MAC OSX
@@@@@@@@@@

# File listed with '@' => extended attributes
xattr -l <file>

# Add user to group
sudo dseditgroup -o edit -a <USER> -t user <GROUP>

# FUN
curl http://google.com/ | base64 | say

# C#
NUNITLIB=/Library/Frameworks/Mono.framework/Versions/2.10.11/lib/mono/2.0/nunit.framework.dll
gmcs -debug -t:library -r:$NUNITLIB *.cs
nunit-console *.dll
mono *.exe


<!---->
<html/>
<!---->

# use protocol-relative URLs (starting with //) like so:
<img src="//domain.com/img/logo.png">
# This will cause the browser to automatically prepend the protocol that is currently being used. This trick also works in CSS.

# Notepad in browser
data:text/html, <html contenteditable>


//~~//~~//~~//~~//
// JavaScript //
//~~//~~//~~//
# Evaluate to 'fail'
(![]+[])[+[]]+(![]+[])[+!+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]];


=======
= Wiki
=======

#REDIRECT[[United States]]

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


:::::::::
:: MySQL
:::::::::

# List columns
show columns from <table>;

# Kill request
SHOW PROCESSLIST;
KILL <thread_to_be_killed>;

# How to start a file to make it executable AND runnable with mysql < FILE.mysql :
/*/cat <<NOEND | mysql #*/
use ...;
select
    ...
from
    ...
where
    ...
order by
    ...;
