## Use cases

* The primary use cases for sets don't need order.  The main use cases being:
  uniquification, fast membership testing, and classic set-to-set operations
  (union, intersection, and difference).
* The primary benefit of an ordered set is that it is easier on the eyes when
  interactively experimenting with trivial schoolbook examples.  That said, an
  OrderedSet `__repr__` looks uglier because it would lack the `{10, 20, 30}`
  style literals we have for regular sets).

Reference: https://mail.python.org/pipermail/python-ideas/2015-February/031699.html
