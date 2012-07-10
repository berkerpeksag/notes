# New-style and classic classes

```python
>>> class A:
...     pass
...
>>> type(A)
<type 'classobj'>
>>> a = A()
>>> type(a)
<type 'instance'>
>>> class B(object):
...     pass
...
>>> type(B)
<type 'type'>
>>> b = B()
>>> type(b)
<class '__main__.B'>

```

Classes and instances come in two flavors: old-style (or classic) and new-style.

Up to Python 2.1, old-style classes were the only flavour available to the user.
The concept of (old-style) class is unrelated to the concept of type: if `x` is
an instance of an old-style class, then `x.__class__` designates the class of
`x`, but `type(x)` is always `<type 'instance'>`. This reflects the fact that
all old-style instances, independently of their class, are implemented with a
single built-in type, called instance.

New-style classes were introduced in Python 2.2 to unify classes and types. A
new-style class is neither more nor less than a user-defined type. If `x` is an
instance of a new-style class, then `type(x)` is typically the same as
`x.__class__` (although this is not guaranteed - a new-style class instance is
permitted to override the value returned for `x.__class__`).

The major motivation for introducing new-style classes is to provide a unified
object model with a full meta-model. It also has a number of practical benefits,
like the ability to subclass most built-in types, or the introduction of
"descriptors", which enable computed properties.

For compatibility reasons, classes are still old-style by default. New-style
classes are created by specifying another new-style class (i.e. a type) as a
parent class, or the "top-level type" object if no other parent is needed. The
behaviour of new-style classes differs from that of old-style classes in a
number of important details in addition to what `type()` returns. Some of these
changes are fundamental to the new object model, like the way special methods
are invoked. Others are "fixes" that could not be implemented before for
compatibility concerns, like the method resolution order in case of multiple
inheritance.

**Old-style classes are removed in Python 3, leaving only the semantics of
new-style classes.**

### Links

* http://docs.python.org/reference/datamodel.html#new-style-and-classic-classes
* http://www.cafepy.com/article/python_types_and_objects/python_types_and_objects.html
* http://www.cafepy.com/article/python_attributes_and_methods/python_attributes_and_methods.html
