# Python Objects

All Python objects have this:

* **A unique identity (an integer, returned by `id(x)`).** You cannot change the
  identity.
* **A type (returned by `type(x)`).** You cannot change the type.
* **Some content.** Some objects allow you to change their content (without
  changing the identity or the type, that is).

Objects may also have this:

* zero or more methods (provided by the type object)
* zero or more names

Some objects have methods that allow you to change the contents of the object
(modify it in place, that is).

Some objects only have methods that allow you to access the contents, not change
it.

Some objects don't have any methods at all.

Even if they have methods, you can never change the type, nor the identity.

**Note:** Things like `name.attr` and `name[index]` are just syntactic sugar for
method calls. The first corresponds to `__setattr__` and `__getattr__`, the
second to `__setitem__` and `__getitem__`.


## Types

[...] An object’s type determines the operations that the object supports
(e.g., "does it have a length?") and also defines the possible values for
objects of that type.

Every object in Python has a type. The type is an object too, so it has a type
of its own, which is called `type`.


## Classes

```py
>>> class Joe: pass
...
>>> j = Joe()
>>> type(j)
<class '__main__.Joe'>
```

Using the class mechanism, we've created `Joe` - a user-defined type. `j` is
an instance of the class `Joe`. In other words, it's an object and its type is
`Joe`.

As any other type, `Joe` is an object itself, and it has a type too:

```py
>>> type(type(j))
<class 'type'>
```


## Instances

Objects are instances of types. So, "42 is an instance of the type int" is
equivalent to "42 is an int object".

**Reference:** http://eli.thegreenplace.net/2012/03/30/python-objects-types-classes-and-instances-a-glossary


## Names

An object can have any number of names, or no name at all.

Names live in namespaces (such as a module namespace, an instance namespace, a
function's local namespace).

## call-by-object

The only thing you need to know is that Python's model is neither
"call by value" nor "call by reference" (because any attempt to use those terms
for Python requires you to use non-standard definitions of the words "-value"
and "-reference"). The most accurate description is CLU’s "call by object" or
"call by sharing". Or, if you prefer, "call by object reference".

The following excerpts are taken from an old comp.lang.python thread. The
interesting parts are the CLU texts, which provide a very concise description of
Python's calling model.

---

> See
>
>   http://wombat.doc.ic.ac.uk/foldoc/foldoc.cgi?call-by-value
>
> What you describe is call-by-value.

It's interesting that you quote FOLDOC, given that FOLDOC doesn't
refer to Python's model as call-by-value, as can be seen in the CLU
entry:

    http://wombat.doc.ic.ac.uk/foldoc/foldoc.cgi?CLU

    "Arguments are passed by call-by-sharing, similar to
    call-by-value, except that the arguments are objects
    and can be changed only if they are mutable."

Note the use of the words "similar" and "except".

For a brief description of CLU's object and argument passing models,
see [1].  I think you'll find that it matches Python's model pretty well.

The CLU Reference Manual [2] by Liskov et al says (page 14):

    "We call the argument passing technique _call by sharing_,
    because the argument objects are shared between the
    caller and the called routine.  This technique does not
    correspond to most traditional argument passing techniques
    (it is similar to argument passing in LISP).  In particular it
    is not call by value because mutations of arguments per-
    formed by the called routine will be visible to the caller.
    And it is not call by reference because access is not given
    to the variables of the caller, but merely to certain objects."

Note the use of "does not" and the repeated use of "it is not".
Let me emphasise:

    "IN PARTICULAR IT IS NOT CALL BY VALUE because mutations
    of arguments performed by the called routine will be visible to
    the caller. And IT IS NOT CALL BY REFERENCE because access
    is not given to the variables of the caller, but merely to certain
    objects."

CLU was designed in the mid-seventies, and this reference manual
was published in 1979.  In other literature, the CLU designers some-
times refer to this model as "call by object" [3], or they carefully
ignore the issue by talking about "objects" instead of values, and
"objects that refer to other objects" instead of references [1], but
I cannot find a single place where they've gone from "in particular
it is not call by value" to "it is call by value".

So what's your excuse for being stuck in the early seventies? ;-)

</F>

1) http://www.cs.berkeley.edu/~jcondit/pl-prelim/liskov77clu.pdf
2) http://www.lcs.mit.edu/publications/pubs/pdf/MIT-LCS-TR-225.pdf
3) http://www.lcs.mit.edu/publications/pubs/pdf/MIT-LCS-TR-561.pdf

---

> I'm not familiar with CLU

I suggest reading reference 3.

    http://www.lcs.mit.edu/publications/pubs/pdf/MIT-LCS-TR-561.pdf

CLU is an important milestone in the development of OO languages;
to quote Liskov herself, from the above paper:

    "The work on CLU, and other related work such as that on
    Alphard, served to crystallize the idea of a data abstraction
    and make it precise. As a result, the notion is widely used as
    an organizing principle in program design and has become a
    cornerstone of modern programming methodology."

if you don't know your history, etc.

> but I think this description of Python's argument-passing
> semantics is misleading.

did you read reference 1?

    http://www.cs.berkeley.edu/~jcondit/pl-prelim/liskov77clu.pdf

in case your PDF reader is broken, here are the relevant portions from
that document (any typos etc added by me).

    "The basic elements of CLU semantics are _objects_ and
    _variables_.  Objects are the data entities that are created and
    manipulated by CLU programs.  Variables are just the names used
    in a program to refer to objects.

    In CLU, each object has a particular _type_, which characterizes
    its behavior.  A type defines a set of operations that create
    and manipulate objects of that type.  An object may be created
    and manipulated only via the operations of its type.

    An object may _refer_ to objects.  For example, a record object
    refers to the objects that are the components of the record.
    This notion is one of logical, not physical, containment.  In
    particular, it is possible for two distinct record objects to
    refer to (or _share_) the same component object.  In the case of
    a cyclic structure, it is even possible for an object to
    "contain" itself.  Thus it is possible to have recursive data
    structure definitions and shared data objects without explicit
    reference types. /.../

    CLU objects exist independently of procedure activations.  Space
    for objects is allocated from a dynamic storage area /.../ In
    theory, all objects continue to exist forever.  In practice, the
    space used by an object may be reclaimed when the object isno
    longer accessible to any CLU program.

    An object may exhibit time-varying behavior.  Such an object,
    called a _mutable_ object, has a state which may be modified by
    certain operations without changing the identity of the
    object. /.../

    If a mutable object _m_ is shared by two other objects _x_ and
    _y_, then a modification to _m_ made via _x_ wil be visible when
    _m_ is examined via _y_.  /.../

    Objects that do not exhibit time-varying behavior are called
    _immutable_ objects, or constants.  Examples of constants are
    integers, booleans, characters, and strings.  The value of a
    constant object can not be modified.  For example, new strings
    may be computed from old ones, but existing strings do not
    change.  Similarily, none of the integer operations modify the
    integers passed to them as arguments.

    Variables are names used in CLU programs to _denote_ particular
    objects at execution time.  Unlike variables in many common
    programming languages, which _are_ objects that _contain_
    values, CLU variables are simply names that the programmer uses
    to refer to objects.  As such, it is possible for two variables
    to denote (or _share_) the same object.  CLU variables are much
    like those in LISP and are similar to pointer variables in other
    languages.  However, CLU variables are _not_ objects; they
    cannot be denoted by other variables or referred to by
    objects. /.../

    The basic actions in CLU are _assignment_ and _procedure
    invocation_.  The assignment primitive 'x := E' where _x_ is a
    variable and _E_ is an expression, causes _x_ to denote the
    object resulting from the evaulation of _E_.  For example, if
    _E_ is a simple variable _y_, then the assignment 'x := y'
    causes _x_ to denote the object denoted by _y_.  The object is
    _not_ copied, it will be _shared_ by _x_ and _y_.  Assignment
    does not affect the state of any object.  (Recall that 'r.s :=
    v' is not a true assignment, but an abbreviation for 'put.s(r,
    v)'.)

    Procedure invocation involves passing argument objects from the
    caller to the called procedure and returning result objects from
    the procedure to the caller.  The formal arguments of a
    procedure are considered to be local variables of the procedure
    and are initialized, by assignment, to the objects resulting
    from the evaluation of the argument expressions.  Thus argument
    objects are shared between the caller and the called procedure.
    A procedure may modify mutable argument objects (e.g. records),
    but of course it cannot modify immutable ones (e.g. integers).
    A procedure has no access to the variables of its caller.

    Procedure invocations may be used directly as statements; those
    that return objects may also be used as expressions.  Arbitrary
    recursive procedures are permitted."

replace "CLU" with "Python", "record" with "instance", and "procedure"
with "function or method", and you get a pretty accurate description
of Python's object model.

---
