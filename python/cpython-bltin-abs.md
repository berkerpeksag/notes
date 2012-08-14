# abs() implementation

**Python/bltinmodule.c**

```c
static PyObject *
builtin_abs(PyObject *self, PyObject *v)
{
    return PyNumber_Absolute(v);
}

PyDoc_STRVAR(abs_doc,
"abs(number) -> number\n\
\n\
Return the absolute value of the argument.");
```

**Objects/abstract.c**

```c
PyObject *
PyNumber_Absolute(PyObject *o)
{
    PyNumberMethods *m;

    if (o == NULL)
        return null_error();
    m = o->ob_type->tp_as_number;
    if (m && m->nb_absolute)
        return m->nb_absolute(o);

    return type_error("bad operand type for abs(): '%.200s'", o);
}
```

### Usage

```python
print(abs.__doc__)
print(abs(4))
```
