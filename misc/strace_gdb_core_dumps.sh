mozilla/rr # recording and replaying execution of applications - aspires to be your primary C/C++ debugging tool, replacing gdb

gcc -Wall -fPIC -shared -o myfopen.so myfopen.c
LD_PRELOAD=./myfopen.so cat $file
man ld.so

# Follow p$rogram system calls (man syscalls) !! -f => follow fork
strace -f -p $pid -e open,access,poll,select,connect,recvfrom,sendto [-c] #stats
strace -f -e trace=network -s 10000 $cmd # capture network traffic
# Bug: http://lethargy.org/~jesus/writes/beware-of-strace ; https://bugzilla.redhat.com/show_bug.cgi?id=590172
kill -CONT $pid # strace bug fix
ltrace -ttS -s 65535 -o $logfile -p $pid # log system calls and library calls

cat /proc/$pid/cmdline
cat /proc/$pid/maps # memory map, useful to now which libs are loaded
cat /proc/$pid/smaps # get resources infos
pmap -x $pid # get memory usage
valgrind --tool=massif $cmd # get memory usage with details & graph
valgrind --db-attach=yes --leak-check=full --track-origins=yes # --tool=callgrind / kcachegrind
oprofile

cat hex.txt
000000: b8d1 a3d8 8d56 e389 c69d d8ca 99e0 cd51
000010: ddce aada 8485 958b d1a0 d5cb 94e8 d29d
000020: e56c
xxd -r hex.txt > hex.bin # generate binary from hexa
hexdump -c $file # aka 'hd', use 'bvi' for editing. Alt: od -Ax -tx1z -v $file
strings -n $min_length exec.bin # extract strings of length >= 4
objdump
/dev/mem # Physical memory, useful to strings | grep pswd. Ubuntu limit this to 1Mb
dd if=/dev/fmem of=/tmp/fmem_dump.dd bs=1MB count=10 # don't forget 'count'
nm *.o # list symbols
readelf -Ws *.so
ldd $executable # list dynamically linked libs
Hex-Rays IDA, Radare # disassemblers


# 0xDEADC0DE 0xDEADBEEF
#       Windows
# 0xBADDCAFE 0xD15EA5E
:: Windows Performance Toolkit, also inc. xbootmgr - TUTOS: http://www.msfn.org/board/topic/140263-how-to-get-the-cause-of-high-cpu-usage-by-dpc-interrupt/ - http://www.msfn.org/board/topic/140264-how-to-get-the-cause-of-high-cpu-usage-caused-by-apps/
xperf -on latency -stackwalk profile
xperf -d latency.etl
wtrace :: strace-like based on Event Tracing for Windows


# 0xDEADC0DE 0xDEADBEEF
#          GDB
# 0xBADDCAFE 0xD15EA5E
# Alt: Oracle dbx

ulimit -c # check if core dumps are enabled
ulimit -S -c unlimited && echo 'kernel.core_pattern = /tmp/core2' >>/etc/sysctl.conf # enable core dumps
gdb -tui $prog /tmp/core.$pid # post-mortem debug of a prog compiled with -g
gcore $pid # memory core dump

gdb --args cmd cmd_arg1 cmd_arg2
# get a core file for a running program
gdb -p $pid -batch -quiet -ex 'generate-core-file' # then manipulate with pstack, pmap
# get a stack trace for all threads
gdb -p $pid -batch -quiet -ex "thread apply all bt full" > program-backtrace.log

(gdb) help // or 'apropos'
(gdb) run // or 'start' to add a breakpoint at the beggining
(gdb) show env // also: 'show args', 'show inferior-tty' (all also be modified)
(gdb) step/next/until
(gdb) b $position [if $condition] // for a one-time breakpoint: 'tbreak'; Also: 'info break', 'clear $breakpoint_position'
// $position can be [$file:]$line_number, relative number of lines (e.g. +5), function name
(gdb) enable/disable/delete $breakpoint_id
(gdb) command $breakpoint_id // run a command each time you hit the breakpoint
print var
end
(gdb) watch $variable // watch point; also: rwatch/awatch triggered when $variable is read/modified 1st
(gdb) p[/$format] $variable // use *address@size to display arrays
// formats: o(octal), x(hex), d(decimal), u(unsigned decimal), t(binary), f(float), a(address), i(instruction), c(char), s(string)
(gdb) show values // show history
(gdb) info [all-]registers
(gdb) x[/$length$format] $address // 'examine' memory
(gdb) set $variable = $value
(gdb) where [full] // aka 'backtrace'
(gdb) up/down // also: 'frame $frame_id'
(gdb) call foo(42) // also: 'jump $position'
(gdb) return [$value]
(gdb) kill
(gdb) directory path/to/src/files/dir // link debug symbols with relative paths to source files - For absolute paths: substitue-path
(gdb) macro expand / info macro // require make KCFLAGS=-ggdb3

set disassembly-flavor intel # Intel syntax is better
set disassemble-next-line on
catch syscall ptrace #Catch the syscall.
commands 1
set ($eax) = 0
continue
end


0101010101010101010
010 Python support
0101010101010101010
cyrus-and/gdb-dashboard  # modular visual interface for GDB in Python

# First, just try on of those:
yum install gdb python-debuginfo
apt-get install gdb python2.7-dbg

curl https://hg.python.org/cpython/raw-file/default/Tools/gdb/libpython.py > ~/gdb_libpython.py
curl https://hg.python.org/cpython/raw-file/default/Misc/gdbinit >> ~/.gdbinit # Latest is http://svn.python.org/projects/python/trunk/Misc/gdbinit but it gives a 'No symbol "_PyUnicode_AsString" in current context'
sed -i 's/printf "%d", $__li/printf "%d", $__li + 1/' ~/.gdbinit
cat <<END >> ~/.gdbinit
# Custom configuration by USER=$USER
add-auto-load-safe-path ~/gdb_libpython.py
## Persistent history
set history save
set history filename ~/.gdb_history
## Colored prompt, trick src: http://dirac.org/linux/gdb/ - Alt: http://reverse.put.as/gdbinit/
set prompt \001\033[1;32m\002(gdb)\001\033[0m\002\040
END

echo 0 > /proc/sys/kernel/yama/ptrace_scope # in case GDB fails attaching to a process with "ptrace: Operation not permitted". >>>better>>than>> sudo chmod +s /usr/bin/gdb
sudo chown root:root ~/.gdbinit  # I used that once as a fix

gdb -p $pid # attach gdb
pystack / py-bt

Perfmon / objgraph / VMMap / umdh # debug tools to track memory leaks: https://benbernardblog.com/tracking-down-a-freaky-python-memory-leak/
