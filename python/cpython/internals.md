# Links

* http://eli.thegreenplace.net/2012/04/16/python-object-creation-sequence/

# [Modules/gcmodule.c](http://hg.python.org/cpython/file/tip/Modules/gcmodule.c)

## About untracking of immutable objects

Certain types of container cannot participate in a reference cycle, and
so do not need to be tracked by the garbage collector. Untracking these
objects reduces the cost of garbage collections. However, determining
which objects may be untracked is not free, and the costs must be
weighed against the benefits for garbage collection.

There are two possible strategies for when to untrack a container:

1. When the container is created.
2. When the container is examined by the garbage collector.

Tuples containing only immutable objects (integers, strings etc, and
recursively, tuples of immutable objects) do not need to be tracked.
The interpreter creates a large number of tuples, many of which will
not survive until garbage collection. It is therefore not worthwhile
to untrack eligible tuples at creation time.

Instead, all tuples except the empty tuple are tracked when created.
During garbage collection it is determined whether any surviving tuples
can be untracked. A tuple can be untracked if all of its contents are
already not tracked. Tuples are examined for untracking in all garbage
collection cycles. It may take more than one cycle to untrack a tuple.

Dictionaries containing only immutable objects also do not need to be
tracked. Dictionaries are untracked when created. If a tracked item is
inserted into a dictionary (either as a key or value), the dictionary
becomes tracked. During a full garbage collection (all generations),
the collector will untrack any dictionaries whose contents are not
tracked.

The module provides the python function `is_tracked(obj)`, which returns
the *CURRENT* tracking status of the object. Subsequent garbage
collections may change the tracking status of the object.

Untracking of certain containers was introduced in
[issue #4688](http://bugs.python.org/issue4688), and the algorithm was refined
in response to [issue #14775](http://bugs.python.org/issue14775).

### Links

* [Issue14775 - Dict untracking can result in quadratic dict build-up](http://bugs.python.org/issue14775)
* http://hg.python.org/cpython/rev/7951900afd00

---

# Float in CPython

Floats sometimes give results which puzzle naive users.

```py
py> L = [1/10]*10
py> print(L)
[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
py> sum(L)  # should be 1.0
0.9999999999999999
```

## Why doesn't Python add up correctly?

And so we have to explain that the float 0.1 is not actually 0.1 because
you can't represent 0.1 as a finite binary fraction, due to some fairly
subtle mathematics that goes right past most people. The float 0.1 is
actually a tiny bit *larger* than the decimal 0.1, but when you add ten of
them together, you end up with a number that it a tiny bit *smaller* than
the expected result.

## Don't you just love binary floating point?

Matthew used a smiley there, but I think there is a very strong case for
making the default floating point numeric type Decimal rather than float.
Decimals behave more like people expect, and they interact better with
other numeric types (ints and Fractions) than floats.

### Links

* http://mail.python.org/pipermail/python-ideas/2012-September/016235.html
