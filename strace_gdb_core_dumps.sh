gcc -Wall -fPIC -shared -o myfopen.so myfopen.c
LD_PRELOAD=./myfopen.so cat $file
man ld.so

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

hexdump -c # aka 'hd', use 'bvi' for editing
strings -n $min_length exec.bin # extract strings of length >= 4
objdump
/dev/mem # Physical memory, useful to strings | grep pswd. Ubuntu limit this to 1Mb
dd if=/dev/fmem of=/tmp/fmem_dump.dd bs=1MB count=10 # don't forget 'count'
nm *.o # list symbols
readelf -Ws *.so
ldd $executable # list dynamically linked libs


# 0xDEADC0DE 0xDEADBEEF
#          GDB
# 0xBADDCAFE 0xD15EA5E
curl -s http://svn.python.org/projects/python/trunk/Misc/gdbinit > ~/.gdbinit
sudo chown root:root ~/.gdbinit
gdb -p $PID # attach gdb
pystack # get the python stack trace

ulimit -c # check if core dumps are enabled
ulimit -S -c unlimited && echo 'kernel.core_pattern = /tmp/core2' >>/etc/sysctl.conf # enable core dumps
gdb $prog /tmp/core.$PID # post-mortem debug of a prog compiled with -g

# get a core file for a running program
gdb -batch -quiet -ex 'generate-core-file' -p PROGRAMPID # then manipulate with pstack, pmap
# get a stack trace for all threads
gdb -batch -quiet -ex "thread apply all bt full" -p PROGRAMPID > program-backtrace.log

(gdb) help // or 'apropos'
(gdb) run // or 'start' to add a breakpoint at the beggining
(gdb) show env // also: 'show args', 'show inferior-tty' (all also be modified)
(gdb) step/next/until
(gdb) b $position [if $condition] // for a one-time breakpoint: 'tbreak'; Also: 'info break', 'clear $breakpoint_position'
// $position can be [$file:]$line_number, relative number of lines (e.g. +5), function name
(gdb) enable/disable/delete $breakpoint_id
(gdb) watch $variable // watch point; also: rwatch/awatch triggered when $variable is read/modified 1st
(gdb) p[/$format] $variable // use *address@size to display arrays
(gdb) show values // show history
(gdb) info [all-]registers
(gdb) x[/$length$format] // 'examine' memory
(gdb) set $variable = $value
(gdb) where [full] // aka 'backtrace'
(gdb) up/down // also: 'frame $frame_id'
(gdb) call foo(42) // also: 'jump $position'
(gdb) return [$value] 
(gdb) kill

