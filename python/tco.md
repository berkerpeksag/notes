# Tail Call Optimization

Let's take the standard Fibonacci number generator in a simple Python example:

```py
def fib(i):
    if i == 0:
        return 0
    elif i == 1:
        return 1
    else:
        return fib(i - 1) + fib(i - 2)
```

and then use this function in a simple interpreter session:

```py
>>> fib(0)
0
>>> fib(1)
1
>>> fib(2)
1
>>> fib(10)
55
```

Everything seems fine. But if I try to compute the 1000th member of the
Fibonacci sequence I find the following:

```py
>>> fib(1000)
  File "fib.py", line 7, in fib
    return fib(i - 1) + fib(i - 2)
  File "fib.py", line 7, in fib
    return fib(i - 1) + fib(i - 2)
RuntimeError: maximum recursion depth exceeded
```

Essentially Python is saying "you can't have a function calling a function this
many levels deep". There is a standard problem here: if one has a recursive
function then every time it recurses one needs extra stack space. At some point
the stack *will* run out.

So in order to make this style of programming practical, a way is needed for
allowing recursive functions to use a fixed stack size. This is where *tail
calls* come in. Let us first rewrite our Fibonacci generator as follows:

```py
def fib(i, current=0, next_item=1):
    if i == 0:
        return current
    else:
        return fib(i - 1, next_item, current + next_item)
```

Our function now has a tail call. That is, the branch of the if construct that
recursively calls the function is a tail call. What this means is that *the very
last thing the function does before returning* is to recursively call itself.

The current invocation of the function will never need the stack space again
since as soon as it receives a value from the recursive call it will return it
to its caller. So instead of allocating stack space, we could simply reuse the
stack space used by the current function (and inherit the return address of the
current function rather than making the current function the address to which we
will return). This way, it doesn't matter *how many times* the function
recursively calls itself - it will only ever use a constant amount of stack
space. Taking advantage of this fact is called *tail call optimization*.


## Costs

* The first is fairly obvious, and is evident in the forced rewriting of the
  Fibonacci function: many functions have their most natural form without tail
  calls. Thus functions often need to be designed very specifically with tail
  calls in mind. Writing functions in this style, or rewriting existing
  functions in this style, can be far from trivial. What's more, as can be seen
  from the Fibonacci example, the resulting function is frequently hard to
  understand because it often requires state to be passed around in parameters.
* The second cost associated with tail calls is something that I have not seen
  mentioned elsewhere, which may well mean that I've got the wrong end of the
  stick. However I suspect it might be the case that it is not mentioned because
  the problem is only really evident in languages which give decent stack trace
  error reports when exceptions occur. Consider this: since tail call
  optimization involves overwriting the stack, what happens if an exception is
  raised at some point deep within a tail calling part of a program?

## Guido's Argument

* Stack traces help debug, TRE makes them useless.
* TRE is Not An Optimization (it creates a class of code that explodes without
  it).
* Guido does not subscribe to the "Recursion is the basis of all programming""
  idea.
* Due to Python's highly dynamic namespaces, it's very nontrivial to know if a
  call is a recursion.
  
### References

* http://tratt.net/laurie/blog/entries/tail_call_optimization
