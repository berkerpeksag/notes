# Notes about file descriptors

* Files are opened by the OS, which keeps a system-wide table of open files,
  some of which may point to the same underlying disk data.
* File descriptors are another abstraction, which is managed per-process.
  Each process has its own table of open file descriptors that point into the
  system-wide table.
* File descriptors allow sharing open files between processes (for example
  when creating child processes with fork).
* They're also useful for redirecting from one entry to another. Suppose
  that we make file descriptor 5 a copy of file descriptor 4. Then all writes
  to 5 will behave in the same way as writes to 4.
* You can read and write to them with the `read` and `write` system calls,
  but this is not the way things are typically done. The C runtime library
  provides a convenient abstraction around file descriptors - streams. These
  are exposed to the programmer as the opaque `FILE` structure with a set of
  functions that act on it (for example `fprintf` and `fgets`).
* `FILE` holds a file descriptor to which the actual system calls are
  directed, and it provides buffering, to ensure that the system call (which
  is expensive) is not called too often. Suppose you emit stuff to a binary
  file, a byte or two at a time. Unbuffered writes to the file descriptor with
  write would be quite expensive because each write invokes a system call. On
  the other hand, using `fwrite` is much cheaper because the typical call to
  this function just copies your data into its internal buffer and advances a
  pointer. Only occasionally (depending on the buffer size and flags) will an
  actual write system call be issued.
* `stdout` is a global `FILE` object kept for us by the C library, and it
  buffers output to file descriptor number 1. Calls to functions like `printf`
  and `puts` add data into this buffer. `fflush` forces its flushing to the
  file descriptor, and so on.
* Python and a C extension loaded by it (this is similarly relevant to C code
  invoked via ctypes) run in the same process, and share the underlying file
  descriptor for standard output.

  However, while Python has its own high-level wrapper around it -
  `sys.stdout`, the C code uses its own `FILE` object. Therefore, simply
  replacing `sys.stdout` cannot, in principle, affect output from C code. To
  make the replacement deeper, we have to touch something shared by the
  Python and C runtimes - the file descriptor.

**Reference:** http://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python/
