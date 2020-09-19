# Implementation details

## String concatenation optimization

Example code to demonstrate speed difference:

```py
def concat(string):
    result = ''
    for element in string:
        result += element
    return result


def concat2(string):
    result = ''
    for element in string:
        result += element
        temp = result
    return result


if __name__ == '__main__':
    import timeit

    print(timeit.timeit(lambda: concat(['a' for _ in range(10000)]), number=10000))
    print(timeit.timeit(lambda: concat2(['a' for _ in range(10000)]), number=10000))
```

Output on early 2015 MacBook Pro:

```sh
$ python3 example.py
23.537358867000002
29.960698949999998
```

Python has a special optimization resizing the string object and appending in
place. If there is an another object referencing to the same string object, it's
not possible to rely on this optimization.

The `+=` operation uses `PyUnicode_Append()` function which has the following
condition in order to use this optimization:

```c
if (unicode_modifiable(left)
    && PyUnicode_CheckExact(right)
    && PyUnicode_KIND(right) <= PyUnicode_KIND(left)
    /* Don't resize for ascii += latin1. Convert ascii to latin1 requires
       to change the structure size, but characters are stored just after
       the structure, and so it requires to move all characters which is
       not so different than duplicating the string. */
    && !(PyUnicode_IS_ASCII(left) && !PyUnicode_IS_ASCII(right)))
{
    /* append inplace */
}
```

Reference: [`/Objects/unicodeobject.c`](https://github.com/python/cpython/blob/b3fbff7289176ba1a322e6899c3d4a04880ed5a7/Objects/unicodeobject.c#L11708-L11723)

---

The most important part in there is `unicode_modifiable()` which basically consists
of bunch of `if` statements:

```c
static int
unicode_modifiable(PyObject *unicode)
{
    assert(_PyUnicode_CHECK(unicode));
    if (Py_REFCNT(unicode) != 1)
        return 0;
    if (_PyUnicode_HASH(unicode) != -1)
        return 0;
    if (PyUnicode_CHECK_INTERNED(unicode))
        return 0;
    if (!PyUnicode_CheckExact(unicode))
        return 0;
#ifdef Py_DEBUG
    /* singleton refcount is greater than 1 */
    assert(!unicode_is_singleton(unicode));
#endif
    return 1;
}
```

Reference: [`/Objects/unicodeobject.c`](https://github.com/python/cpython/blob/b3fbff7289176ba1a322e6899c3d4a04880ed5a7/Objects/unicodeobject.c#L2004-L2021)

---

In `concat()` example, the following `if` statement will return `false`:

```c
if (Py_REFCNT(unicode) != 1)
    return 0;
```

However, in `concat2()` example won't return `1` because of the following line:

```py
temp = result
```
