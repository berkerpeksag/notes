# Notes

## Short notes

* The `hash(x) == id(x)` behaviour is a CPython implementation detail.

## Container objects

Container is a class that implements the `__contains__` method.

Containers are any object that holds an arbitrary number of other objects.
Generally, containers provide a way to access the contained objects and to
iterate over them.

`tuple`, `list`, `set`, `dict` are the *built-in* containers.


## Behavior of `list.extend()`

```py
>>> a = [1, 2]
>>> print a.extend([2,3])
None
```

`extend` is a procedure with a side effect: the "self" object (i.e. `a` in
this example) is modified.

By convention, procedures return `None` in Python, as opposed to functions,
which have no side effect but return a result. This is to avoid code like:

```py
def combine(a, b):
    return a.extend(b)

a = [1, 2]
b = [3, 4]
c = combine(a, b)
```

If extend would return the "self" list, then people may think that they get a
fresh, new list, and then wonder why a is modified.

**Resource:** http://bugs.python.org/issue15614#msg167861


## Generators: Your own iterables

```py
def hello_world():
    yield 'Hello'
    yield 'World'

for c in hello_world():
    print c
```


## Getters and setters

Getters and setters are evil. Evil, evil, I say! Python objects are not Java
beans. Do not write getters and setters. This is what the 'property' built-in is
for. And do not take that to mean that you should write getters and setters, and
then wrap them in 'property'. That means that until you prove that you need
anything more than a simple attribute access, don't write getters and setters.
They are a waste of CPU time, but more important, they are a waste of programmer
time. Not just for the people writing the code and tests, but for the people who
have to read and understand them as well.

In Java, you have to use getters and setters because using public fields gives
you no opportunity to go back and change your mind later to using getters and
setters. So in Java, you might as well get the chore out of the way up front. In
Python, this is silly, because you can start with a normal attribute and change
your mind at any time, without affecting any clients of the class. So, don't
write getters and setters.


## == vs. is

* `is` tests object identity. Do the two operands refer to the same object?
* `==` tests equality of value. Do the two operands have the same value?
* There's an optimization that allows small integers to be compared with is, but
don't rely on it.
* For comparing against `None`, `x is None` is preferred over `x == None`.

```py
a = 19998989890
b = 19998989889 + 1
>>> a is b
False
>>> a == b
True
```

`is` compares for two objects in memory, `==` compares their values, for example
you can see that small integers are cached by Python:

```py
c = 1
b = 1
>>> b is c
True
```


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

**Resource:** http://mail.python.org/pipermail/python-ideas/2007-January/000054.html


## What is the difference between arguments and parameters?

Parameters are defined by the names that appear in a function definition,
whereas arguments are the values actually passed to a function when calling it.
Parameters define what types of arguments a function can accept. For example,
given the function definition:

```py
def func(foo, bar=None, **kwargs):
    pass
```

*foo*, *bar* and *kwargs* are parameters of `func`. However, when calling
`func`, for example:

```py
func(42, bar=314, extra=somevar)
```

the values `42`, `314`, and `somevar` are arguments.


## Presentations

### Python White Magic

* https://speakerdeck.com/u/antocuni/p/python-white-magic
* [magic.py](https://bitbucket.org/antocuni/whitemagic/src/tip/code/magic.py)


## Why does Python allow an empty function body without a "pass" statement?

```py
def method_one(self):
    """This is the first method, will do something useful one day"""
```

**Short answer:** Although the docstring is usually not considered to be part of
the function body, because it is not "executed", it is parsed as such, so the
`pass` can be omitted.

### Long answer

According to the Python 2.7.5 grammar specification, which is read by the parser
generator and used to parse Python source files, a function looks like this:

```
funcdef: 'def' NAME parameters ':' suite
```
The function body is a suite which looks like this:

```
suite: simple_stmt | NEWLINE INDENT stmt+ DEDENT
```

Following this all the way through the grammar, `stmt` can be an `expr_stmt`,
which can be just a `testlist`, which can be just a single `test` which can
(eventually) be just an `atom`, which can be just a single `STRING`: The
docstring.

Here are just the appropriate parts of the grammar, in the right order to follow
through:

```
stmt: simple_stmt | compound_stmt
simple_stmt: small_stmt (';' small_stmt)* [';'] NEWLINE
small_stmt: (expr_stmt | print_stmt  | del_stmt | pass_stmt | flow_stmt |
             import_stmt | global_stmt | exec_stmt | assert_stmt)
expr_stmt: testlist (augassign (yield_expr|testlist) |
                     ('=' (yield_expr|testlist))*)
testlist: test (',' test)* [',']
test: or_test ['if' or_test 'else' test] | lambdef
or_test: and_test ('or' and_test)*
and_test: not_test ('and' not_test)*
not_test: 'not' not_test | comparison
comparison: expr (comp_op expr)*
comp_op: '<'|'>'|'=='|'>='|'<='|'<>'|'!='|'in'|'not' 'in'|'is'|'is' 'not'
expr: xor_expr ('|' xor_expr)*
xor_expr: and_expr ('^' and_expr)*
and_expr: shift_expr ('&' shift_expr)*
shift_expr: arith_expr (('<<'|'>>') arith_expr)*
arith_expr: term (('+'|'-') term)*
term: factor (('*'|'/'|'%'|'//') factor)*
factor: ('+'|'-'|'~') factor | power
power: atom trailer* ['**' factor]
atom: ('(' [yield_expr|testlist_comp] ')' |
       '[' [listmaker] ']' |
       '{' [dictorsetmaker] '}' |
       '`' testlist1 '`' |
       NAME | NUMBER | STRING+)
```

Reference:
http://stackoverflow.com/questions/17735170/why-does-python-allow-an-empty-function-with-doc-string-body-without-a-pass


## `__init__` vs `__new__`

* The `__new__` method is essentially the constructor for your class and handles
  its creation.
* You may think this is what the `__init__` method is for, but the class
  instance is actually already created by the time `__init__` gets called.
* The `__init__` method is just setting initial values for an already created
  object.
* The `__new__` method is what gets called before the object exists and actually
  creates and returns the object.


## `str.startswith((t1, t2))`

The current behavior is intentional, and the ambiguity of strings
themselves being iterables is the main reason. Since `str.startswith()` is
almost always called with a literal or tuple of literals anyway, I see
little need to extend the semantics.

Reference: https://mail.python.org/pipermail/python-ideas/2014-January/024661.html


## Guido's thoughts on `x.copy()`

> I personally despise almost all uses of "copying" (including the entire copy
> module, both deep and shallow copy functionality).  I much prefer to write
> e.g. list(x) over x.copy() -- when I say list(x) I know the type of the result.

Reference: http://bugs.python.org/msg224430


## `@staticmethod`s

Python's static methods not only execute at runtime, they are *defined* at
runtime. The compiler doesn't know that something will be a "static method", a
regular function, a "class method"... or whatever. The meaning of "static" is
entirely different from C's or Java's, where the information about static
methods is (and has to be) known at compile time.

Of course, this isn't limited to static methods. The same can be said about
docstrings, which use separate analysis methods in languages such as C++ or Java
(e.g. doxygen, javadoc...), but regular runtime introspection capabilities in
Python.

Reference: https://mail.python.org/pipermail/python-ideas/2014-August/029128.html


## What `range` really is in Python 3?

It's a full sequence type (specifically, a calculated tuple). The only immutable
sequence operations it doesn't support are concatenation and repetition (since
concatenating or repeating a range can't be represented using the simple
"start + n*step" calculation that range uses internally).

From the official Python documentation:

The advantage of the range type over a regular list or tuple is that a range
object will always take the same (small) amount of memory, no matter the size of
the range it represents (as it only stores the start, stop and step values,
calculating individual items and subranges as needed).

Range objects implement the ``collections.abc.Sequence`` ABC, and provide
features such as containment tests, element index lookup, slicing and support
for negative indices.

#### References

1. https://mail.python.org/pipermail/python-ideas/2014-October/029646.html
2. https://docs.python.org/3/library/stdtypes.html#ranges


## Recursion vs. tail recursion

Tail calls are when a function is recursing and returns simply on a function
call to itself. This is different than normal recursion where multiple things
can be happening on our recursed return statement.

**Tail recursion:**

```py
def factorial(N, result=1):
    if N == 1:
        return result
    return factorial(N-1, N*result)
```

**Normal recursion:**

```py
def factorial(N):
    if N == 1:
        return 1
    return N * factorial(N-1)
```

So we can see that normal recursion uses the return register in order to
maintain the state of the calculation. By contrast, tail recursion uses a
function parameter.

Generally when a function gets called, the system must set up a function stack
in memory that maintains the state of the function, including local variables
and code pointers, so that the function can go on its merry way. However, when
we do a tail recursion we are trying to enter the same function stack that we
are already in, just with changes to the values of the arguments! This can be
quickly optimized by never creating the new function stack and instead just
modifying the argument values and starting the function from the beginning!

Reference: http://blog.fastforwardlabs.com/post/117173339298/bytecode-hacking-for-great-justice

## Call by object

Objects are allocated on the heap and pointers to them can be passed around
anywhere.

When you make an assignment such as `x = 1000`, a dictionary entry is created
that maps the string "x" in the current namespace to a pointer to the integer
object containing one thousand.

When you update "x" with `x = 2000`, a new integer object is created and the
dictionary is updated to point at the new object. The old one thousand object
is unchanged (and may or may not be alive depending on whether anything else
refers to the object).

When you do a new assignment such as `y = x`, a new dictionary entry "y" is
created that points to the same object as the entry for "x".

Objects like strings and integers are immutable. This simply means that there
are no methods that can change the object after it has been created. For
example, once the integer object one-thousand is created, it will never change.
Math is done by creating new integer objects.

Objects like lists are mutable. This means that the contents of the object can
be changed by anything pointing to the object. For example,
`x = []; y = x; x.append(10); print y` will print `[10]`. The empty list was
created. Both "x" and "y" point to the same list. The append method mutates
(updates) the list object (like adding a record to a database) and the result
is visible to both "x" and "y" (just as a database update would be visible to
every connection to that database).

**Reference:** http://stackoverflow.com/a/15697476
