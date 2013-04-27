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

## Differences between `buffer` and `memoryviews`

A naive way to write a large string of bytes to a socket:

```py
sent = 0
while sent < len(message):
    sent += sock.send(message[sent:])
```

This makes many unnecessary copies of message. You can imagine how bad it
performs if message is 1GB long and the client only receives 1K at a time.

You can improve this by using Python's lesser known `buffer` built-in, which is
like a `memoryview` except it's read-only:

```py
buf = buffer(message,0)
while len(buf):
    buf = buffer(message,len(buf) + sock.send(buf))
```

This doesn't make any copies of message.

But what if I want the equivalent for efficiently receiving data from a socket
into a single buffer without having to allocate a bunch of small strings in the
loop?

Awesome `memoryview` way:

```py
view = memoryview(bytearray(bufsize))
while len(view):
    view = view[sock.recv_into(view,1024):]
```

Slicing view just returns a new `memoryview`, so there aren't any unnecessary
string allocations.

[Source](https://profiles.google.com/116139041198229909169/buzz/SmLJKHwpLPC)

## Documentation

* [The buffer interface][python-dev] by Guido van Rossum

[python-dev]: http://mail.python.org/pipermail/python-dev/2000-October/009974.html
