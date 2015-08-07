# GIL

## The *new* GIL

(Notes from the Antoine Pitrou's python-dev thread)

...releasing the GIL every 100 opcodes, regardless of their length, is a
very poor policy.

The new GIL does away with this by ditching `_Py_Ticker` entirely and
instead using a fixed interval (by default 5 milliseconds, but settable)
after which we ask the main thread to release the GIL and let another
thread be scheduled.

http://mail.python.org/pipermail/python-dev/2009-October/093321.html

### Implementation

* `Python/ceval_gil.h`:
  http://svn.python.org/view/sandbox/trunk/newgil/Python/ceval_gil.h?view=log
* `Python/ceval.c`:
  http://svn.python.org/view/sandbox/trunk/newgil/Python/ceval.c?view=log

## Notes

**Advantages:**

* Increased speed of single-threaded programs compared to single-threaded
  programs that automatically perform some other fine-grained (and
  equally redundant) locking.
* Easy integration of C libraries that usually are not thread-safe.

Python has a GIL as opposed to fine-grained locking for several reasons:

* It is faster in the single-threaded case.
* It is faster in the multi-threaded case for i/o bound programs.
* It is faster in the multi-threaded case for cpu-bound programs that do
  their compute-intensive work in C libraries.
* It makes C extensions easier to write: there will be no switch of
  Python threads except where you allow it to happen (i.e. between the
  `Py_BEGIN_ALLOW_THREADS` and `Py_END_ALLOW_THREADS` macros).
* It makes wrapping C libraries easier. You don't have to worry about
  thread-safety. If the library is not thread-safe, you simply keep the
  GIL locked while you call it.

From Python C API documentation:

> The Python interpreter is not fully thread-safe.

In CPython, the global interpreter lock, or GIL, is a mutex that
prevents multiple native threads from executing Python bytecodes at once.
This lock is necessary mainly because CPython's memory management is not
thread-safe.

The GIL is controversial because it prevents multithreaded CPython
programs from taking full advantage of multiprocessor systems in certain
situations. Note that potentially blocking or long-running operations,
such as I/O, image processing, and NumPy number crunching, happen outside
the GIL. Therefore it is only in multithreaded programs that spend a lot
of time inside the GIL, interpreting CPython bytecode, that the GIL
becomes a bottleneck.

The GIL is a problem if, and only if, you are doing CPU-intensive work
in pure Python. Here you can get cleaner design using processes and
message-passing.

Reference: http://programmers.stackexchange.com/a/186909
