"""
Shows how to use the jitcompiler.jit decorator to automatically compile the
function to native code on the first call.
"""

import minijit

print("Definition point of foo\n")


@minijit.jit
def foo(a, b):
    return a*a - b*b


def test(a, b):
    result = foo(a, b)
    print("foo(%d, %d) => %d" % (a, b, result))
    assert result == (a*a - b*b)

print("\nCalling foo\n")
test(1, 2)
test(2, 3)

print("\nDisassembly of foo\n")
print(minijit.disassemble(foo))
