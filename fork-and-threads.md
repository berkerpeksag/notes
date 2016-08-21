# Using fork and threads

1. Only use fork to immediately call exec. This is the least error-prone.
   However, you really do need to immediately call exec. Most other functions,
   including malloc, are unsafe.

   If you do need to do some complex work, you must do it in the parent, before
   the fork.
2. Fork a worker at the beginning of your program, before there can be other
   threads. You then tell this worker to fork additional processes. You must
   ensure that nothing accidentally starts a thread before this worker is
   started.

**Reference:** http://www.evanjones.ca/fork-is-dangerous.html

The problem is taking two abstractions which don't work in combination, and
supporting both of them at the same time, without doing anything to resolve
the conflict.

**Reference:** http://www.evanjones.ca/fork-is-dangerous.html#comment-2842308168


# Why threads and fork() don't mix

When threads were introduced, kernel authors had to make a choice: should
`fork()` only fork the calling thread, or should it fork *all* threads in the
calling process?

In retrospect, it is obvious that forking all threads is a bad idea. Imagine
that one thread (not the one calling `fork()`) is just about to do I/O (write
something to a socket). Then, immediately after `fork()`, imagine that that
thread would start running in both parent and child; now you end up with the
data written twice to the socket. Bad. So we're left with one sensible choice:
fork just the calling thread.

Now, what happens if another thread in the parent holds a mutex? That mutex
will be held in the child and no one will be around to release it, so, if the
child needs to call a function that needs to acquire the same mutex, the child
will deadlock. **The mutex could be something outside of your control --
something deep inside a library.**

Let's release all mutexes on `fork()`. This is another obviously bad idea: the
thread that holds the mutex presumably did so for a reason, so it's in the
middle of a critical section, which means that some data structures are likely
to be in an inconsistent state at the time of the fork, so the child can't use
them safely.

The most common use of `fork()` is to spawn a subprocess, in which case you
should use `vfork()` instead.

**Reference:** https://cppwisdom.quora.com/Why-threads-and-fork-dont-mix


# Why threads can't fork

Whenever a new child process is created with `fork(2)` the new process gets a
new memory address space but everything in memory is copied from the old
process (with copy-on-write that’s not 100% true, but the semantics are the
same).

If we call `fork(2)` in a multi-threaded environment the thread doing the call
is now the main-thread in the new process and all the other threads, which ran
in the parent process, are dead. And everything they did was left exactly as it
was just before the call to `fork(2)`.

Let’s say our main thread (the one which is going to call `fork(2)`) was
sleeping while we had lots of other threads happily doing some work. Allocating
memory, writing to it, copying from it, writing to files, writing to a database
and so on. They were probably allocating memory with something like
`malloc(3)`. Well, it turns out that `malloc(3)` uses a mutex internally to
guarantee thread-safety. And exactly this is the problem.

What if one of these threads was using `malloc(3)` and has acquired the lock of
the mutex in the exact same moment that the main-thread called `fork(2)`? In
the new child process the lock is still held - by a now-dead thread, who will
never return it.

The new child process will have no idea if it’s safe to use `malloc(3)` or not.
In the worst case it will call `malloc(3)` and block until it acquires the
lock, which will never happen, since the thread who’s supposed to return it is
dead. And this is just `malloc(3)`. Think about all the other possible mutexes
and locks in database drivers, file handling libraries, networking libraries
and so on.

**Reference:** http://thorstenball.com/blog/2014/10/13/why-threads-cant-fork/
