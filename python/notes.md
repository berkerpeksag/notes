# Notes

* ```py
  >>> a = [1, 2]
  >>> print a.extend([2,3])
  None
  ```

  `extend` is a procedure with a side effect: the "self" object (i.e. `a` in
  this example) is modified.

  By convention, procedures return `None` in Python, as opposed to functions,
  which have no side effect but return a result. This is to avoid code like:

  ```py
  def combine(a, b):
      return a.extend(b)

  a = [1, 2]
  b = [3, 4]
  c = combine(a, b)
  ```

  If extend would return the "self" list, then people may think that they get a
  fresh, new list, and then wonder why a is modified.

  http://bugs.python.org/issue15614#msg167861

## What is the difference between arguments and parameters?

Parameters are defined by the names that appear in a function definition,
whereas arguments are the values actually passed to a function when calling it.
Parameters define what types of arguments a function can accept. For example,
given the function definition:

```py
def func(foo, bar=None, **kwargs):
    pass
```

*foo*, *bar* and *kwargs* are parameters of `func`. However, when calling
`func`, for example:

```py
func(42, bar=314, extra=somevar)
```

the values `42`, `314`, and `somevar` are arguments.
