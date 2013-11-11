# Python object creation sequence

*(Python 3)*

This article aims to explore the process of creating new objects in
Python. Object creation is just a special case of calling a callable. Consider
this Python code:

```py
class Joe:
    pass

j = Joe()
```


## What happens when `j = Joe()` is executed?

1. Python sees it as a call to the callable `Joe`, and routes it to the internal
   function `PyObject_Call`, with `Joe` passed as the first argument.
2. `PyObject_Call` looks at the type of its first argument to extract its
   `tp_call` attribute.

## Now, what is the type of `Joe`?

Whenever we define a new Python class, unless we explicitly specify a metaclass
for it, its type is `type`. Therefore, when `PyObject_Call` attempts to look at
the type of `Joe`, it finds type and picks its `tp_call` attribute.

In other words, the function `type_call` in `Objects/typeobject.c` is
invoked. The `PyTypeObject` structure definition for `type` is `PyType_Type` in
`Objects/typeobject.c`. You can see that `type_call` is being assigned to its
`tp_call` slot:

```c
static PyObject *
type_call(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *obj;

    if (type->tp_new == NULL) {
        PyErr_Format(PyExc_TypeError,
                     "cannot create '%.100s' instances",
                     type->tp_name);
        return NULL;
    }

    obj = type->tp_new(type, args, kwds);
    if (obj != NULL) {
        /* Ugly exception: when the call was type(something),
           don't call tp_init on the result. */
        if (type == &PyType_Type &&
            PyTuple_Check(args) && PyTuple_GET_SIZE(args) == 1 &&
            (kwds == NULL ||
             (PyDict_Check(kwds) && PyDict_Size(kwds) == 0)))
            return obj;
        /* If the returned object is not an instance of type,
           it won't be initialized. */
        if (!PyType_IsSubtype(Py_TYPE(obj), type))
            return obj;
        type = Py_TYPE(obj);
        if (type->tp_init != NULL &&
            type->tp_init(obj, args, kwds) < 0) {
            Py_DECREF(obj);
            obj = NULL;
        }
    }
    return obj;
}
```

So what arguments is `type_call` being passed in our case? The first one is
`Joe` itself – but how is it represented? Well, `Joe` is a class, so it's a
`type`. Types are represented inside the CPython VM by `PyTypeObject` objects.

What `type_call` does is first call the `tp_new` attribute of the given
type. Then, it checks for a special case we can ignore for simplicity, makes
sure `tp_new` returned an object of the expected type, and then calls
`tp_init`. If an object of a different type was returned, it is not being
initialized.

Translated to Python, what happens is this: if your class defines the `__new__`
special method, it gets called first when a new instance of the class is
created. This method has to return some object. Usually, this will be of the
required type, but this doesn’t have to be the case. Objects of the required
type get `__init__` invoked on them. Here’s an example:

```py
class Joe:
    def __new__(cls, *args, **kwargs):
        obj = super(Joe, cls).__new__(cls)
        print('__new__ called. got new obj id=0x%x' % id(obj))
        return obj

    def __init__(self, arg):
        print('__init__ called (self=0x%x) with arg=%s' % (id(self), arg))
        self.arg = arg

j = Joe(12)
print(type(j))
```

This prints:

```
__new__ called. got new obj id=0x7f88e7218290
__init__ called (self=0x7f88e7218290) with arg=12
<class '__main__.Joe'>
```

## Customizing the sequence

As we saw above, since the type of `Joe` is `type`, the `type_call` function is
invoked to define the creation sequence for `Joe` instances. This sequence can
be changed by specifying a custom type for `Joe` – in other words, a
metaclass. Let’s modify the previous example to specify a custom metaclass for
`Joe`:

```py
class MetaJoe(type):
    def __call__(cls, *args, **kwargs):
        print('MetaJoe.__call__')
        return None

class Joe(metaclass=MetaJoe):
    def __new__(cls, *args, **kwargs):
        obj = super(Joe, cls).__new__(cls)
        print('__new__ called. got new obj id=0x%x' % id(obj))
        return obj

    def __init__(self, arg):
        print('__init__ called (self=0x%x) with arg=%s' % (id(self), arg))
        self.arg = arg

j = Joe(12)
print(type(j))
```

So now the type of `Joe` is not `type`, but `MetaJoe`. Consequently, when
`PyObject_Call` picks the call function to execute for `j = Joe(12)`, it takes
`MetaJoe.__call__`. The latter prints a notice about itself and returns `None`,
so we don’t expect the `__new__` and `__init__` methods of `Joe` to be called at
all. Indeed, this is the outcome:

```
MetaJoe.__call__
<class 'NoneType'>
```

## Digging deeper – `tp_new`

Alright, so now we have a better understanding of the object creation
sequence. One crucial piece of the puzzle is still missing, though. While we
almost always define `__init__` for our classes, defining `__new__` is rather
rare. Even when we do explicitly override `__new__` in our classes, we almost
certainly defer the actual object creation to the base’s `__new__`.

Moreover, from a quick look at the code it’s obvious that `__new__` is more
fundamental in a way. This method is used to create a new object. It is called
once and only once per instantiation. `__init__`, on the other hand, already
gets a constructed object and may not be called at all; it can also be called
multiple times.

Since the `type` parameter passed to `type_call` in our case is `Joe`, and `Joe`
does not define a custom `__new__` method, then `type->tp_new` defers to the
`tp_new` slot of the base type. The base type of `Joe` (and all other Python
objects, except `object` itself) is `object`. The `object.tp_new` slot is
implemented in CPython by the `object_new` function in `Objects/typeobject.c`.

`object_new` is actually very simple. It does some argument checking, verifies
that the type we’re trying to instantiate is not abstract, and then does this:

```c
return type->tp_alloc(type, 0);
```

`tp_alloc` is a low-level slot of the type object in CPython. It’s not directly
accessible from Python code, but should be familiar to C extension developers. A
custom type defined in a C extension may override this slot to supply a custom
memory allocation scheme for instances of itself. Most C extension types will,
however, defer this allocation to the function `PyType_GenericAlloc`.

This function is part of the public C API of CPython, and it also happens to be
assigned to the `tp_alloc` slot of `object` (defined in
`Objects/typeobject.c`). It figures out how much memory the new object needs
(this information is available in the `PyObject` header of any type), allocates
a memory chunk from CPython’s memory allocator and initializes it all to
zeros. It then initializes the bare essential `PyObject` fields (type and
reference count), does some GC bookkeeping and returns. The result is a freshly
allocated instance.

## Conclusion

What happens when CPython executes `j = Joe()`?

* Since `Joe` has no explicit metaclass, `type` is its type. So the `tp_call`
  slot of `type`, which is `type_call`, is called.
* `type_call` starts by calling the `tp_new` slot of `Joe`:
    - Since `Joe` has no explicit base class, its base is `object`. Therefore,
      `object_new` is called.
    - Since `Joe` is a Python-defined class, it has no custom `tp_alloc` slot.
      Therefore, `object_new` calls `PyType_GenericAlloc`.
    - `PyType_GenericAlloc` allocates and initializes a chunk of memory big
      enough to contain `Joe`.
* `type_call` then goes on and calls `Joe.__init__` on the newly created object.
    - Since `Joe` does not define `__init__`, its base’s `__init__` is called,
      which is `object_init`.
    - `object_init` does nothing.
* The new object is returned from `type_call` and is bound to the name `j`.

This is the vanilla flow for an object of a class that doesn’t have a custom
metaclass, doesn’t have an explicit base class, and doesn’t define its own
`__new__` and `__init__` methods.

Practically every single step of the process described above can be customized,
even for user-defined types implemented in Python. Types implemented in a C
extension can customize even more, such as the exact memory allocation strategy
used to create instances of the type.

http://eli.thegreenplace.net/2012/04/16/python-object-creation-sequence/
