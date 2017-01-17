import os
import time

child_pid = os.fork()

if child_pid == 0:
    print('[child] child_pid:', child_pid)
    print('[child] process ID:', os.getpid())
    print('[child] parent process ID:', os.getppid())
    # We can also put a sleep() call here, and then play with
    # a tool like ps or pstree to see how it works
    time.sleep(2)
else:
    os.waitpid(child_pid, 0)
    print('[parent] child_pid:', child_pid)
    print('[parent] process ID:', os.getpid())
