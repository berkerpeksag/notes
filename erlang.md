# Erlang Notes

An Erlang program is made up of modules where each module is a text file with the extension .erl. For
small programs, all modules typically reside in one directory.

```erl
-module(demo).
-export([double/1]).

double(X) -> times(X, 2).

times(X, N) -> X * N.
```

The above module demo consists of the function times/2 which is local to the module and the function
double/1 which is exported and can be called from outside the module.

double/1 means the function “double” with one argument. A function double/2 taking two arguments is
regarded as a different function. The number of arguments is called the arity of
the function.

A module attribute defines a certain property of a module and consists of a tag
and a value:

```erl
-Tag(Value).
```

Tag must be an atom, while Value must be a literal term. Any module attribute can
be specified. The attributes are stored in the compiled code and can be retrieved by calling the function
Module:module_info(attributes).

Pre-defined module attributes must be placed before any function declaration.

```erl
-module(Module).
```

This attribute is mandatory and must be specified first. It defines the name of the module. The name
Module, an atom, should be the same as the filename without the ‘.erl’
extension.

• -export([Func1/Arity1, ..., FuncN/ArityN]).
This attribute specifies which functions in the module that can be called from outside the module. Each
function name FuncX is an atom and ArityX an integer.
• -import(Module,[Func1/Arity1, ..., FuncN/ArityN]).
This attribute indicates a Module from which a list of functions are imported. For example:
-import(demo, [double/1]).
This means that it is possible to write double(10) instead of the longer demo:double(10) which can
be impractical if the function is used frequently.

Records and macros are defined in the same way as module attributes:

```erl
-record(Record,Fields).

-define(Macro,Replacement).
```

Records and macro definitions are also allowed between functions, as long as the definition comes before its
first use.

File inclusion is specified in the same way as module attributes:

```erl
-include(File).

-include_lib(File).
```

File is a string that represents a file name. Include files are typically used for record and macro definitions
that are shared by several modules. By convention, the extension .hrl is used
for include files.

```erl
-include("my_records.hrl").
-include("incdir/my_records.hrl").
-include("/home/user/proj/my_records.hrl").
```

include_lib is similar to include, but the first path component is assumed to be
the name of an application.

```erl
-include_lib("kernel/include/file.hrl").
```

An atom is a symbolic name, also known as a literal. Atoms begin with a lower-case letter, and may contain
alphanumeric characters, underscores (_) or at-signs (@). Alternatively atoms can be specified by enclosing
them in single quotes (’), necessary when they start with an uppercase character or contain characters other
than underscores and at-signs. For example:

```erl
hello
phone_number
'Monday'
'phone number'
'Anything inside quotes \n\012'
```

There is no boolean data type in Erlang. The atoms true and false are used
instead.

A reference is a term which is unique in an Erlang runtime system, created by the built-in function
make_ref/0.

A port identifier identifies a port.

A process identifier, pid, identifies a process.

A fun identifies a functional object.

A tuple is a compound data type that holds a fixed number of terms enclosed
within curly braces.

```erl
{Term1,...,TermN}
```

Each TermX in the tuple is called an element. The number of elements is called
the size of the tuple.

```erl
P = {adam, 24, {july, 29}}  % P is bound to {adam, 24, {july, 29}}
element(1, P)  % adam
element(3, P)  % {july,29}
P2 = setelement(2, P, 25)  % P2 is bound to {adam, 25, {july, 29}}
size(P)  % 3
size({})  % 0
```

A record is a named tuple with named elements called fields. A record type is defined as a module attribute,
for example:

```erl
-record(Rec, {Field1 [= Value1],
        ...
        FieldN [= ValueN]}).
```

Rec and Fields are atoms and each FieldX can be given an optional default ValueX. This definition may
be placed amongst the functions of a module, but only before it is used. If a record type is used by several
modules it is advisable to put it in a separate file for inclusion.

A new record of type Rec is created using an expression like this:

```erl
#Rec{Field1=Expr1, ..., FieldK=ExprK [, _=ExprL]}
```

The fields need not be in the same order as in the record definition. Fields omitted will get their respective
default values. If the final clause is used, omitted fields will get the value ExprL. Fields without default values
and that are omitted will have their value set to the atom undefined.
The value of a field is retrieved using the expression “Variable#Rec.Field”.

```erl
-module(employee).
-export([new/2]).
-record(person, {name, age, employed=erixon}).

new(Name, Age) -> #person{name=Name, age=Age}.
```

The function employee:new/2 can be used in another module which must also include the same record
definition of person.

```erl
{P = employee:new(ernie,44)}  % {person, ernie, 44, erixon}
P#person.age  % 44
P#person.employed  % erixon
```

When working with records in the Erlang shell, the functions rd(RecordName, RecordDefinition) and
rr(Module) can be used to define and load record definitions.

A list is a compound data type that holds a variable number of terms enclosed
within square brackets.

```erl
[Term1,...,TermN]
```

Each term TermX in the list is called an element. Common in functional programming, the first element is called the head of the list and the remainder (from
the 2nd element onwards) is called the tail of the list.

Note that individual elements within a list do not have
to have the same type, although it is common (and perhaps good) practice to do so — where mixed types
are involved, records are more commonly used.

BIFs to manipulate lists

* length(List) Returns the length of List
* hd(List) Returns the 1st (head) element of List
* tl(List) Returns List with the 1st element removed (tail)
