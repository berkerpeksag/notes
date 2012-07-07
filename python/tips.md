## `%s` vs. `str.format()`

The `%s` gets implicitly coerced to unicode. You can use format if you just
always make your format input strings unicode strings (which you should be doing
anyway, especially now that Python 3.3 will allow the `u` prefix...that is,
such code will be forward-compatible with Python 3).
