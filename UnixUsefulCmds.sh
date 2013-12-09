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

time read # chrono
man ascii # display ASCII table
cal # quick calendar
look # find English words (or lines in a file) beginning with a string

# 'top' < 'htop'
* killing : Press "k", then pid, then signal (15, 9...)
* sorting : press "O" and select the column
* display full command path of processes : "c"
* display /cores stats : "1"
VIRT: how much memory the program is able to access at the present moment
RES: resident size, how much actual physical memory a process is consuming (heap memory that is currently in RAM) + (non heap memory in RAM) + (thread stack memory * number of threads) + (direct/mapped buffer memory)
DATA is the amount of VIRT used that isn't shared and that isn't code-text; i.e., it is the virtual stack and heap of the process
SHR: how much of the VIRT size is actually sharable memory or libraries
SWAP: bogus
pstree -p # hierarchy of processes

pid -o comm= -p $PPID # get process name
pwdx <pid> # get process working directory

nohup <cmd> # detach command
disown -h <pid> # detach running process

# Follow program system calls (!! -f => follow fork)
strace -f -p <pid> -e open,access,poll,select,connect,recvfrom,sendto [-c] #stats
# Bug: http://lethargy.org/~jesus/writes/beware-of-strace ; https://bugzilla.redhat.com/show_bug.cgi?id=590172
kill -CONT <pid> # Fix
# log system calls and library calls
ltrace -ttS -s 65535 -o <logfile> -p <pid> 

cat /proc/<pid>/smaps # get resources infos
pmap -x <pid> # get memory usage
valgrind --tool=massif <cmd> # get memory usage with details & graph
valgrind --leak-check=full --track-origins=yes # --tool=callgrind / kcachegrind

# get a core file for a running program 
gdb -batch -quiet -ex 'generate-core-file' -p PROGRAMPID 
# get a stack trace for all threads 
gdb -batch -quiet -ex "thread apply all bt full" -p PROGRAMPID > program-backtrace.log 

hexdump -c # aka 'hd', use 'bvi' for editing
strings exec.bin # extract strings of length >= 4
objdump

nm *.o # list symbols
readelf -Ws *.so

sudo ldconfig

# LD_PRELOAD trick
man ld.so
gcc -Wall -fPIC -shared -o myfopen.so myfopen.c
LD_PRELOAD=./myfopen.so cat <file>

write / mesg # 2nd control write access
wall # broadcast message

xev # Listen to keyboard events
loadkeys fr # Change keyboard to FR
killall gnome-settings-daemon # Fix crazy numpad (no '-')

echo <ctrl-v><ctrl-o> # or 'reset', fix terminal frenzy

# Configure 'mail' command
/etc/ssmtp/revaliases
/etc/ssmtp/ssmtp.conf

# Audio/mike issues
pulseaudio -D
pavucontrol
alsamixer
gstreamer-properties

apt-file # see which package provides that file you're missing
apt-key fingerprint # display imported keys fingerprints
sudo dpkg -D1 -i *.deb

# Identify video
mplayer -identify -vo null -ao null -frames 0 <video>
# Convert .wmv to .avi
mencoder vid.wmv -o vid.avi -ofps 25 -ni -ovc lavc -oac mp3lame
# .mp4 to .avi
avconv -i vid%02d.mp4 -vcodec copy -acodec copy vid.avi

# Install libdvdcss
sudo /usr/share/doc/libdvdread4/install-css.sh

# Rescan for memory card
sudo su -l
echo 1 > /sys/bus/pci/rescan

/dev/mem # Physical memory, useful to strings | grep pswd. Ubuntu limit this to 1Mb
dd if=/dev/fmem of=/tmp/fmem_dump.dd bs=1MB count=10 # don't forget 'count'

: () { : | : & } ; : # Fork bomb

perl -wle 'print "Prime" if (1 x shift) !~ /^1?$|^(11+?)\1+$/' # Primality testing with a REGEX !

# Resurect computer : http://en.wikipedia.org/wiki/Magic_SysRq_key


##################
  Bash scripting
##################

# Standard warnings
set -o pipefail -o errexit -o nounset -o xtrace
export PS4='+ ${FUNCNAME[0]:+${FUNCNAME[0]}():}line ${LINENO}: '

bash -n <script> # Check syntax without executing
bash --debugger <script>
parent_func=$(caller 0 | cut -d' ' -f2) # "$line $subroutine $filename"
source ~/sctrace.sh # FROM: http://stackoverflow.com/questions/685435/bash-stacktrace/686092

# Redirect logs
exec >>logs/$(basename $0).log.$(date +%Y-%m-%d-%H) 2>&1
# Standard logs date
date "+%F %T,%N" | cut -c-23
# Seconds since EPOCH
date -u +%s

# Set positional parameters $0 $1 ...
set - A B C

# Create and set permissions
install -o $USER -m 644 <file>
install -d -m 777 <directory>

for f in ./*.txt; do; [[ -f "$f" ]] || continue # Safe 'for' loop - http://bash.cumulonim.biz/BashPitfalls.html

: ${1:?'Missing or empty parameter'}
: ${var:="new value set if empty"}
local var=${1:-"default value"}
# !! 'local' is a command, and its return code will shadow the one of the cmd in the right part of an assignment

# Variables substitutions (http://tldp.org/LDP/abs/html/parameter-substitution.html)
echo ${PWD//\//-}

# List all defined variables
( set -o posix; set )

# Floating point arithmetic
echo "1/3" | bc -l # or specify "scale=X;" instead of flag
factor <really-long-int> # decompose in factors

# Script file parent dir
EXEC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

is_true () { ! { [ -z "$1" ] || [[ "$1" =~ 0+ ]] || [[ "$1" =~ [Ff][Aa][Ll][Ss][Ee] ]] ; } ; }

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

/var/tmp is better than /tmp # as filling it is less system impacting
# mktemp dir & default value
tdir="$(mktemp -d ${TMPDIR:-/tmp}/$0_XXXXXX)"
# Use RAM for tmp files:
/dev/shm # monitor usage with ipcs -m

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
local argv=("$@")
# Back to string
str="${argv[*]}"
# Array slice
echo ${argv[@]:1:2}

# Powerful regex
[[ "some string" =~ "$regex" ]]
group1="${BASH_REMATCH[1]}"

# disable wildcard expansion
set -o noglob
# Extended bash globbing
shopt -s extglob # http://www.linuxjournal.com/content/bash-extended-globbing
# list options values
echo $- # Check the shell is interactive: [[ $- =~ i ]]

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

# Syslog (port: 514)
logger -is -t SCRIPT_NAME -p user.warn "Message"
echo "<15>My logline" | nc -u -w 0 127.0.0.1 514 # <15> means 'user.debug', see RFC3164

mv $file ${file%.*}.bak # Change extension
mv --backup=numbered new target # !! --suffix/SIMPLE_BACKUP_SUFFIX can be broken on some distros
logrotate -s /var/log/logstatus /etc/logrotate.conf [-d -f] # Logrotate (to call in a cron job) Examples: http://www.thegeekstuff.com/2010/07/logrotate-examples/

nice / ionice / renice # Control process priority (useful in cron job) 

flock -n /pathi/to/lockfile -c cmd # run cmd only if lock acquired, useful for cron jobs

# Get all commands prefixed by (useful for unit tests)
compgen -abck unit_test_
# Control readline auto-completion : http://linuxcommand.org/man_pages/complete1.html
complete -f -X '!*.ext' command # exclude files using a filter
complete -F _compfunc command
_compfunc() {
    local cmd="${1##*/}"
    local word=${COMP_WORDS[COMP_CWORD]}
    local line=${COMP_LINE}
    local xpat='!*.foo'

    COMPREPLY=($(compgen -f -X "$xpat" -- "${word}"))
}

# Launch command at a specified time or when load average is under 0.8
echo <cmd> | at midnight
echo <cmd> | batch

# control the resources available to the shell and to processes it starts
ulimit -v # max virtual memory
ulimit -s # max stack size
ulimit -t # max of cpu time
ulimit -u # max number of processes


++++++++++++++++++
# Text filtering
++++++++++++++++++

grep -o # output only matching parts
grep -C3 # output 3 lines of context, see also -B/-A
grep -H/-h # output with/without filename
grep -L PATTERN <files> # Get only filenames where PATTERN is not present
grep -P '^((?!b).)*a((?!b).)*$' # Grep 'a' but not 'b' -> PCRE ;  awk '/a/ && !/b/'
grep -P -n "[\x80-\xFF]" file.xml # Find non-ASCII characters
LANG=C grep -F # faster grep : fixed strings + no UTF8 multibyte, ASCII only (significantly better if v < 2.7)

# shows non-printing characters as ascii escapes. 
cat -vET
# echo non-ascii
printf "\177" # octal

printf "%-8s\n" "${value}" # 8 spaces output formatting

# filter outpout : not lines 1-3 and last one
type ssh_setup | sed -n '1,3!p' | sed '$d'| sed 's/local //g'
# this is also a crazy hack : put the output in ORIG_CMD, then redefine ssh_setup () { eval $ORIG_CMD $@; ... }

# Print lines starting with one containing FOO and ending with one containing BAR.
sed -n '/FOO/,/BAR/p'

# Replace newlines by a separator
seq 1 10 | paste -s -d+ | bc
# Break on word per line
perl -pe 's/\s+/\n/g'
# paste is also usefule to interlace files: paste <file1> <file2>

# Longest line of code
perl -ne 'if (length > $w) { $w = length; print $ARGV.":".$_ };  END {print "$w\n"}' *.py

# Print nth column
awk [-F":|="] '{ print $NF }'

# Sets intersec
comm -12 #or uniq -d

# display input to stdout + append to end of <file>
tee -a <file>

fold # breaks lines to proper width
fmt # reformat lines into paragraphs 


=#=#=#=#=#=
   FILES
#=#=#=#=#=#

find / -size +100M -ls # find big/largest files - One can safely ignore /proc/kcore
find -regex 'pat\|tern' # >>>way>more>efficient>than>>> \( -path ./pat -o -path ./tern \) -prune -o -print

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

killall -HUP <process name> # To tell a process to reload its file descriptors, e.g. when deleting a log file

# Sum up kind of files without ext
ls | cut -d . -f 1 | funiq

# Create fake file
sudo dd if=/dev/urandom of=FAKE-2012Oct23-000000.rdb bs=1M count=6000

# Forbid file deletion
sudo chattr +i [-R] <file> # to check a file attributes : lsattr

# Bring back deleted file from limbo (ONLY if still in use in another process)
lsof | grep myfile # get pid
cp /proc/<pid>/fd/4 myfile.saved

# http://www.cyberciti.biz/tips/linux-audit-files-to-see-who-made-changes-to-a-file.html
auditctl -w <file> -p wax -k <tag>
ausearch -k <tag> [-ts today -ui 506 -x cat]

mkfifo # Named pipes: https://en.wikipedia.org/wiki/Named_pipe
python -c "from fcntl import ioctl ; from termios import FIONREAD ; from ctypes import c_int ; from sys import argv ; size_int = c_int() ; fd = open(argv[1]) ; ioctl(fd, FIONREAD, size_int) ; fd.close() ; print size_int.value" <file> # readble bytes in a fifo
ulimit -p # should get max pipe size, but WRONG : defined in pipe_fs_i.h
fcntl(fd, F_SETPIPE_SZ, size) # to change max size, if Linux > 2.6.35 (/proc/sys/fs/pipe-max-size)

man mq_overview # POSIX queues - not fully implemented : can't read/write on them with shell cmds, need C code
beanstalk # Better alternative queuing system, with lots of existing tools & libs in various labguages
ActiveMQ, RQ(Redis), RestMQ(Redis), RabittMQ # Message queue using AMPQ
Celery/Kombu # Framework to use any of the above ones

#Append at the end of stdout (or beginning with ^)
echo ECHO | sed s/$/.ext/

rsync -avz --exclude=".*" --delete # the last option remove extra remote files

sha{1,224,256,384,512}sum
md5sum


|°|°|°|°|°|°|°|°
== NETWORKING
|°|°|°|°|°|°|°|°

mtr <host/ip> # > ping / traceroute

socat > nc/netcat > telnet
socat - udp4-listen:5000,fork # create server redirecting listening on port 5000 output to terminal
nc -l -u -k -w 0 5000
echo hello | socat - udp4:127.0.0.1:5000 # send msg to server
echo hello | nc -u -w 0 127.0.0.1 5000

# Port scanning
nmap <host> -p <port> --reason [-sT|-sU] # TCP/UDP scanning ; -Pn => no host ping, only scanning
nmap -sS -O 127.0.0.1 # Guess OS !!

# Locally
lsof -i -P -p <pid> # -i => list all Internet network files ; -P => no conversion of port numbers to port names for network files ; -n => no IP->hostname resolution

ss -nap # -a => list both listening and non-listening sockets/ports ; -n => no DNS resolution for addresses, use IPs ; -p => get pid & name of process owning the socket
ss -lp [-t|-u] # list only listening TCP/UDP sockets/ports

# Even if 'ss' is the replacement for deprecated 'netstat', the following has no equivalent
netstat --statistics [--udp] # global network statistics

ip n[eighbour] # ARP or NDISC cache entries - replace deprecated 'arp'
ip a[ddr] [show|add <ip>] dev eth0 # replace deprecated 'ifconfig'
ip link set eth0 [up|down] # enable/disable the[interface specified
ip tunnel # replace deprecated 'iptunnel'
ip route # host routing tables - replace deprecated 'route'
iw # details about wireless interfaces - replace deprecated 'iwconfig'

grep -Eo '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}' # grep an IP

lynx -dump -stdin # convert HTML to text
wget --random-wait -r -p -e robots=off -U mozilla http://www.example.com # aspire web page
  -p --page-requisites : download all the files necessary to properly display a page: inlined images, sounds, CSS...
  -k --convert-links : convert the links in the document to make them suitable for local viewing
  --no-parent : do not ever ascend to the parent directory when retrieving recursively
  -A --accept acclist -R --reject rejlist : comma-separated list of filename suffixes or patterns to accept or reject
  -l --level=depth : default = 5
  -c --continue : continue getting a partially-downloaded file
curl #See: http://curl.haxx.se/docs/httpscripting.html

# Iptables
iptables -A INPUT -s <IP_OR_HOSTNAME> -j DROP
iptables -n -L -v

snmpget -v2c -c '<community_string>' <device> sysDescr.0 # or sysUpTime.0, sysName.0
# The community string can be found in the 'Variables' tab in an AutoNOC device page
# SNMP port : 161

# Dump all tcp transmission to a specific IP :
sudo tcpdump -X host $IP [ip proto icmp|udp|tcp]

# On RedHat / CentOS / Fedora
$EDITOR /etc/sysconfig/network-scripts/ifcfg-eth0
$EDITOR /etc/sysconfig/network
/etc/init.d/network restart 

# Query DNS
dig txt [+short] <hostname>
host -t txt <hostname>
nslookup
# Reverse
dig +short -x <IP>

# Keep ssh session open after executing commands
ssh $host "$cmds ; /bin/bash -i"
# How to change your login on a specified acces: http://orgmode.org/worg/worg-git-ssh-key.php
.ssh/config
# Exit a hung SSH session
[ENTER] ~.
openssl s_client # bare SSL client cmd
openssl x509 -text -noout -in <cert.pem> # get certs details
keytool -printcert -file <cert.pem> # get certs details

# Find wireless driver
lspci -vv -s $(lspci | grep -i wireless | awk '{print $1}')

# Non portable tools
iptraf, ntop, rddtool
mininet # realistic virtual network, running real kernel, switch and application code, on a single machine


=cCcCcCc=
# Cisco #
=cCcCcCc=

sh run
sh int
sh ip int [brief]
sh ip rou 1.2.3.4
sh version
exit


-%-%-%-%-%-
 =SYSTEM=
-%-%-%-%-%-

stap # SystemTap

sysctl

cat /etc/*-release
lsb_release -a
uname -a
cat /etc/issue*

/proc/version
/proc/cpuinfo # Number of cores, cache size & alignement...
/proc/loadavg :
- first 3 fields : number of jobs in the run queue (state R) or waiting for disk I/O (state D) averaged over 1, 5, and 15 minutes
- 4th field : number of currently executing kernel scheduling entities (processes, threads) / number of existing kernel scheduling entities
- 5th field : PID of last process created

# People previous logged
last [-f /var/log/wtmp.1]

# System errors
dmesg -s 500000 | grep -i -C 1 "fail\|error\|fatal\|warn\|oom"
# Enable dmesg timestamps
echo 1 > /sys/module/printk/parameters/printk_time 

# Message of the day
/etc/motd

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
umask # Control the permissions a process will give by default to files it creates; useful to avoid temporarily having world-readable files before 'chmoding' them

# Watch system stats
watch -d 'cat /proc/meminfo'

iostat
mpstat 5 # cpu usage stats every 5sec
dstat

# Checking Swap Space Size and Usage
free -m # how much free ram I really have ? -> look at the row that says "-/+ buffers/cache"
vmstat 2
sar
# + to consult history : https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/5/html/Tuning_and_Optimizing_Red_Hat_Enterprise_Linux_for_Oracle_9i_and_10g_Databases/sect-Oracle_9i_and_10g_Tuning_Guide-Swap_Space-Checking_Swap_Space_Size_and_Usage.html

# Frozen X server
sudo service lightdm restart
killall gnome-panel

lspci -v # list devices
lshw -C disk # list disks : ata, cdrom, dvdrom
blkid # list UUIDs
dmidecode

rpm --qf "%{INSTALLTIME:date} %{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}.rpm\n" -qa *regex* # list rpm
rpmbuild file.spec
alien # transformer un .rpm en .deb

init q # Reload /etc/inittab


=\/=/\=\/=/\=\/=
=  Virtualbox
=\/=/\=\/=/\=\/=
sudo adduser $USER vboxusers # then logout
VBoxManage list vms
VBoxManage controlvm <name> poweroff

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
display <img>
convert img.png -adaptive-resize 800x600 -auto-orienti -crop 50x100+10+20 img.jpg
mogrify ... *.jpg # for f in *.jpg; do convert $f ... ; done
identify -v <img> # get PPI: -format "%w x %h %x x %y"
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

sudo softwareupdate -i -a # Manual software update

Finder > Applications > Utilities > Disk Utility # Repair permissions

pmset -g # power management settings 

pbpaste | pbcopy

textutil -convert txt # or -info : convert / get infos on files

xattr -l <file> # File listed with '@' => extended attributes

sudo dseditgroup -o edit -a <USER> -t user <GROUP> # Add user to group

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


=======
= Wiki
=======

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

http://en.wikipedia.org/wiki/Help:Magic_words


::=::=::=::
:: MySQL
::=::=::=::
mysql -h <host> -u <user> -p [--ssl-ca=<file>.pem] # default port 3306

mytop # watch mysql

LIKE >faster> REGEXP

# list tables
show tables;
.tables # SqLite

# List columns
show columns from <table>;

# Kill request
SHOW PROCESSLIST;
KILL <thread_to_be_killed>;

# Get tables informations
SHOW TABLE STATUS;

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
