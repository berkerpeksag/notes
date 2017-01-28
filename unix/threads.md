### Drawbacks of threads

* Serialize on memory operations.
* Share the same file descriptor table.

  There is locking involved making changes and performing lookups in this
  table, which stores stuff like file offsets, and other flags.

  Every system call made that uses this table such as `open()`, `accept()`,
  `fcntl()` must lock it to translate `fd` to internal file handle, and when
  make changes.
* Share some scheduling attributes.

  Processes are constantly evaluated to determine the load they're putting on
  the system, and scheduled accordingly.

  Lots of threads implies a higher CPU load, which the scheduler typically
  dislikes, and it will increase the response time on events for that process
  (such as reading incoming data on a socket).
* May share some writable memory.

  Any memory being written to by multiple threads (especially slow if it
  requires fancy locking), will generate all kinds of cache contention and
  convoying issues.

  For example heap operations such as `malloc()` and `free()` operate on a
  global data structure (that can to some degree be worked around).
* Share signal handling, these will interrupt the entire process while they're
  handled.


### Processes or Threads

* If you want to make debugging easier, use threads.
* If you are on Windows, use threads. (Processes are extremely heavyweight in
  Windows).
* If stability is a huge concern, try to use processes.
* If your threads share resources that can't be use from multiple processes,
  use threads. (Or provide an IPC mechanism to allow communicating with the
  "owner" thread of the resource).
* If you use resources that are only available on a one-per-process basis,
  obviously use processes.
* One of the biggest differences between threads and processes is this: Threads
  use software constructs to protect data structures, processes use hardware
  (which is significantly faster).

**Source:** http://stackoverflow.com/a/3705919
