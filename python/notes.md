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
