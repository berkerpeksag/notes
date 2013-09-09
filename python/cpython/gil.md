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
