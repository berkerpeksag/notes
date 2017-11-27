import random
import unittest

import minijit

test_cases = []


def test(function):
    test_cases.append(function)
    return function


@test
def example0(n):
    return n


@test
def example1(n):
    return n*101


@test
def example2(a, b):
    return a*a + b*b


@test
def example3(a):
    b = a*101
    return b + a + 2


@test
def example4(a, b, c):
    return a*a + 2*a*b + c


@test
def example5(n):
    n -= 10
    return n


@test
def example6(a, b):
    return a*a - b*b


@test
def example7(a, b, c):
    return (a+c)*b - a*a*(a-c-b)-b*2+(c*(2+3*a*b-c*a)-3*c)


@test
def foo(a, b):
    return a*a - b*b


class MiniJitTestCase(unittest.TestCase):

    def assertCompiles(self, function):
        native, asm = minijit.compile_native(function)
        for n in range(10):
            # Create random arguments.
            argcount = function.__code__.co_argcount
            args = [random.randint(-999, 999) for x in range(argcount)]

            # Run original and compiled functions.
            expected = function(*args)
            actual = native(*args)
            self.assertEqual(expected, actual)

    def test_function(self):
        for function in test_cases:
            with self.subTest(function=function.__name__):
                self.assertCompiles(function)


if __name__ == '__main__':
    unittest.main()
