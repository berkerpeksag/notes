## PID 1 and zombie processes

Process ID 1, which is normally the UNIX ‘init’ process, has a special role in
the operating system. That is that when the parent of a process exits prior to
its child processes, and the child processes therefore become orphans, those
orphaned child processes have their parent process remapped to be process ID 1.
When those orphaned processes then finally exit and their exit status is
available, it is the job of the process with process ID of 1, to acknowledge
the exit of the child processes so that their process state can be correctly
cleaned up and removed from the system kernel process table.

If this cleanup of orphaned processes does not occur, then the system kernel
process table will over time fill up with entries corresponding to the orphaned
processes which have exited. Any processes which persist in the system kernel
process table in this way are what are called **zombie processes**. They will
remain there so long as no process performs the equivalent of a system
`waitpid()` call on that specific process to retrieve its exit status and so
acknowledge that the process has terminated.

**Source:** http://blog.dscpl.com.au/2015/12/issues-with-running-as-pid-1-in-docker.html
