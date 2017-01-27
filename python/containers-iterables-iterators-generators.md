# Containers, Iterables, Iterators, Generators

* An iterable is a *sequence* of data you can iterate over using the `for`
  statement:

  ```py
  l = [1, 2, 3, 4, 5, 6, 7]

  for i in l:
      print(i)
  ```

  `l` is also a container. Containers are data structures holding elements,
  and that support membership tests.
* Lists are not the only container type in Python: strings, dicts, tuples,
  sets, etc.
* Most containers are iterable.
* An iterable is any object, not necessarily a data structure, that can return
  an iterator
* Any object that has a `__iter__` method can be used as an **iterable**.
* An iterator is always an iterable.
* There is a difference between an iterator and iterable:

  ```py
  >>> x = [1, 2, 3]
  >>> y = iter(x)
  >>> z = iter(x)
  >>> next(y)
  1
  >>> next(y)
  2
  >>> next(z)
  1
  >>> type(x)
  <class 'list'>
  >>> type(y)
  <class 'list_iterator'>
  ```

  `x` is the iter*able*, while `y` and `z` are two individual instances of an
  iterat*or*, producing values from the iterable `x`.

  Both `y` and `z` hold state, as you can see from the example.

  In this example, `x` is a data structure (a list), but that is not a
  requirement.
* An **iterator** is a stateful helper object that will produce the next value
  when you call `next()` on it.

  Any object that has a `__next__` method is therefore an iterator.
* Some iterable classes will implement both `__iter__` and `__next__` in the
  same class, and have `__iter__` return `self`, which makes the class both an
  **iterable** and its own **iterator**.
* When you use a for loop, Python will do the following steps:

  **Low level explanation:**

  1. `GET_ITER` opcode will call `PyObject_GetIter(iterable)` which is an
     equivalent of `iter(iterable)`
  2. Then `FOR_ITER` opcode will call the function that the `tp_iternext`
     slot of the type of the iterator points to:

     ```c
     PyObject *next = (*iter->ob_type->tp_iternext)(iter);
     ```

     `tp_iternext` is an optional pointer to a function that returns the
     next item in an iterator.

  **High level explanation:**

  1. `__iter__` method is called on the object to get an iterator object by
     calling `iter(iterator)`.
  2. `__next__` method is called on the iterator object to get the next
     element of the sequence.
  3. `StopIteration` exception is raised when there are no elements left
     to call.

  Here's an example:

  ```py
  >>> my_list = [1, 2, 3]
  >>> my_list
  [1, 2, 3]
  >>> my_iterator = iter(my_list)
  >>> my_iterator
  <list_iterator object at 0x7fb91910e2b0>
  >>> next(my_iterator)
  1
  >>> next(my_iterator)
  2
  >>> next(my_iterator)
  3
  >>> next(my_iterator)
  Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
  StopIteration
  ```
* You can avoid implementing `__iter__` and `__next__` methods by using
  **generators**. Note that any generator is also an iterator.
* Here's an example of a lazily created container by using a generator:

  ```py
  >>> import itertools as it
  >>> def gen():
  ...   i = 0
  ...   while True:
  ...     yield i
  ...     i += 1
  ...
  >>> g = gen()
  >>> list(it.islice(g, 0, 5))  # it.islice() is also an iterator
  [0, 1, 2, 3, 4]
  ```

**Reference:** The part about the difference between an iterator and an
iterable taken from http://nvie.com/posts/iterators-vs-generators/ The rest of
the document written by me.
