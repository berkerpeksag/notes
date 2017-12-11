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

## Practical Advice

`super()` is in the business of delegating method calls to some class in the
instance’s ancestor tree. For reorderable method calls to work, the classes need
to be designed cooperatively. This presents three easily solved practical
issues:

* the method being called by `super()` needs to exist
* the caller and callee need to have a matching argument signature
* and every occurrence of the method needs to use `super()`

1) Let’s first look at strategies for getting the caller’s arguments to match
the signature of the called method. This is a little more challenging than
traditional method calls where the callee is known in advance. With `super()`,
the callee is not known at the time a class is written (because a subclass
written later may introduce new classes into the MRO).

One approach is to stick with a fixed signature using positional arguments. This
works well with methods like `__setitem__` which have a fixed signature of two
arguments, a key and a value. This technique is shown in the `LoggingDict`
example where `__setitem__` has the same signature in both `LoggingDict` and
`dict`.

A more flexible approach is to have every method in the ancestor tree
cooperatively designed to accept keyword arguments and a keyword-arguments
dictionary, to remove any arguments that it needs, and to forward the remaining
arguments using `**kwds`, eventually leaving the dictionary empty for the final
call in the chain.

Each level strips-off the keyword arguments that it needs so that the final
empty `dict` can be sent to a method that expects no arguments at all (for
example, `object.__init__` expects zero arguments):

```py
class Shape:
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)

cs = ColoredShape(color='red', shapename='circle')
```

2) Having looked at strategies for getting the caller/callee argument patterns
to match, let’s now look at how to make sure the target method exists.

The above example shows the simplest case. We know that object has an `__init__`
method and that object is always the last class in the MRO chain, so any
sequence of calls to `super().__init__` is guaranteed to end with a call to
`object.__init__` method. In other words, we’re guaranteed that the target of
the `super()` call is guaranteed to exist and won’t fail with an
`AttributeError`.

For cases where object doesn’t have the method of interest (a `draw()` method
for example), we need to write a root class that is guaranteed to be called
before object. The responsibility of the root class is simply to eat the method
call without making a forwarding call using `super()`.

`Root.draw` can also employ
[defensive programming](http://en.wikipedia.org/wiki/Defensive_programming)
using an assertion to ensure it isn’t masking some other `draw()` method later
in the chain.  This could happen if a subclass erroneously incorporates a class
that has a `draw()` method but doesn’t inherit from `Root.`:

```py
class Root:
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)

    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)

    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()
```

If subclasses want to inject other classes into the MRO, those other classes
also need to inherit from `Root` so that no path for calling `draw()` can reach
object without having been stopped by `Root.draw`. This should be clearly
documented so that someone writing new cooperating classes will know to subclass
from Root. This restriction is not much different than Python’s own requirement
that all new exceptions must inherit from `BaseException`.

3) The techniques shown above assure that `super()` calls a method that is known
to exist and that the signature will be correct; however, we’re still relying on
`super()` being called at each step so that the chain of delegation continues
unbroken. This is easy to achieve if we’re designing the classes cooperatively
– just add a `super()` call to every method in the chain.

The three techniques listed above provide the means to design cooperative
classes that can be composed or reordered by subclasses.

## How to Incorporate a Non-cooperative Class

Occasionally, a subclass may want to use cooperative multiple inheritance
techniques with a third-party class that wasn’t designed for it (perhaps its
method of interest doesn’t use `super()` or perhaps the class doesn’t inherit
from the root class). This situation is easily remedied by creating an adapter
class that plays by the rules.

For example, the following `Moveable` class does not make `super()` calls, and
it has an `__init__()` signature that is incompatible with `object.__init__`,
and it does not inherit from `Root`:

```py
class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        print('Drawing at position:', self.x, self.y)
```

If we want to use this class with our cooperatively designed `ColoredShape`
hierarchy, we need to make an adapter with the requisite `super()` calls:

```py
class MoveableAdapter(Root):
    def __init__(self, x, y, **kwds):
        self.movable = Moveable(x, y)
        super().__init__(**kwds)

    def draw(self):
        self.movable.draw()
        super().draw()

class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

MovableColoredShape(color='red', shapename='triangle',
                    x=10, y=20).draw()
```

## Complete Example – Just for Fun

In Python 2.7 and 3.2, the `collections` module has both a `Counter` class and
an `OrderedDict` class. Those classes are easily composed to make an
`OrderedCounter`:

```py
from collections import Counter, OrderedDict


class OrderedCounter(Counter, OrderedDict):
     """Counter that remembers the order elements are first seen."""
     def __repr__(self):
         return '%s(%r)' % (self.__class__.__name__,
                            OrderedDict(self))

     def __reduce__(self):
         return self.__class__, (OrderedDict(self),)

oc = OrderedCounter('abracadabra')
```

## Notes and References

* When subclassing a builtin such as `dict()`, it is often necessary to override
  or extend multiple methods at a time. In the above examples, the `__setitem__`
  extension isn’t used by other methods such as `dict.update`, so it may be
  necessary to extend those also. This requirement isn’t unique to `super()`;
  rather, it arises whenever builtins are subclassed.

* If a class relies on one parent class preceding another (for example,
  `LoggingOD` depends on `LoggingDict` coming before `OrderedDict` which comes
  before `dict`), it is easy to add assertions to validate and document the
  intended method resolution order:

  ```py
  position = LoggingOD.__mro__.index
  assert position(LoggingDict) < position(OrderedDict)
  assert position(OrderedDict) < position(dict)
  ```

* Good write-ups for linearization algorithms can be found at [Python MRO
  documentation](http://www.python.org/download/releases/2.3/mro/)
  and at [Wikipedia entry for C3 Linearization](http://en.wikipedia.org/wiki/C3_linearization).

---

#### Resources

* http://rhettinger.wordpress.com/2011/05/26/super-considered-super/
