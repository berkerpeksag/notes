# MRO

A method resolution order is the ordering of an inheritance graph for the
purposes of deciding which implementation to use when a method is invoked on an
object.

```py
>>> class A: pass
...
>>> class B(A): pass
...
>>> class C(A): pass
...
>>> class D(B, C): pass
...
>>> A.mro()
[<class '__main__.A'>,
 <class 'object'>]
>>> B.mro()
[<class '__main__.B'>,
 <class '__main__.A'>,
 <class 'object'>]
>>> C.mro()
[<class '__main__.C'>,
 <class '__main__.A'>,
 <class 'object'>]
>>> D.mro()
[<class '__main__.D'>,
 <class '__main__.B'>,
 <class '__main__.C'>,
 <class '__main__.A'>,
 <class 'object'>]
```

We can see that all of our classes have an MRO. But what is it used for? The
second half of our definition said “for the purposes of deciding which
implementation to use when a method is invoked on an object”. What this means is
that Python looks at a class’s MRO when a method is invoked on an instance of
that class. Starting at the head of the MRO, Python examines each class in order
looking for the first one which implements the invoked method. That
implementation is the one that gets used.

```py
>>> class A:
...     def foo(self):
...         print('A.foo')
...
>>> class B(A):
...     def foo(self):
...         print('B.foo')
...
>>> class C(A):
...     def foo(self):
...         print('C.foo')
...
>>> class D(B, C):
...     pass
...
```

What will happen if we invoke `foo()` on an instance of `D`? Remember that the
MRO of `D` was `[D, B, C, A, object]`. Since the first class in that sequence to
support `foo()` is `B`, we would expect to see `'B.foo'` printed, and indeed
that is exactly what happens:

```py
>>> D().foo()
B.foo
```

To reiterate, method resolution order is nothing more than some ordering of the
inheritance graph that Python uses to find method implementations.


## C3

The short answer to the question of how Python determines MRO is "C3 superclass
linearization", or simply C3. C3 is an algorithm initially developed for the
Dylan programming language, and it has since been adopted by several prominent
programming languages including Perl, Parrot, and of course Python.

What's important to know about C3 is that it guarantees three important
features:

1. Subclasses appear before base classes
2. Base class declaration order is preserved
3. For all classes in an inheritance graph, the relative orderings guaranteed by
   1 and 2 are preserved at all points in the graph.

When you invoke `super()` in Python, what actually happens is that you construct
an object of type `super`. In other words, super is a class, not a keyword or
some other construct. You can see this in a REPL:

```py
>>> s = super(C)
>>> type(s)
<class 'super'>
```

Given a method resolution order and a class `C` in that MRO, `super()` gives you
an object which resolves methods using only the part of the MRO which comes
after `C`.

In other words, rather than resolving method invocation using the full MRO like
normal, `super` uses only the tail of an MRO.

For example, suppose I have an MRO like this:

```
[A, B, C, D, E, object]
```

and further suppose that I have a `super` object using this MRO and the class
`C` in this MRO. In that case, the `super` instance would only resolve to
methods implemented in `D`, `E`, or `object` (in that order.) In other words, a
call like this:

```py
super(C, A).foo()
```

would only resolve to an implementation of `foo()` in `D` or `E`.

Reference: http://sixty-north.com/blog/method-resolution-order-c3-and-super-proxies
