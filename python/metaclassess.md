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

---

## The `__new__()` static method

### Instance method

A little bit about instance methods first. Let's write a class.

```python
class A(object):
    def met(self, a, b):
        print a, b
```

In this case, `met()` is an instance method. So, it is expected that we pass an
instance of `A` as the first argument to `met()`.

When we called `met()`, we passed two arguments although `met()` expects three
argument as per its definition. When we wrote `obj.met(1, 2)`, interpreter took
care of sending instance `obj` as the first argument to `met()` and 1 and 2 were
passed as second and third arguments respectively:

```python
def met(self, a, b):  # self == A()
    pass
```

If we pass an instance of `A` as the first argument, it will work as expected.

```python
>>> obj = A()
>>> A.met(obj, 3, 4)
3 4
```

Let's see static method now.

```python
class B(object):
    @staticmethod
    def met(a, b):
        print a, b
```

So, for our method definition, the method does not expect its first argument to
be an instance of `B`. Even if we call the method on an instance of `B`, current
instance will not be passed as the first argument to this method, since its a
static method. For instance method that we saw earlier the current instance was
passed as the first argument.

```python
>>> B.met(5, 6)
>>> 5 6
```

### So, what is `__new__`?

1. `__new__` is a static method which creates an instance. We will see the
method signature soon. One reason I could think of having `__new__` as a static
method is because the instance has not been created yet when `__new__` is
called. So, they could not have had it as an instance method.
2. `__new__` gets called when you call the class. Call the class means issuing
the statement `a = A(1, 2)`. Here `A(1, 2)` is like calling the class. A is a
class and we put two parenthesis in front of it and put some arguments between
the parenthesis. So, its like *calling the class* similar to calling a method.
3. `__new__` **must return** the created object.
4. Only when `__new__` returns the created instance then `__init__` gets called.
If `__new__` does not return an instance then `__init__` would not be called.
Remember `__new__` is always called **before** `__init__`.
5. `__new__` gets passed all the arguments that we pass while calling the class.
Also, it gets passed one extra argument that we will see soon.

#### How was the instance created in the last example when we didn't define `__new__`?

Class `A` extends from `object`(like a *abstract base class*). `object` defines
a method `__new__`, so `A` gets this method from `object` since its extending
`object`. This inherited `__new__` created the instance of `A`.

```python
class A(object):  # Inherited from object
    pass
```

#### The result

```python
class A(object):
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls, *args, **kwargs)
```

#### Resources

* http://agiliq.com/blog/2012/06/__new__-python/
* http://agiliq.com/blog/2012/07/metaclass-python/
