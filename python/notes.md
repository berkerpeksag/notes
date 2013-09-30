# Notes

## Short notes

* The `hash(x) == id(x)` behaviour is a CPython implementation detail.


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

Reference: http://stackoverflow.com/questions/17735170/why-does-python-allow-an-empty-function-with-doc-string-body-without-a-pass
