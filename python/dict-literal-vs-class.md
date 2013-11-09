# The Performance Impact of Using `dict()` Instead of `{}` in CPython 2.7

## tl;dr

With CPython 2.7, using `dict()` to create dictionaries takes up to 6 times
longer and involves more memory allocation operations than the literal
syntax. Use `{}` to create dictionaries, especially if you are pre-populating
them, unless the literal syntax does not work for your case.

## Initial Hypothesis

I wanted to study the performance difference between the literal syntax for
creating a dictionary instance (`{}`) and using the name of the class to create
one (`dict()`). I knew that the Python interpreter is based on opcodes and that
there are codes dedicated to creating a dictionary that would not be invoked
when the `dict()` form was used instead of the literal form. I suspected that
the extra overhead for looking up the name "dict" and then calling the function
would make the “function” form slower.

## What is going on?

After establishing the performance difference, I asked myself what was going on
to cause such a significant slowdown. To answer that question, I needed to look
more deeply into what the interpreter was doing as it processed each
expression. I wanted to see which (and how many) opcodes were being executed. I
used *dis* to disassemble the Python expressions to see which opcodes implement
each.

To use *dis* from the command line, I needed input files containing the
different expressions I was studying. I created `func.py`:

```py
dict()
```

and `literal.py`:

```py
{}
```

The output of *dis* is arranged in columns with the original source line number,
the instruction “address” within the code object, the opcode name, and any
arguments passed to the opcode.

```sh
$ python2.7 -m dis func.py
  1           0 LOAD_NAME                0 (dict)
              3 CALL_FUNCTION            0
              6 POP_TOP
              7 LOAD_CONST               0 (None)
             10 RETURN_VALUE
```

The function form uses two separate opcodes: `LOAD_NAME` to find the object
associated with the name “dict”, and `CALL_FUNCTION` to invoke it. The last
three opcodes are not involved in creating or populating the dictionary, and
appear in both versions of the code, so I ignored them for my analysis.

The literal form uses a special opcode to create the dictionary:

```sh
$ python2.7 -m dis literal.py
  1           0 BUILD_MAP                0
              3 POP_TOP
              4 LOAD_CONST               0 (None)
              7 RETURN_VALUE
```

The `BUILD_MAP` opcode creates a new empty dictionary instance and places it on
the top of the interpreter’s stack.

After comparing the two sets of opcodes, I suspected that the `CALL_FUNCTION`
operation was the culprit, since calling functions is relatively expensive in
Python. However, these were trivial examples and did not look like what I was
seeing in code reviews. Most of the actual code I had seen was populating the
dictionary as it created it, and I wanted to understand what difference that
would make.

## Examining More Complex Examples

I created two new source files that set three key/value pairs in the dictionary
as it is created. I started with `func-members.py`, which instantiated a
dictionary with the same members using the `dict()` function.

```py
dict(a="A",
     b="B",
     c="C",
     )
```

The disassembled version of `func-members.py` started the same way as the
earlier example, looking for the `dict()` function:

```sh
$ python2.7 -m dis func-members.py
  1           0 LOAD_NAME                0 (dict)
```

Then it showed key/value pairs being pushed onto the stack using `LOAD_CONST` to
create named arguments for the function.

```
            3 LOAD_CONST               0 ('a')
            6 LOAD_CONST               1 ('A')
            9 LOAD_CONST               2 ('b')

2          12 LOAD_CONST               3 ('B')
           15 LOAD_CONST               4 ('c')

3          18 LOAD_CONST               5 ('C')
```

Finally `dict()` was called:

```
21 CALL_FUNCTION          768
24 POP_TOP
25 LOAD_CONST               6 (None)
28 RETURN_VALUE
```

Next I created `literal-members.py`:

```py
{"a": "A",
 "b": "B",
 "c": "C",
 }
```

The disassembled version of this example showed a few differences from the
literal example without any values. First, the argument to `BUILD_MAP` was 3
instead of 0, indicating that there were three key/value pairs on the stack to
go into the dictionary.

```sh
$ python2.7 -m dis literal-members.py
  1           0 BUILD_MAP                3
```

It also showed the values and then keys being pushed onto the stack using
`LOAD_CONST`.

```
3 LOAD_CONST               0 ('A')
6 LOAD_CONST               1 ('a')
```

Finally, a new opcode, `STORE_MAP`, appeared once after each key/value pair is
processed.

```
9 STORE_MAP
```

The same pattern repeated for each of the other two key/value pairs.

```
2          10 LOAD_CONST               2 ('B')
           13 LOAD_CONST               3 ('b')
           16 STORE_MAP

3          17 LOAD_CONST               4 ('C')
           20 LOAD_CONST               5 ('c')
           23 STORE_MAP
           24 POP_TOP
           25 LOAD_CONST               6 (None)
           28 RETURN_VALUE
```

After looking at the output more closely, I noticed that there were actually
fewer opcodes in the function form than the literal form. There were no
`STORE_MAP` opcodes, just the `CALL_FUNCTION` after all of the items were on the
stack. At this point I realized that in order to really understand what was
going on, I would have to look at the interpreter implementation.

## Interpreter Source

The interpreter evaluates opcodes in a loop defined in `PyEval_EvalFrameEx()` in
[`Python/ceval.c`][cevalc]. Each opcode name corresponds to an entry in the
switch statement. For example, the `POP_TOP` opcode that appears near the end of
each disassembled example is implemented as:

[cevalc]: http://hg.python.org/cpython/file/121872879e91/Python/ceval.c

```c
        case POP_TOP:
            v = POP();
            Py_DECREF(v);
            goto fast_next_opcode;
```

The top-most item is removed from the stack and its reference count is
decremented to allow it (eventually) to be garbage collected. After orienting
myself in the source, I was ready to trace through the opcodes used in the
examples above.

## What Happens When You Call `dict()`?

The disassembly above shows that the opcodes used to call `dict()` to create a
dictionary are `LOAD_NAME`, `LOAD_CONST`, and `CALL_FUNCTION`.

The `LOAD_NAME` opcode finds the object associated with the given name (“dict”
in this case) and puts it on top of the stack.

```c
        case LOAD_NAME:
            w = GETITEM(names, oparg);
            if ((v = f->f_locals) == NULL) {
                PyErr_Format(PyExc_SystemError,
                             "no locals when loading %s",
                             PyObject_REPR(w));
                why = WHY_EXCEPTION;
                break;
            }
            if (PyDict_CheckExact(v)) {
                x = PyDict_GetItem(v, w);
                Py_XINCREF(x);
            }
            else {
                x = PyObject_GetItem(v, w);
                if (x == NULL && PyErr_Occurred()) {
                    if (!PyErr_ExceptionMatches(
                                    PyExc_KeyError))
                        break;
                    PyErr_Clear();
                }
            }
            if (x == NULL) {
                x = PyDict_GetItem(f->f_globals, w);
                if (x == NULL) {
                    x = PyDict_GetItem(f->f_builtins, w);
                    if (x == NULL) {
                        format_exc_check_arg(
                                    PyExc_NameError,
                                    NAME_ERROR_MSG, w);
                        break;
                    }
                }
                Py_INCREF(x);
            }
            PUSH(x);
            continue;
```

Three separate namespaces (represented as dictionaries) are searched. First, the
local namespace from inside any function scope, followed by the module global
namespace, and then the set of built-ins.

`LOAD_CONST` is the next opcode used. It pushes literal constant values onto the
interpreter’s stack:

```c
        case LOAD_CONST:
            x = GETITEM(consts, oparg);
            Py_INCREF(x);
            PUSH(x);
            goto fast_next_opcode;
```

The oparg value indicates which constant to take out of the set of constants
found in the code object. The constant’s reference count is increased and then
it is pushed onto the top of the stack. This is an inexpensive operation since
no name lookup is needed.

The portion of the implementation of `CALL_FUNCTION` in the case statement looks
similarly simple:

```c
        case CALL_FUNCTION:
        {
            PyObject **sp;
            PCALL(PCALL_ALL);
            sp = stack_pointer;
            x = call_function(&sp, oparg);
            stack_pointer = sp;
            PUSH(x);
            if (x != NULL)
                continue;
            break;
        }
```

The function is called and its return value is pushed onto the stack.

The implementation of `call_function()` starts to expose some of the complexity
of calling Python functions.

```c
static PyObject *
call_function(PyObject ***pp_stack, int oparg)
{
    int na = oparg & 0xff;
    int nk = (oparg>>8) & 0xff;
    int n = na + 2 * nk;
    PyObject **pfunc = (*pp_stack) - n - 1;
    PyObject *func = *pfunc;
    PyObject *x, *w;

    /* Always dispatch PyCFunction first, because these are
       presumed to be the most frequent callable object.
    */
    if (PyCFunction_Check(func) && nk == 0) {
        int flags = PyCFunction_GET_FLAGS(func);
        PyThreadState *tstate = PyThreadState_GET();

        PCALL(PCALL_CFUNCTION);
        if (flags & (METH_NOARGS | METH_O)) {
            PyCFunction meth = PyCFunction_GET_FUNCTION(func);
            PyObject *self = PyCFunction_GET_SELF(func);
            if (flags & METH_NOARGS && na == 0) {
                C_TRACE(x, (*meth)(self,NULL));
            }
            else if (flags & METH_O && na == 1) {
                PyObject *arg = EXT_POP(*pp_stack);
                C_TRACE(x, (*meth)(self,arg));
                Py_DECREF(arg);
            }
            else {
                err_args(func, flags, na);
                x = NULL;
            }
        }
        else {
            PyObject *callargs;
            callargs = load_args(pp_stack, na);
            READ_TIMESTAMP(*pintr0);
            C_TRACE(x, PyCFunction_Call(func,callargs,NULL));
            READ_TIMESTAMP(*pintr1);
            Py_XDECREF(callargs);
        }
    } else {
        if (PyMethod_Check(func) && PyMethod_GET_SELF(func) != NULL) {
            /* optimize access to bound methods */
            PyObject *self = PyMethod_GET_SELF(func);
            PCALL(PCALL_METHOD);
            PCALL(PCALL_BOUND_METHOD);
            Py_INCREF(self);
            func = PyMethod_GET_FUNCTION(func);
            Py_INCREF(func);
            Py_DECREF(*pfunc);
            *pfunc = self;
            na++;
            n++;
        } else
            Py_INCREF(func);
        READ_TIMESTAMP(*pintr0);
        if (PyFunction_Check(func))
            x = fast_function(func, pp_stack, n, na, nk);
        else
            x = do_call(func, pp_stack, na, nk);
        READ_TIMESTAMP(*pintr1);
        Py_DECREF(func);
    }

    /* Clear the stack of the function object.  Also removes
       the arguments in case they weren't consumed already
       (fast_function() and err_args() leave them on the stack).
     */
    while ((*pp_stack) > pfunc) {
        w = EXT_POP(*pp_stack);
        Py_DECREF(w);
        PCALL(PCALL_POP);
    }
    return x;
}
```

The number arguments the function is passed is given in `oparg`. The low-end
byte is the number of positional arguments, and the high-end byte is the number
of keyword arguments (lines 5-6). The value 768 in the example above translates
to 3 keyword arguments and 0 positional arguments.

```
21 CALL_FUNCTION          768
```

There are separate cases for built-in functions implemented in C, function
written in Python, and methods of objects. All of the cases eventually use
`load_args()` to pull the positional arguments off of the stack as a tuple:

```c
static PyObject *
load_args(PyObject ***pp_stack, int na)
{
    PyObject *args = PyTuple_New(na);
    PyObject *w;

    if (args == NULL)
        return NULL;
    while (--na >= 0) {
        w = EXT_POP(*pp_stack);
        PyTuple_SET_ITEM(args, na, w);
    }
    return args;
}
```

And then `update_keyword_args()` is used to pull keyword arguments off of the
stack as a dictionary:

```c
static PyObject *
update_keyword_args(PyObject *orig_kwdict, int nk, PyObject ***pp_stack,
                    PyObject *func)
{
    PyObject *kwdict = NULL;
    if (orig_kwdict == NULL)
        kwdict = PyDict_New();
    else {
        kwdict = PyDict_Copy(orig_kwdict);
        Py_DECREF(orig_kwdict);
    }
    if (kwdict == NULL)
        return NULL;
    while (--nk >= 0) {
        int err;
        PyObject *value = EXT_POP(*pp_stack);
        PyObject *key = EXT_POP(*pp_stack);
        if (PyDict_GetItem(kwdict, key) != NULL) {
            PyErr_Format(PyExc_TypeError,
                         "%.200s%s got multiple values "
                         "for keyword argument '%.200s'",
                         PyEval_GetFuncName(func),
                         PyEval_GetFuncDesc(func),
                         PyString_AsString(key));
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(kwdict);
            return NULL;
        }
        err = PyDict_SetItem(kwdict, key, value);
        Py_DECREF(key);
        Py_DECREF(value);
        if (err) {
            Py_DECREF(kwdict);
            return NULL;
        }
    }
    return kwdict;
}
```

In order to pass keyword arguments to `dict()` to instantiate a dictionary,
first another dictionary is created.

After the arguments are prepared, they are passed to `dict()`. The
implementation of the dictionary object is found in
[`Objects/dictobject.c`][dictobject], and the dict type is defined as:

```c
PyTypeObject PyDict_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "dict",
    sizeof(PyDictObject),
    0,
    (destructor)dict_dealloc,                   /* tp_dealloc */
    (printfunc)dict_print,                      /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    (cmpfunc)dict_compare,                      /* tp_compare */
    (reprfunc)dict_repr,                        /* tp_repr */
    0,                                          /* tp_as_number */
    &dict_as_sequence,                          /* tp_as_sequence */
    &dict_as_mapping,                           /* tp_as_mapping */
    (hashfunc)PyObject_HashNotImplemented,      /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_BASETYPE | Py_TPFLAGS_DICT_SUBCLASS,         /* tp_flags */
    dictionary_doc,                             /* tp_doc */
    dict_traverse,                              /* tp_traverse */
    dict_tp_clear,                              /* tp_clear */
    dict_richcompare,                           /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    (getiterfunc)dict_iter,                     /* tp_iter */
    0,                                          /* tp_iternext */
    mapp_methods,                               /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    dict_init,                                  /* tp_init */
    PyType_GenericAlloc,                        /* tp_alloc */
    dict_new,                                   /* tp_new */
    PyObject_GC_Del,                            /* tp_free */
};
```

Because `dict` is a class, `dict()` creates a new object and then invokes the
`__init__()` method. The initialization for `dict` is handled by `dict_init()`:

```c
static int
dict_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    return dict_update_common(self, args, kwds, "dict");
}
```

Which calls `dict_update_common()` to update the contents of the dictionary with
the arguments passed to the initialization function.

```c
static int
dict_update_common(PyObject *self, PyObject *args, PyObject *kwds, char *methname)
{
    PyObject *arg = NULL;
    int result = 0;

    if (!PyArg_UnpackTuple(args, methname, 0, 1, &arg))
        result = -1;

    else if (arg != NULL) {
        if (PyObject_HasAttrString(arg, "keys"))
            result = PyDict_Merge(self, arg, 1);
        else
            result = PyDict_MergeFromSeq2(self, arg, 1);
    }
    if (result == 0 && kwds != NULL)
        result = PyDict_Merge(self, kwds, 1);
    return result;
}
```

In this case, a set of keyword arguments are passed so the very last case is
triggered and `PyDict_Merge()` is used to copy the keyword arguments into the
dictionary. There are a couple of cases for merging, but from what I can tell
because there are two dictionaries involved the first case applies. The target
dictionary is resized to be big enough to hold the new values, and then the
items from the merging dictionary are copied in one at a time.

```c
int
PyDict_Merge(PyObject *a, PyObject *b, int override)
{
    register PyDictObject *mp, *other;
    register Py_ssize_t i;
    PyDictEntry *entry;

    /* We accept for the argument either a concrete dictionary object,
     * or an abstract "mapping" object.  For the former, we can do
     * things quite efficiently.  For the latter, we only require that
     * PyMapping_Keys() and PyObject_GetItem() be supported.
     */
    if (a == NULL || !PyDict_Check(a) || b == NULL) {
        PyErr_BadInternalCall();
        return -1;
    }
    mp = (PyDictObject*)a;
    if (PyDict_Check(b)) {
        other = (PyDictObject*)b;
        if (other == mp || other->ma_used == 0)
            /* a.update(a) or a.update({}); nothing to do */
            return 0;
        if (mp->ma_used == 0)
            /* Since the target dict is empty, PyDict_GetItem()
             * always returns NULL.  Setting override to 1
             * skips the unnecessary test.
             */
            override = 1;
        /* Do one big resize at the start, rather than
         * incrementally resizing as we insert new items.  Expect
         * that there will be no (or few) overlapping keys.
         */
        if ((mp->ma_fill + other->ma_used)*3 >= (mp->ma_mask+1)*2) {
           if (dictresize(mp, (mp->ma_used + other->ma_used)*2) != 0)
               return -1;
        }
        for (i = 0; i <= other->ma_mask; i++) {
            entry = &other->ma_table[i];
            if (entry->me_value != NULL &&
                (override ||
                 PyDict_GetItem(a, entry->me_key) == NULL)) {
                Py_INCREF(entry->me_key);
                Py_INCREF(entry->me_value);
                if (insertdict(mp, entry->me_key,
                               (long)entry->me_hash,
                               entry->me_value) != 0)
                    return -1;
            }
        }
    }
    else {
        /* Do it the generic, slower way */
        PyObject *keys = PyMapping_Keys(b);
        PyObject *iter;
        PyObject *key, *value;
        int status;

        if (keys == NULL)
            /* Docstring says this is equivalent to E.keys() so
             * if E doesn't have a .keys() method we want
             * AttributeError to percolate up.  Might as well
             * do the same for any other error.
             */
            return -1;

        iter = PyObject_GetIter(keys);
        Py_DECREF(keys);
        if (iter == NULL)
            return -1;

        for (key = PyIter_Next(iter); key; key = PyIter_Next(iter)) {
            if (!override && PyDict_GetItem(a, key) != NULL) {
                Py_DECREF(key);
                continue;
            }
            value = PyObject_GetItem(b, key);
            if (value == NULL) {
                Py_DECREF(iter);
                Py_DECREF(key);
                return -1;
            }
            status = PyDict_SetItem(a, key, value);
            Py_DECREF(key);
            Py_DECREF(value);
            if (status < 0) {
                Py_DECREF(iter);
                return -1;
            }
        }
        Py_DECREF(iter);
        if (PyErr_Occurred())
            /* Iterator completed, via error */
            return -1;
    }
    return 0;
}
```

## Creating a Dictionary with `{}`

The opcodes used to implement the literal examples are `BUILD_MAP`,
`LOAD_CONST`, and `STORE_MAP`. I started with the first opcode, `BUILD_MAP`,
which creates the dictionary instance:

```c
        case BUILD_MAP:
            x = _PyDict_NewPresized((Py_ssize_t)oparg);
            PUSH(x);
            if (x != NULL) continue;
            break;
```

The dictionary is created using `_PyDict_NewPresized()`, from
[`Objects/dictobject.c`][dictobject].

[dictobject]: http://hg.python.org/cpython/file/121872879e91/Objects/dictobject.c

```c
/* Create a new dictionary pre-sized to hold an estimated number of elements.
   Underestimates are okay because the dictionary will resize as necessary.
   Overestimates just mean the dictionary will be more sparse than usual.
*/

PyObject *
_PyDict_NewPresized(Py_ssize_t minused)
{
    PyObject *op = PyDict_New();

    if (minused>5 && op != NULL && dictresize((PyDictObject *)op, minused) == -1) {
        Py_DECREF(op);
        return NULL;
    }
    return op;
}
```

The argument for `BUILD_MAP` is the number of items that are going to be added
to the new dictionary as it is created. The disassembly for `literal-members.py`
showed that value as 3 earlier.

```
$ python2.7 -m dis literal-members.py
  1           0 BUILD_MAP                3
```

Specifying the initial number of items in the dictionary is an optimization for
managing memory, since it means the table size can be set ahead of time and it
does not need to be reallocated in some cases.

The argument for `BUILD_MAP` is the number of items that are going to be added
to the new dictionary as it is created.

Each key/value pair is added to the dictionary using three opcodes. Two
instances of `LOAD_CONST` push the value, then the key, onto the stack. Then a
`STORE_MAP` opcode adds the pair to the dictionary.

```
2          10 LOAD_CONST               2 ('B')
           13 LOAD_CONST               3 ('b')
           16 STORE_MAP
```

As we saw early, `LOAD_CONST` is fairly straightforward and
economical. `STORE_MAP` looks for the key, value, and dictionary on the stack
and calls `PyDict_SetItem()` to add the new key/value pair. The `STACKADJ(-2)`
line removes the key and value off from the stack.

```c
        case STORE_MAP:
            w = TOP();     /* key */
            u = SECOND();  /* value */
            v = THIRD();   /* dict */
            STACKADJ(-2);
            assert (PyDict_CheckExact(v));
            err = PyDict_SetItem(v, w, u);  /* v[w] = u */
            Py_DECREF(u);
            Py_DECREF(w);
            if (err == 0) continue;
            break;
```

`PyDict_SetItem()` is the same function invoked when a program uses `d[k] = v`
to associate the value v with a key k in a dictionary.

```c
int
PyDict_SetItem(register PyObject *op, PyObject *key, PyObject *value)
{
    register long hash;

    if (!PyDict_Check(op)) {
        PyErr_BadInternalCall();
        return -1;
    }
    assert(key);
    assert(value);
    if (PyString_CheckExact(key)) {
        hash = ((PyStringObject *)key)->ob_shash;
        if (hash == -1)
            hash = PyObject_Hash(key);
    }
    else {
        hash = PyObject_Hash(key);
        if (hash == -1)
            return -1;
    }
    return dict_set_item_by_hash_or_entry(op, key, hash, NULL, value);
}
```

The functions it calls handle resizing the internal data structure used by the
dictionary, if that’s necessary.

## Conclusions

In summary, calling `dict()` requires these steps:

1. Find the object associated with the name "dict" and push it onto the stack.
2. Push the key/value pairs onto the stack as constant values.
3. Get the key/value pairs off of the stack and create a dictionary to hold the
   keyword arguments to the function.
4. Call the constructor for dict to make a new object.
5. Initialize the new object by passing the keyword arguments to its
   initialization method.
6. Resize the new dict and copy the key/value pairs into it from the keyword
   arguments.

Whereas using `{}` to create a dictionary uses only these steps:

1. Create an empty but pre-allocated dictionary instance.
2. Push the key/value pairs onto the stack as constant values.
3. Store each key/value pair in the dictionary.

The times involved here are pretty small, but as a general principle I try to
avoid code constructions I know to introduce performance hits. On the other
hand, there may be times when using `dict()` is necessary, or easier.

*Doug Hellmann*

http://doughellmann.com/2012/11/the-performance-impact-of-using-dict-instead-of-in-cpython-2-7-2.html
