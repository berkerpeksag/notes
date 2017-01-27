## Builder pattern

> In Python you can save common options in a dict and either pass them as
> keyword arguments or use `functools.partial`. In any case you don't need a
> builder class with the build method and a number of configuring methods. It
> can be just a function with optional keyword parameters.

> The builder pattern is often used in languages that don't support passing
> parameters as keyword arguments and partial functions. [...] The builder
> pattern is actually built-in in the core language as a part of its syntax.

**Reference:** https://mail.python.org/pipermail/python-ideas/2017-January/044379.html


## Iterator pattern

The classic iterator pattern is obsolote in Python since 2.2 released in 2001.
Python's iterator protocol and generators make the idea of classic iterator
pattern described in the famous Gang of Four book obsolote.

See [train.py](https://github.com/berkerpeksag/python-playground/blob/master/train.py) for an example.
