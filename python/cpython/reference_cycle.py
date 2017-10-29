import ctypes
import gc


class PyObject(ctypes.Structure):
    _fields_ = [('refcnt', ctypes.c_long)]

gc.disable()

l = []
l.append(l)

l_address = id(l)

del l

print('Generational GC is disabled:')

print(PyObject.from_address(l_address).refcnt)

# Force garbage collection by explicitly calling ``gc.collect()``.
# Notmally calling ``gc.enable()`` should be enough.
gc.collect()

print('Generational GC is enabled:')

print(PyObject.from_address(l_address).refcnt)
