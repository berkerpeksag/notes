# Unix tricks in Unicorn

## `fork(2)`

What's a system call? A way to communicate with the kernel of our operating
system. System calls are the API of the kernel, if you will. We tell the
kernel to do something for our us with system calls: reading, writing,
allocating memory, networking, device management.

And fork is the system call that tells the kernel to create a new process.
When one process asks the kernel for a new process with `fork(2)` the kernel
splits the process making the call into two.

As soon as the kernel returns control to the process after handling the system
call there now is a parent process and a child process. A parent can have a
lot of child processes, but a child process only one parent process.

And both processes, parent and child, are pretty much the same, right after
the creation of the child. That's because child processes in a Unix system
inherit a lot of stuff from their parent processes:

* the data (the code it's executing)
* the stack
* the heap
* the user id
* the working directory
* open file descriptors
* the connected terminal and a lot more

```py
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
```

When Unicorn boots up it calls the `spawn_missing_workers` method, which
contains this piece of code:

```rb
worker_nr = -1
until (worker_nr += 1) == @worker_processes
  WORKERS.value?(worker_nr) and next
  worker = Worker.new(worker_nr)
  before_fork.call(self, worker)
  if pid = fork
    WORKERS[pid] = worker
    worker.atfork_parent
  else
    after_fork_internal
    worker_loop(worker)
    exit
  end
end
```

Unicorn calls this method with `@worker_processes` set to the number of
workers we told it to boot up. It then goes into a loop and calls fork that
many times.

Unicorn then checks the return value of fork so see if its now executing in
the parent and in the child process. **Remember:** a forked process inherits
the data of the parent process! A child process executes the same code as the
parent, and we have to check for that in order to have the child do something
else.

If fork returned in the parent process, Unicorn saves the newly created
`worker` object with PID of the newly created child process in the `WORKERS`
hash constant, calls a callback and starts the loop again.

In the child process another callback is called and then the child goes into
its main loop, the `worker_loop`. If the worker loop should somehow return the
child process exits and is done.


## `pipe(2)`

`pipe(2)` is exactly what shells are using.

Remember the saying that under Unix *"everything is a file"*? Well, pipes are
files too. One pipe is nothing more than two file descriptors.

A file descriptor is a number that points to an entry in the file table
maintained by the kernel for each running process. In the case of pipes the
two file table entries do not point to files on a disk, but rather to a memory
buffer to which you can write and from which you can read with both ends of
the pipe.

One of the file descriptors returned by `pipe(2)` is the read-end and the
other one is the write-end. That's because pipes are half duplex – the data
only flows in one direction.

Outside of the shell pipes are heavily used for inter-process communication.
One process writes to one end, and another process reads from the other end.
How? Remember that a child process inherits a lot of stuff from its parent
process? That includes file descriptors! And since pipes are just file
descriptors, child processes inherit them.

If we open a pipe with `pipe(2)` in a parent process and then call `fork(2)`,
both the parent and the child process have access to the same file descriptors
of the pipe.

```py
import os

read_fd, write_fd = os.pipe()

child_pid = os.fork()

if child_pid == 0:
    os.close(read_fd)

    with open(write_fd, "w") as write_end:
        write_end.write("hello from your child!")
else:
    os.close(write_fd)
    os.waitpid(child_pid, 0)

    with open(read_fd) as read_end:
        message = read_end.read()
    print("received from child:", message)
```

Since just after the call to `fork` both processes have both pipe file
descriptors we need to close the end of the pipe we're not going to need. In
the child process that's the read-end and in the parent it’s the write-end.

This is the exact same concept a shell uses to make the pipe-character work.
It creates a pipe, it forks (once for each process on one side of the pipe)
then uses `dup2(2)` to turn the write-end of the pipe into `STDOUT` and the
read-end into `STDIN` respectively and then executes different programs which
are now connected through a pipe.

Unicorn uses pipes a lot.

First of all, there is a pipe between each worker process and the master
process, with which they communicate. The master process writes command to the
pipe (something like `QUIT`) and the child process then reads the commands and
acts upon them.

Communication between the master and its worker processes through pipes.

Then there's another pipe the master process only uses internally and not for
IPC, but for signal handling. It's called the "self-pipe".


## Sockets and `select(2)`

There are a ton of different sockets: TCP sockets, UDP sockets, SCTP sockets,
Unix domain sockets, raw sockets, datagram sockets, and so on. But there is one
thing they all have in common: they are files. Just like a pipe, a socket is
a file descriptor, from which you can read and write to just like with a file.

The basic lifecycle of a server socket looks like this:

1. First we ask the kernel for a socket with the `socket(2)` system call. We
   specify the family of the socket (IPv4, IPv6, local), the type (stream,
   datagram) and the protocol (TCP, UDP, ...). The kernel then returns a file
   descriptor, a number, which represents our socket.
2. Then we need to call `bind(2)`, to bind our socket a network address and
   a port. After that we need to tell the kernel that our socket is a server
   socket, that will accept new connections, by calling `listen(2)`. So now the
   kernel forwards incoming connections to us.
3. Now that our socket is a real server socket and waiting for new incoming
   connections we can call `accept(2)`, which accepts connections and returns
   a new socket. This new socket represents the connection. We can read from it
   and write to it.

But here's the thing: `accept(2)` is a blocking call. It only returns if the
kernel has a new connection for us. A server that doesn't have too many
incoming connections will be blocking for a long time on `accept(2)`.

This is where `select(2)` comes into play.

`select(2)` is a pretty old and famous Unix system call for working with file
descriptors. It allows us to do multiplexing: we can monitor several file
descriptors with `select(2)` and let the kernel notify us as soon as one of
them has changed its state. And since sockets are file descriptors too, we can
use `select(2)` to work with multiple sockets:

```py
import os
import select
import socket

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.bind(('0.0.0.0', 8888))
sock1.listen(10)
sock2.bind(('0.0.0.0', 9999))
sock2.listen(10)

for _ in range(5):
    child_pid = os.fork()
    if child_pid == 0:
        # We could wrap this block with
        # ``try: ... except KeyboardInterrupt: sys.exit()``
        # to avoid printing tracebacks to the console.
        while True:
            readable, _, _ = select.select([sock1, sock2], [], [])
            connection, _ = readable[0].accept()
            with connection.makefile() as fobj:
                print('[%d] %s' % (os.getpid(), fobj.read().strip()))
            connection.close()

os.waitpid(-1, 0)
```

Before master process calls fork to create the worker processes, it calls
socket, bind and listen to create one or more listening sockets. It also
creates the pipes that will be used to communicate with the worker processes.

After forking, the workers, of course, have inherited both the pipe and the
listening sockets. Because, after all, sockets and pipes are file descriptors.

The workers then call `select(2)` as part of their `worker_loop` with both the
pipe and the sockets as arguments. Now, whenever a connection comes in, one of
the workers' call to `select(2)` returns and this worker handles the connection
by reading the request and passing it to the Rack/Rails application.


## Signals

Signals are another way to do IPC under Unix. We can send signals to processes
and we can receive them.

If we send a signal to the process, the kernel delivers it for us and makes the
process jump to the code that deals with receiving this signal, effectively
interrupting the current code flow of the process. Signals are asynchronous
— we don't have to block somewhere to send or receive a signal.

Ignoring signals has one limitation: we can't ignore `SIGKILL` and
`SIGSTOP`, since there has to be a way for an administrator to kill and stop
a process.

A lot of Unix programs do some clean-up work (remove temp files, write to
a log, kill child processes) when receiving `SIGQUIT`. That's done by catching
the signal and defining an appropriate signal handler, that does the clean-up
work. Catching signals has the limitations that ignoring signals has: we can't
catch `SIGKILL` and `SIGSTOP`.

---

#### The self-pipe trick

Richard Stevens's 1992 book *Advanced programming in the Unix environment* says
that you can't safely mix `select()` or `poll()` with `SIGCHLD` (or other
signals). The `SIGCHLD` might go off while `select()` is starting, too early to
interrupt it, too late to change its timeout.

Solution: the self-pipe trick. Maintain a pipe and select for readability on
the pipe input. Inside the `SIGCHLD` handler, write a byte (non-blocking, just
in case) to the pipe output.

**Reference:** http://cr.yp.to/docs/selfpipe.html

---

#### How a shell launches `vim`

The shell calls `fork(2)` to create a child process and then it calls
`execve(2)` with the path to the Vim executable. Without the call to
`execve(2)` we'd end up with a lot of copies of the original shell process
when trying to start programs.

---

**Reference:** http://thorstenball.com/blog/2014/11/20/unicorn-unix-magic-tricks/
