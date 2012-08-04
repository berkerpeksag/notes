# Python Idioms

Getters and setters are evil. Evil, evil, I say! Python objects are not Java
beans. Do not write getters and setters. This is what the 'property' built-in is
for. And do not take that to mean that you should write getters and setters, and
then wrap them in 'property'. That means that until you prove that you need
anything more than a simple attribute access, don't write getters and setters.
They are a waste of CPU time, but more important, they are a waste of programmer
time. Not just for the people writing the code and tests, but for the people who
have to read and understand them as well.

In Java, you have to use getters and setters because using public fields gives
you no opportunity to go back and change your mind later to using getters and
setters. So in Java, you might as well get the chore out of the way up front. In
Python, this is silly, because you can start with a normal attribute and change
your mind at any time, without affecting any clients of the class. So, don't
write getters and setters.

## == vs. is

* `is` tests object identity. Do the two operands refer to the same object?
* `==` tests equality of value. Do the two operands have the same value?
* There's an optimization that allows small integers to be compared with is, but
don't rely on it.
* For comparing against `None`, `x is None` is preferred over `x == None`.

```python
a = 19998989890
b = 19998989889 + 1
>>> a is b
False
>>> a == b
True
```

`is` compares for two objects in memory, `==` compares their values, for example
you can see that small integers are cached by Python:

```python
c = 1
b = 1
>>> b is c
True
```
