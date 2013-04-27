# Memoryviews

**Note:** `buffer` has been replaced by the better named `memoryview` in
Python 3, though you can use either in Python 2.7.

```py
>>> s = 'Hello world'
>>> t = buffer(s, 6, 5)
>>> t
<read-only buffer for 0x10064a4b0, size 5, offset 6 at 0x100634ab0>
>>> print t
world
```

The buffer in this case is a sub-string, starting at position 6 with length
5, and *it doesn't take extra storage space* - it references a slice of the
string.

This isn't very useful for short strings like this, but it can be necessary
when using large amounts of data. This example uses a mutable `bytearray`:

```py
>>> s = bytearray(1000000)   # a million zeroed bytes
>>> t = buffer(s, 1)         # slice cuts off the first byte
>>> s[1] = 5                 # set the second element in s
>>> t[0]                     # which is now also the first element in t!
'\x05'
```

This can be very helpful if you want to have more than one view on the data and
don't want to (or can't) hold multiple copies in memory.

[Source](http://stackoverflow.com/a/3422740)

## Documentation

* [The buffer interface][python-dev] by Guido van Rossum

[python-dev]: http://mail.python.org/pipermail/python-dev/2000-October/009974.html
