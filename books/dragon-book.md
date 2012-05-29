# Dragon Book

## Chapter 1. Introduction

### Names, Identifiers, and Variables

Although the terms "name" and "variable," often refer to the same thing,
we use them carefully to distinguish between compile-time names and the
run-time locations denoted by names.

An *identifier* is a string of characters, typically letter or digits,
that refers to (identifies) an entity, such as a data object, a procedure,
a class, or a type. All identifiers are names, but not all names, but not
all names are identifiers. Names can also be expressions.  For example,
the name `x.y` might denote the field *y* of a structure denoted by *x*.
Here, *x* and *y* are identifiers, while `x.y` is a name, but not an
identifier. Composite names likes like `x.y` are called *qualified* names.

A *variable* refers to a particular location of the store. It is common
for the sanme identifier to be declared more than once; each such declaration
introduces a variable. Even if each identifier is declared just once, an
identifier local to a recursive procedure will refer to different locations
of the store at different times.

### Procedures, Functions, and Methods

To avoid saying "procedures, functions, or methods," each time we want to
talk about a *subprogram* that may be called, we shall usually refer to all
of them as "procedures." The exception is that when talking explicitly of
programs in languages like C that have only functions, we sahll refer to
them as "functions." Or, if we are discussing a language like Java that has
only methods, we shall use that term instead.

A function generally returns a value of some type (the "return type"), while 
a procedure does not any value. C and similar languages, which have only 
functions, treat procedures as functions that have a special return type
"void," to signify no return value. Object-oriented languages like Java and
C++ use the term "methods." These can behave like either functions or
procedures, but are associated with a particular class.
