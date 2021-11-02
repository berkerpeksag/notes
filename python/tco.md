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
run time (or in some languages it can be converted to `goto` statements) It
also reduces the space complexity of recursion from O(N) to O(1).:

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

### Stack frames

The Python interpreter uses a call stack to run a Python program. When a
function is called in Python, a new frame is pushed onto the call stack for its
local execution, and every time a function call returns, its frame is popped
off the call stack.

The module in which the program runs has the bottom-most frame which is called
the global frame or the module frame.

Python stores all the information about each frame of the call stack in a frame object.

Here is an example to show how stack frames are created during execution of a recursed
function:

```py
import inspect

from inspect import FrameInfo
from typing import List


def print_frames(frame_list: List[FrameInfo]) -> None:
    module_frame_index = frame_list.index(frame_list[-1])
    for i in range(module_frame_index):
        frame_index = module_frame_index - i
        function_name = frame_list[i].function
        local_vars = frame_list[i][0].f_locals
        print(f"  [Frame {frame_index} {function_name!r}: {local_vars}]")
    print("  [Frame '<module>']")
    print()


def fact(n: int) -> int:
    if n == 0:
        print(f"fact({n}) called:")
        print_frames(inspect.stack())
        print(f"fact({n}) returned 1")
        return 1
    else:
        print(f"fact({n}) called:")
        print_frames(inspect.stack())
        result = n * fact(n - 1)
        print_frames(inspect.stack())
        print(f"fact({n}) returned {result}")
        return result


if __name__ == '__main__':
    fact(3)
```

Output of the snippet above:

```
fact(3) called:
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(2) called:
  [Frame 2 'fact': {'n': 2}]
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(1) called:
  [Frame 3 'fact': {'n': 1}]
  [Frame 2 'fact': {'n': 2}]
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(0) called:
  [Frame 4 'fact': {'n': 0}]
  [Frame 3 'fact': {'n': 1}]
  [Frame 2 'fact': {'n': 2}]
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(0) returned 1
  [Frame 3 'fact': {'n': 1, 'result': 1}]
  [Frame 2 'fact': {'n': 2}]
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(1) returned 1
  [Frame 2 'fact': {'n': 2, 'result': 2}]
  [Frame 1 'fact': {'n': 3}]
  [Frame '<module>']

fact(2) returned 2
  [Frame 1 'fact': {'n': 3, 'result': 6}]
  [Frame '<module>']

fact(3) returned 6
```


## References

* http://tratt.net/laurie/blog/entries/tail_call_optimization
* http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html
* https://towardsdatascience.com/python-stack-frames-and-tail-call-optimization-4d0ea55b0542
