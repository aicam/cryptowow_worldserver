
import os
import sys
import select
import termios
import tty
import pty
from subprocess import Popen

command = 'bash'
# command = 'docker run -it --rm centos /bin/bash'.split()
pid = pty.fork()
if not pid:
    # is child
    termios.tcgetattr(sys.stdin.fileno())
# save original tty setting then set it to raw mode
# old_tty = termios.tcgetattr(sys.stdin)
# tty.setraw(sys.stdin.fileno())

# open pseudo-terminal to interact with subprocess
master_fd, slave_fd = pty.openpty()

# use os.setsid() make it run in a new process group, or bash job control will not be enabled
p = Popen(command,
          preexec_fn=os.setsid,
          stdin=slave_fd,
          stdout=slave_fd,
          stderr=slave_fd,
          universal_newlines=True)

SERVER_STARTED = False
while p.poll() is None:
    r, w, e = select.select(master_fd, [], [])
    if not SERVER_STARTED:
        os.write(master_fd, "/home/wow/server/bin/worldserver\n".encode())
        SERVER_STARTED = True
        continue
    if master_fd in r:
        o = os.read(master_fd, 10240)
        if o:
            os.write(sys.stdout.fileno(), o)
    gm_cms = open("GMCommands", "r+")
    if gm_cms:
        for cm in gm_cms:
            cm = cm if cm[-1] == "\n" else cm + "\n"
            print(cm)
            os.write(master_fd, cm.encode())
            r, w, e = select.select(master_fd, [], [])
            if master_fd in r:
                o = os.read(master_fd, 10240)
                if o:
                    os.write(sys.stdout.fileno(), o)


# restore tty settings back
# termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)