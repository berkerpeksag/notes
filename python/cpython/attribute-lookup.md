# Attribute lookup in CPython

```py
class Foo:
    spam = 42

f = Foo()
f.spam
f.x
```

As shown below, attribute lookup is initiated by the `LOAD_ATTR` bytecode.

```py
 7          28 LOAD_NAME                1 (f)
            31 LOAD_ATTR                2 (spam)
            34 POP_TOP

 8          35 LOAD_NAME                1 (f)
            38 LOAD_ATTR                3 (x)
            41 POP_TOP
            42 LOAD_CONST               2 (None)
            45 RETURN_VALUE
```

What `LOAD_ATTR(namei)` does is replacing `TOS` (top-of-stack) with
`getattr(TOS, co_names[namei])`

`Python/ceval.c`:

```c
TARGET(LOAD_ATTR) {
    PyObject *name = GETITEM(names, oparg);
    PyObject *owner = TOP();
    PyObject *res = PyObject_GetAttr(owner, name);
    Py_DECREF(owner);
    SET_TOP(res);
    if (res == NULL)
        goto error;
    DISPATCH();
}
```

We get the value (TOS) by calling `TOP()` and the attribute name by calling
`GETITEM(names, oparg)`.


`Objects/object.c`:

```c
PyObject *
PyObject_GetAttr(PyObject *v, PyObject *name)
{
    PyTypeObject *tp = Py_TYPE(v);

    if (!PyUnicode_Check(name)) {
        PyErr_Format(PyExc_TypeError,
                     "attribute name must be string, not '%.200s'",
                     name->ob_type->tp_name);
        return NULL;
    }
    if (tp->tp_getattro != NULL)
        return (*tp->tp_getattro)(v, name);
    if (tp->tp_getattr != NULL) {
        char *name_str = PyUnicode_AsUTF8(name);
        if (name_str == NULL)
            return NULL;
        return (*tp->tp_getattr)(v, name_str);
    }
    PyErr_Format(PyExc_AttributeError,
                 "'%.50s' object has no attribute '%U'",
                 tp->tp_name, name);
    return NULL;
}
```

`PyObject_GetAttr(obj, name)` will call the `tp_getattro` slot of `type(obj)`
with `obj` and `name` parameters by default:

```c
if (tp->tp_getattro != NULL)
    return (*tp->tp_getattro)(v, name);
```

`tp_getattro` is a function pointer which points to either the
`PyObject_GenericGetAttr` function in `Objects/object.c` or to the
`slot_tp_getattro` or the `slot_tp_getattr_hook` functions in
`Objects/typeobject.c`.

A slot is an attribute on a type which points to a function or a structure
The CPython interpreter will invoke the functions that are stored in slots.
All members of the `PyTypeObject` structure can be found on [official
documentation](https://docs.python.org/3/c-api/typeobj.html).

If either of `__getattr__` or `__getattribute__` is overridden by the user
defined class, `tp_getattro` will point to `slot_tp_getattr_hook`:

```py
class Spam:

    def __getattr__(self, name):
        return getattr(self, name)
```

Otherwise, it will point to `PyObject_GenericGetAttr`:

```py
class Eggs:
    pass
```

Since we don't see a lot of user defined classed that are override either
`__getattr__` and `__getattribute__` methods, let's take a look at what
`PyObject_GenericGetAttr` does internally. `PyObject_GenericGetAttr` is
basically a wrapper that calls `_PyObject_GenericGetAttrWithDict(obj, name,
NULL)`.

`Objects/object.c`:

```c
PyObject *
_PyObject_GenericGetAttrWithDict(PyObject *obj, PyObject *name, PyObject *dict)
{
    PyTypeObject *tp = Py_TYPE(obj);
    PyObject *descr = NULL;
    PyObject *res = NULL;
    descrgetfunc f;
    Py_ssize_t dictoffset;
    PyObject **dictptr;

    Py_INCREF(name);

    /* Removed some sanity checks to make the code easy to understand */

    descr = _PyType_Lookup(tp, name);

    f = NULL;
    if (descr != NULL) {
        Py_INCREF(descr);
        f = descr->ob_type->tp_descr_get;
        if (f != NULL && PyDescr_IsData(descr)) {
            res = f(descr, obj, (PyObject *)obj->ob_type);
            goto done;
        }
    }

    if (dict == NULL) {
        /* Inline _PyObject_GetDictPtr */
        dictoffset = tp->tp_dictoffset;
        if (dictoffset != 0) {
            if (dictoffset < 0) {
                Py_ssize_t tsize;
                size_t size;

                tsize = ((PyVarObject *)obj)->ob_size;
                if (tsize < 0)
                    tsize = -tsize;
                size = _PyObject_VAR_SIZE(tp, tsize);
                assert(size <= PY_SSIZE_T_MAX);

                dictoffset += (Py_ssize_t)size;
                assert(dictoffset > 0);
                assert(dictoffset % SIZEOF_VOID_P == 0);
            }
            dictptr = (PyObject **) ((char *)obj + dictoffset);
            dict = *dictptr;
        }
    }
    if (dict != NULL) {
        Py_INCREF(dict);
        res = PyDict_GetItem(dict, name);
        if (res != NULL) {
            Py_INCREF(res);
            Py_DECREF(dict);
            goto done;
        }
        Py_DECREF(dict);
    }

    if (f != NULL) {
        res = f(descr, obj, (PyObject *)Py_TYPE(obj));
        goto done;
    }

    if (descr != NULL) {
        res = descr;
        descr = NULL;
        goto done;
    }

    PyErr_Format(PyExc_AttributeError,
                 "'%.50s' object has no attribute '%U'",
                 tp->tp_name, name);
  done:
    Py_XDECREF(descr);
    Py_DECREF(name);
    return res;
}
```

* `_PyType_Lookup`: Lookup the attribute name in MRO
* If the result of the `_PyType_Lookup` is a data descriptor (which is an
  object that defines both `__get__` and `__set__` methods), it will call the
  `__get__` method of the descriptor:

  ```c
  result->ob_type->tp_descr_get(result, obj, (PyObject *)obj->ob_type);
  ```
* Otherwise, it will lookup to the instance dictionary of the class by
  calling `PyDict_GetItem(dict, name)`. Since we've passed `NULL` to `dict`,
  we need to get the instance dictionary of our object first:

  ```c
  if (dict == NULL) {
    dictptr = _PyObject_GetDictPtr(obj);
    dict = *dictptr;
  }
  ```
* If the instance dictionary doesn't contain the attribute, but the attribute
  was found in MRO and the attribute pointed to a non-data descriptor (an
  object that only defined the `__get__` method) then resolve the attribute
  lookup by calling the `__get__` method of the descriptor:

  ```c
  result->ob_type->tp_descr_get(result, obj, (PyObject *)Py_TYPE(obj));
  ```
* Raise `AttributeError` if we didn't find the attribute in any of the steps
  we explained above.

If we have a class that overrides `__getattr__` or `__getattribute__`, it will
call `slot_tp_getattr_hook`. Since overriding `__getattr__` is much more
common, we are going to ignore `__getattribute__` to make the code shorter:

```c
static PyObject *
slot_tp_getattr_hook(PyObject *self, PyObject *name)
{
    PyTypeObject *tp = Py_TYPE(self);
    PyObject *getattr, *res;
    _Py_IDENTIFIER(__getattr__);
    getattr = _PyType_LookupId(tp, &PyId___getattr__);
    if (getattr == NULL) {
        tp->tp_getattro = slot_tp_getattro;
        /* This means that the object implements a custom
           __getattribute__ method so tp_slot_getattro will
           simply invoke the custom __getattribute__ method.

           Side note: __getattribute__ will point to
           PyObject_GenericGetAttr by default. */
        return slot_tp_getattro(self, name);
    }
    Py_INCREF(getattr);
    res = call_attribute(self, getattr, name);
    Py_DECREF(getattr);
    return res;
}
```

If `PyObject_GenericGetAttr` (because `__getattribute__` is always defined and
it points to `PyObject_GenericGetAttr` by default so `__getattribute__` will
always be called before `__getattr__`) or the custom `__getattribute__` method
raises an `AttributeError`, then the custom `__getattr__` method will be
invoked.
