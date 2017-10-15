"""
Structure of PyLongObject

struct _longobject {
    ssize_t ob_refcnt;
    struct _typeobject *ob_type;
    ssize_t ob_size;
    uint32_t ob_digit[1];
} PyLongObject;

Implementation based on
https://rushter.com/blog/python-integer-implementation/
"""

import ctypes

SHIFT = 30  # Number of bits for each 'digit'.
MASK = 2 ** SHIFT
bignum = 18446744073709551615


def split_number(bignum):
    t = abs(bignum)
    num_list = []
    while t != 0:
        # Get remainder from division.
        small_int = t & (MASK - 1)  # more readable: t % MASK
        num_list.append(small_int)
        # Get integral part of the division (floor division)
        t >>= SHIFT  # more readable: t // MARK
    return num_list


def restore_number(num_list):
    bignum = 0
    for i, n in enumerate(num_list):
        bignum += n * (2 ** (SHIFT * i))
    return bignum


num_list = split_number(bignum)

print('bignum:', bignum)
print('stored in a PyLongObject as:', num_list)
print('restored bignum:', restore_number(num_list))


class PyLongObject(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_long),
        ('ob_type', ctypes.c_void_p),
        ('ob_size', ctypes.c_ulong),
        ('ob_digit', ctypes.c_uint * 3),
    ]


num_list_from_pylongobject = [
    n for n in PyLongObject.from_address(id(bignum)).ob_digit
]

print('check it from the actual PyLongObject:', num_list_from_pylongobject)
