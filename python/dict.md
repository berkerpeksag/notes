**Note:** This document can be merged into ``python/notes.md``.

## "Attribute lookup" or "dot notation" in a dictionary

```py
class Dict(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
```

## try/except KeyError vs "if name in ..."

If failure is rare (less than 10-20%) use try.

```py
def __import__(name, globals=None, locals=None, fromlist=None):
    # Fast path: see if the module has already been imported.
    try:
        return sys.modules[name]
    except KeyError:
        pass
```

If you expect that most of the time the module will be found, the
``try...except`` version will be faster.

```py
if name in sys.modules:
    return sys.modules[name]
```

If you expect that most of the time the module will not be found, the
``if name in`` version will be faster.

#### Resources

* http://mail.python.org/pipermail/python-list/2012-October/632493.html
* http://mail.python.org/pipermail/python-list/2012-October/632518.html
