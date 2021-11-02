## Tail Call Recursion Optimization (TCO)

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

Everything seems fine until we try to compute the 1000th member of the
Fibonacci sequence:

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
calls* come in:

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

## Tail Recursion Elimination (TRE)

TRE is a technique to convert recursive functions into loops during compile or
run time:

```py
# Before:

def get_root(node):
    if node.parent is None:
        return node
    return get_root(node.parent)

# After:

def get_root(node):
    while True:
        if node.parent is None:
            return node
        node = node.parent
```

### Guido's thoughts

* Stack traces help debug, Tail Recursion Elimination (TRE) makes them useless.
* TRE is Not An Optimization (it creates a class of code that explodes without
  it).
* Guido does not subscribe to the "Recursion is the basis of all programming"
  idea.
* Due to Python's highly dynamic namespaces, it's very nontrivial to know if a
  call is a recursion.
  
#### References

* http://tratt.net/laurie/blog/entries/tail_call_optimization
* http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html
