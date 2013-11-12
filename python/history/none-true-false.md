# The story of None, True and False
(and an explanation of literals, keywords and builtins thrown in)

*Guido van Rossum*

I received an interesting question in the mail recently:

> What is the difference between keywords and literals? Why are True and False
> keywords rather than literals in Python 3?
> I was horrified recently to find that assigning to True/False works in Python
> 2. So I went digging, and found that True and False were created to be
> 'constants' like None in PEP 285. Assignment to None was disallowed in 2.4,
> but not to True/False until Python 3. Was there a reason None was originally
> built as a variable rather than a literal?

Let's start with the first question: keywords and literals.

A keyword, in the context of defining the syntax of a language, also known as a
reserved word, is something that looks like an identifier in the language, but
from the parser's point of view act like a token of the language. An identifier
is defined as a sequence of one or more letters, digits and underscores, not
starting with a digit. (This is Python's definition, but many languages, like C
or Java, use the same or a very similar definition.)

The important thing to remember about keywords is that a keyword cannot be used
to name a variable (or function, class, etc.). Some well-known keywords in
Python include 'if', 'while', 'for', 'and', 'or'.

A literal, on the other hand, is an element of an expression that describes a
constant value. Examples of literals are numbers (e.g. 42, 3.14, or 1.6e-10) and
strings (e.g. "Hello, world"). Literals are recognized by the parser, and the
exact rules for how literals are parsed are often quite subtle. For example,
these are all numeric literals in Python 3:

* 123
* 1.0
* 1.
* .01e10
* .1e+42
* 123.456e-100
* 0xfffe
* 0o755

but these are not:

* . (dot)
* e10 (identifier)
* 0y12 (the literal 0 followed by the identifier y12)
* 0xffe+10 (the literal 0xffe followed by a plus sign and and the number 10)

Note the distinction between a constant and a literal. We often write code
defining "constants", e.g.

```py
MAX_LEVELS = 15
```

Here, 15 is a literal, but MAX_LEVELS is not -- it is an identifier, and the
all-caps form of the name suggests to the reader that it is probably not changed
anywhere in the code, which means that we can consider it a constant -- but this
is just a convention, and the Python parser doesn't know about that convention,
nor does it enforce it.

On the other hand, the parser won't let you write

```py
15 = MAX_LEVELS
```

This is because the left-hand side of the assignment operator (=) must be a
variable, and a literal is not a variable. (The exact definition of variable is
complex, since some things that look like expressions are also considered to be
variables, such as d[k], (a, b), and foo.bar -- but not f() or () or 42. This
definition of variable is also used by the "del" statement.)

Now on to None, True and False.

Let's begin with None, because it has always been in the language. (True and
False were relatively recent additions -- they first made their appearance in
Python 2.2.1, to be precise.) None is a singleton object (meaning there is only
one None), used in many places in the language and library to represent the
absence of some other value. For example, if d is a dictionary, d.get(k) will
return d[k] if it exists, but None if d has no key k. In earlier versions of
Python, None was just a "built-in name". The parser had no special knowledge of
None -- just like it doesn't have special knowledge of built-in types like int,
float or str, or built-in exceptions like KeyError or ZeroDivisionError. All of
these are treated by the parser as identifiers, and when your code is being
interpreted they are looked up just like any other names (e.g. the functions and
variables you define yourself). So from the parser's perspective, the following
are treated the same, and the parse tree it produces (<name> = <name>) is the
same in each case:

```py
x = None
x = int
x = foobar
```

On the other hand, the following produce different parse trees (<name> =
<literal>):

```py
x = 42
x = 'hello'
```

Because the parser treats numeric and string literals as different from
identifiers. Combining this with the earlier MAX_LEVEL examples, we can see that
if we swap the left and right hand sides, the first three will still be accepted
by the parser (<name> = <name>), while the swapped version of the second set
will be rejected (<literal> = <name> is invalid).

The practical consequence is that, if you really want to mess with your readers,
you can write code that reassigns built-ins; for example, you could write:

```py
int = float
def parse_string(s):
    return int(s)
print(parse_string('42'))  # Will print '42.0'
```

Some of you may respond to this with "So what? Reasonable programmers don't
write such code." Others may react in the opposite way, saying "Why on earth
does the language allow assignment to a built-in name like 'int' at all?!"

The answer is subtle, and has to do with consistency and evolution of the
language. I bet that without looking it up you won't be able to give a complete
list all built-in names defined by Python. (I know I can't.) Moreover, I bet
that many of you won't recognize every single name on that list. (To see the
list, try typing `dir(__builtins__)` at the Python command prompt.)

Take for example the weird built-ins named copyright, credits or license. They
exist so that we can mention them in the greeting shown when you start Python
interactively:

```py
Python 3.4.0a4+ (default:0917f6c62c62, Oct 22 2013, 10:55:35)
[GCC 4.2.1 Compatible Apple LLVM 4.2 (clang-425.0.28)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> credits
Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
for supporting Python development.  See www.python.org for more information.
>>>
```

In order for this to work, we made them built-ins. But does this mean you
shouldn't be allowed to use 'credits' as a variable or parameter name? I think
not. Certainly many people don't realize that these esoteric built-ins even
exist, and they would be surprised if they were prevented from using them as
variable names. From here, it's just a gradual path. Many people write functions
or methods with arguments named str or len, or with names like compile or
format. Moreover, suppose you wrote some Python 2.5 code where you used bytes as
a variable name. In Python 2.6, we added a built-in function named 'bytes' (it's
an alias for str, actually). Should your code now be considered invalid? There's
no reason for that, and in fact your code will be fine. (Even in Python 3, where
bytes is one of the fundamental types.)

On the other hand, you cannot have a variable named 'if' or 'try', because these
are reserved words (keywords) that are treated special by the parser. Because
you cannot use these as variable or function names anywhere, ever, in any Python
program, everyone using Python has to know about all the reserved words in the
language, even if they don't have any need for them. For this reason, we try to
keep the list of reserved words small, and the core developers hem and haw a lot
before adding a new reserved word to the language.

In fact, many proposed new features have been killed because they would require
a new keyword; others have been modified to avoid that need. Also, when we do
decide to add a new keyword, we start a deprecation campaign at least one
release before the new keyword is introduced, warning developers to choose a
different name for their variables. (There's also a trick to allow developers to
choose to use the new keyword right away; this is why we have e.g. `from
__future__ import with_statement`.)

There's no such concern for built-ins. Code that happens to use the name of a
new built-in as a variable or function name will continue to function (as long
as you don't also try to use the new built-in in the same function). While we
still try to be conservative with the introduction of new built-ins, at least we
don't have to worry about breaking working code by merely adding something to
the language. The (small) price we pay for this is the possibility that some
joker intentionally redefines a built-in just to confuse others. But there are
tons of other ways to write unreadable code, and I don't see this as a
particularly bad problem.

So, after this long detour about built-ins vs. keywords, back to None. Why did
we eventually make None a reserved word? Frankly, the reasons were perhaps
mostly social. Unlike some built-ins and many exceptions, None is so central to
using Python that you really can't be using Python without knowing about
None. So people were (like our question-asker) "horrified" when they found that
assignment to None was actually allowed at all. Worse, there was the concern
(whether founded or not) that the way name lookup in Python works, "evaluating"
the expression None is slow, because it requires at least two dictionary lookups
(all names are looked up in the globals dict before being looked up in the
built-ins dict).

In the end we decided that there was no downside to making None a keyword (there
is no code that actually assigns to it) and it might make some code a tiny bit
faster, or catch rare typos. There was still a one-time cost to the developer
community (changes to the parser and documentation) but this was small enough
that we din't hesitate very long.

The situation for True/False is a little different. They weren't always part of
the language, and many people had invented their own convention. People would
define constants named true and false, True and False, or TRUE and FALSE, and
use those consistently throughout their code. I don't recall which spelling was
most popular, but when we introduced True and False into the language, we
definitely did not want to break any packages that were defining their own True
and False constants. (One concern was that those packages would have to have a
way to continue to run on previous Python versions.)

So, essentially our hand was forced in this case, and we had to introduce True
and False as built-in constants, not as keywords. But over time, code defining
its own versions of True and False (by whichever name) became more and more
frowned upon, and by the time Python 3 came around, when we looked at
opportunities for cleaning up the language, we found that it was logical to make
True and False keywords, by analogy to None.

And there you have it. It's all completely logical, once you understand the
context. :-) Sorry for the long response; I hope it's been educational.

**UPDATE**: I still forgot to answer whether None/True/False are literals or
keywords. My answer is that they are both. They are keywords because that's
how the parser recognizes them. They are literals because that's their role in
expressions and because they stand for constant values. One could argue about
whether things like `{'foo': 42}` are literals; personally I'd prefer to give
these some other name, because otherwise what would you call `{'foo': x+1}`?
The [language reference][langref] calls both of these "displays".

[langref]: http://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries

http://python-history.blogspot.ro/2013/11/story-of-none-true-false.html
