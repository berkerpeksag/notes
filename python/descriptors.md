# The Descriptor Protocol

> Descriptors have the advantage that you don't actually have to know anything
> about them to use Python

*gutworth on #python-dev*


The default behavior for attribute access is to `get`, `set`, or `delete` the
attribute from an object’s dictionary.

For instance, `a.x` has a lookup chain starting with `a.__dict__['x']`, then
`type(a).__dict__['x']`, and continuing through the base classes of `type(a)`
*excluding metaclasses*.

## Methods

* `descr.__get__(self, obj, type=None)`
* `descr.__set__(self, obj, value)`
* `descr.__delete__(self, obj)`

### Data Descriptors

If an object defines both `__get__()` and `__set__()`, it is considered a data
descriptor.

### Non-data Descriptor

Descriptors that only define `__get__()` are called non-data descriptors. They
are typically used for methods but other uses are possible.

### Read-only Data Descriptor

To make a read-only data descriptor, define both `__get__()` and `__set__()`
with the `__set__()` raising an `AttributeError` when called. Defining the
`__set__()` method with an exception raising placeholder is enough to make it a
data descriptor.

## Invoking Descriptors

A descriptor can be called directly by its method name: `d.__get__(obj)`.

Alternatively, it is more common for a descriptor to be invoked automatically
upon attribute access. For example, `obj.d` looks up `d` in the dictionary of
`obj`. If `d` defines the method `__get__()`, then `d.__get__(obj)` is invoked
according to the precedence rules listed below.

**Descriptors only work for new style objects and classes. A class is new style
if it is a subclass of `object`.**

### Objects

For objects, the machinery is in `object.__getattribute__()` which transforms
`b.x` into `type(b).__dict__['x'].__get__(b, type(b))`.

The implementation works through a precedence chain that gives data descriptors
priority over *instance variables*, instance variables priority over *non-data
descriptors*, and assigns lowest priority to `__getattr__()` if provided.

The full C implementation can be found in `PyObject_GenericGetAttr()` in
`Objects/object.c`.

### Classes

For classes, the machinery is in `type.__getattribute__()` which transforms
`B.x` into `B.__dict__['x'].__get__(None, B)`.

In pure Python, it looks like:

```py
def __getattribute__(self, key):
    """Emulate type_getattro() in Objects/typeobject.c"""
    v = object.__getattribute__(self, key)
    if hasattr(v, '__get__'):
       return v.__get__(None, self)
    return v
```

The important points to remember are:

* descriptors are invoked by the `__getattribute__()` method
* overriding `__getattribute__()` prevents automatic descriptor calls
* `__getattribute__()` is only available with new style classes and objects
* `object.__getattribute__()` and `type.__getattribute__()` make different calls
  to `__get__()`.
* data descriptors always override instance dictionaries.
* non-data descriptors may be overridden by instance dictionaries.

### MRO

The object returned by `super()` also has a custom `__getattribute__()` method
for invoking descriptors. The call `super(B, obj).m()` searches
`obj.__class__.__mro__` for the base class `A` immediately following `B` and
then returns `A.__dict__['m'].__get__(obj, A)`. If not a descriptor, `m` is
returned unchanged. If not in the dictionary, `m` reverts to a search using
`object.__getattribute__()`.

## Descriptor Example

The following code creates a class whose objects are data descriptors which
print a message for each `get` or `set`. Overriding `__getattribute__()` is
alternate approach that could do this for every attribute. However, this
descriptor is useful for monitoring just a few chosen attributes:

```py
class RevealAccess(object):
    """A data descriptor that sets and returns values
    normally and prints a message logging their access."""

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print 'Retrieving', self.name
        print obj, objtype
        return self.val

    def __set__(self, obj, val):
        print 'Updating' , self.name
        self.val = val


class MyClass(object):
    x = RevealAccess(10, 'x')
    y = 5


def main():
    a = MyClass()
    print a.x
    print a.y
    a.x = 42
    print a.x

if __name__ == '__main__':
    main()
```

## Properties

Calling `property()` is a succinct way of building a data descriptor that
triggers function calls upon access to an attribute. Its signature is:

```
property(fget=None, fset=None, fdel=None, doc=None)
```

The documentation shows a typical use to define a managed attribute `x`:

```py
class C(object):
    def __init__(self):
        self.__x = 'Eggs'

    def getx(self):
        return self.__x

    def setx(self, value):
        self.__x = value

    def delx(self):
        del self.__x

    # or use decorator style
    x = property(getx, setx, delx, "I'm the 'x' property.")


def main():
    c = C()
    print c.x
    c.x = 'Spam'
    print c.x

if __name__ == '__main__':
    main()
```

To see how `property()` is implemented in terms of the descriptor protocol, here
is a pure Python equivalent:

```py
class Property(object):
    """Emulate PyProperty_Type() in Objects/descrobject.c

    Signature of property():

    property(fget=None, fset=None, fdel=None, doc=None)
    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)


def main():
    c = C()
    print c.x
    c.x = 'Spam'
    print c.x

if __name__ == '__main__':
    main()
```

The `property()` builtin helps whenever a user interface has granted attribute
access and then subsequent changes require the intervention of a method.

For instance, a spreadsheet class may grant access to a cell value through
`Cell('b10').value`. Subsequent improvements to the program require the cell to
be recalculated on every access; however, the programmer does not want to affect
existing client code accessing the attribute directly. The solution is to wrap
access to the value attribute in a property data descriptor:

```py
class Cell(object):
    # ...
    def getvalue(self, obj):
        """Recalculate cell before returning value."""
        self.recalc()
        return obj._value
    value = property(getvalue)
```

## Functions and Methods

Class dictionaries store methods as functions.

In a class definition, methods are written using `def` and `lambda`, the usual
tools for creating functions.

The only difference from regular functions is that the first argument is
*reserved* for the **object instance**. By Python convention, the instance
reference is called `self` but may be called this or any other variable name.

To support method calls, functions include the `__get__()` method for binding
methods during attribute access. This means that all functions are non-data
descriptors which return bound or unbound methods depending whether they are
invoked from an object or a class.

Running the interpreter shows how the function descriptor works in practice:

```py
>>> class D(object):
     def f(self, x):
          return x

>>> d = D()
>>> D.__dict__['f']  # Stored internally as a function
<function f at 0x00C45070>
>>> D.f  # Get from a class becomes an unbound method
<unbound method D.f>
>>> d.f  # Get from an instance becomes a bound method
<bound method D.f of <__main__.D object at 0x00B18C90>>
```

The output suggests that bound and unbound methods are two different types.
While they could have been implemented that way, the actual C implementation of
`PyMethod_Type` in `Objects/classobject.c` is a single object with two different
representations depending on whether the `im_self` field is set or is `NULL`
(the C equivalent of `None`).

Likewise, the effects of calling a method object depend on the `im_self` field.
If set (meaning bound), the original function (stored in the `im_func` field) is
called as expected with the first argument set to the instance.

If unbound, all of the arguments are passed unchanged to the original function.
The actual C implementation of `instancemethod_call()` is only slightly more
complex in that it includes some type checking.
