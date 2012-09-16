# Python’s super() considered super!

* [Python 2 syntax](http://code.activestate.com/recipes/577721-how-to-use-super-effectively-python-27-version/)
* [Python 3 syntax](http://code.activestate.com/recipes/577720-how-to-use-super-effectively/)

Using Python 3 syntax, let’s start with a basic use case, a subclass for
extending a method from one of the builtin classes:

```py
class LoggingDict(dict):
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super().__setitem__(key, value)
```

This class has all the same capabilities as its parent, `dict`, but it extends
the `__setitem__` method to make log entries whenever a key is updated. After
making a log entry, the method uses `super()` to delegate the work for actually
updating the dictionary with the key/value pair.

Before `super()` was introduced, we would have hardwired the call with
`dict.__setitem__(self, key, value)`. However, `super()` is better because it is
a computed indirect reference.

One benefit of indirection is that we don’t have to specify the delegate class
by name. If you edit the source code to switch the base class to some other
mapping, the `super()` reference will automatically follow. You have a single
source of truth:

```py
class LoggingDict(SomeOtherMapping):  # new base class
    def __setitem__(self, key, value):
        logging.info('Setting %r to %r' % (key, value))
        super().__setitem__(key, value)  # no change needed
```

The calculation depends on both the class where `super()` is called and on the
instance’s tree of ancestors. The first component, the class where super is
called, is determined by the source code for that class. In our example,
`super()` is called in the `LoggingDict.__setitem__` method. That component is
fixed. The second and more interesting component is variable (we can create new
subclasses with a rich tree of ancestors).

Let’s use this to our advantage to construct a logging ordered dictionary
without modifying our existing classes:

```py
class LoggingOD(LoggingDict, collections.OrderedDict):
    pass
```

The ancestor tree for our new class is: `LoggingOD`, `LoggingDict`,
`OrderedDict`, `dict`, `object`. For our purposes, the important result is that
`OrderedDict` was inserted after `LoggingDict` and before `dict`! This means
that the `super()` call in `LoggingDict.__setitem__` now dispatches the
key/value update to `OrderedDict` instead of `dict`.

Think about that for a moment. We did not alter the source code for
`LoggingDict`. Instead we built a subclass whose only logic is to compose two
existing classes and control their search order.

## Search order

What I’ve been calling the search order or ancestor tree is officially known as
the **Method Resolution Order** or MRO. It’s easy to view the MRO by printing
the `__mro__` attribute:

```py
>>> pprint(LoggingOD.__mro__)
(<class '__main__.LoggingOD'>,
 <class '__main__.LoggingDict'>,
 <class 'collections.OrderedDict'>,
 <class 'dict'>,
 <class 'object'>)
```

If our goal is to create a subclass with an MRO to our liking, we need to know
how it is calculated. The basics are simple. The sequence includes the class,
its base classes, and the base classes of those bases and so on until reaching
`object` which is the root class of all classes. The sequence is ordered so that
a class always appears before its parents, and if there are multiple parents,
they keep the same order as the tuple of base classes.

The MRO shown above is the one order that follows from those constraints:

* `LoggingOD` precedes its parents, `LoggingDict` and `OrderedDict`
* `LoggingDict` precedes `OrderedDict` because `LoggingOD.__bases__` is
  `(LoggingDict, OrderedDict)`
* `LoggingDict` precedes its parent which is `dict`
* `OrderedDict` precedes its parent which is `dict`
* `dict` precedes its parent which is `object`

The process of solving those constraints is known as linearization. There are a
number of good papers on the subject, but to create subclasses with an MRO to
our liking, we only need to know the two constraints: children precede their
parents and the order of appearance in `__bases__` is respected.
