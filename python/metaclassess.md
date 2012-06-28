# Metaclassess

## Basic Principles

* Everything is an object
* Everything has a type
* No real difference between 'class' and 'type' (see note)
* Classes are objects
* Their type is `type`

**Note:** Typically the term type is used for the built-in types and the term
class for user-defined classes. Since Python 2.2 there has been no real
difference and 'class' and 'type' are synonyms.

```python
Python 2.5.1 (r251:54869, Apr 18 2007, 22:08:04)
>>> class Something(object):
...     pass
...
>>> Something
<class '__main__.Something'>
>>> type(Something)
<type 'type'>
```

* The Class of a Class is its metaclass.
* Just as an object is an instance of its class; a class is an instance of its
metaclass.
* The metaclass is called to create the class.
* In exactly the same way as any other object in Python.
* So when you create a class... The interpreter calls the metaclass to create
it.

For a normal class that inherits from object this means that `type` is called to
create the class:

```python
>>> help(type)
Help on class type in module __builtin__:

class type(object)
 |  type(object) -> the object's type
 |  type(name, bases, dict) -> a new type

```

#### Resources

* http://www.voidspace.org.uk/python/articles/five-minutes.shtml
