# Stepping Through Python

## Breakpoint 1

```sh
$ gdb python3
(gdb) break main
(gdb) run stepping.py
```

### `main`

Lives in `Modules/python.c`.

* Copies argv
* Sets locale
* Calls `Py_Main`

### Memory Management

Two families:

1. `PyMem_`
2. `PyObject_` memory

**Note:** Don't call `malloc()`.

#### 1. `PyMem_`

* `Include/pymem.h`
* `Objects/object.c`

* `PyMem_Malloc()` just calls `malloc()`.
* There is a preprocessor called `PyMem_MALLOC()`.

## Breakpoint 2

```sh
(gdb) break Py_Main
(gdb) c
```

### `Py_Main`

Lives in `Modules/main.c`.

* `_PyOS_Getopt`
* `Py_GETENV`
* stdio
* `Py_Initialize` (loads builtin modules etc.)
* Run script / `-m module` / `-c "command"`

## Breakpoint 3

```sh
(gdb) break _PyObject_New
(gdb) c
(gdb) n
241	    op = (PyObject *) PyObject_MALLOC(_PyObject_SIZE(tp));
```

and delete the breakpoint:

> **Not:** Eğer bunu kaldırmazsak GDB oturumu boyunca sürekli bu satıra
> denk geleceğiz.

```sh
(gdb) clear _PyObject_New
```

### `PyObject`

Lives in `Include/object.h` and `Objects/object.c`.

**Note:** Almost everything is `PyObject` in the CPython interpreter.

```c
typedef struct _object {
	_PyObject_HEAD_EXTRA
	Py_ssize_t ob_refcnt;
	struct _typeobject *ob_type;
} PyObject;
```

[08:03]
