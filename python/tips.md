## `%s` vs. `str.format()`

The `%s` gets implicitly coerced to unicode. You can use format if you just
always make your format input strings unicode strings (which you should be doing
anyway, especially now that Python 3.3 will allow the `u` prefix...that is,
such code will be forward-compatible with Python 3).

## Backticks in Python

Backticks are a deprecated alias for `repr()`. Don't use them any more, the
syntax was removed in Python 3.

In Python 2.7.3:

```py
>>> repr(object)
"<type 'object'>"
>>> `object`
"<type 'object'>"
```

In Python 3.3:

```py
>>> repr(object)
"<class 'object'>"
>>> `object`
  File "<stdin>", line 1
    `object`
    ^
SyntaxError: invalid syntax
```

### Guido van Rossum's thoughts

>> Thus, I propose one of the following as the new use for the backtick (`):
>
> You're missing one of the main reasons for removing the backtick
> syntax in the first place: the character itself causes trouble by
> looking too much like a regular quote (depending on your font), is
> routinely mangled by typesetting software (as every Python book author
> can testify), and requires a four-finger chord on Swiss keyboards. No
> new uses for it will be accepted in Python 3000 no matter how good the
> idea.

http://mail.python.org/pipermail/python-ideas/2007-January/000054.html
