## Free and bound variables in Lisp

A **bound** variable:

> A variable, V, is "bound in an expression", E, if the meaning of E is
> **unchanged** by the uniform replacement of a variable, W, not occurring in E,
> for every occurrence of V in E.

And a **free** variable:

> A variable, V, is "free in an expression"", E, if the meaning of E is
> **changed** by the uniform of replacement of a variable, W, not occurring in
> E, for every occurrence of V in E.

Let's look at an example:

```lisp
(lambda (x) (* x 2))
```

In this expression, `x` is bound according to the definition, because of we
change every occurrence of `x` by `w`, we get:

```lisp
(lambda (w) (* w 2))
```

Which is essentially the same expression. On the other hand, consider:

```lisp
(lambda (x) (* x y))
```

Here, `x` is still bound, but `y` is free. That is because if we change `y` to,
say, `z`:

```lisp
(lambda (x) (* x z))
```

We get an expression with a different meaning. To see an all-encompassing
example, consider this snippet of code:

```lisp
((lambda (x) (* x 2)) 6)
; 12

((lambda (w) (* w 2)) 6)
; 12
```

Nothing changes, really, because `x` (and now `w`) is bound in the
expression. On the other hand:

```lisp
(define y 5)
(define z 2)

((lambda (x) (* x y)) 9)
; 45

((lambda (x) (* x z)) 9)
; 18
```

Since `y` is free in the expression, substituting it for `z` changes the
expression's meaning.


### References

* http://eli.thegreenplace.net/2007/09/23/free-and-bound-variables-in-lisp/
* http://en.wikipedia.org/wiki/Lambda_calculus#Free_variables
* http://en.wiktionary.org/wiki/free_variable
