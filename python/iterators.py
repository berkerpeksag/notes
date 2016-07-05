"""
The __iter__() method is called whenever someone calls iter(fib).

After performing beginning-of-iteration initialization, the
__iter__() method can return any object that implements a __next__()
method.

In this case (and in most cases), __iter__() simply returns self,
since this class implements its own __next__() method.

The "magic" in for loops
------------------------

The for loop calls Fib(1000), as shown. This returns an instance
of the Fib class. Call this fib_inst.

Secretly, the for loop calls iter(fib_inst), which returns an
iterator object. Call this fib_iter.

In this case, fib_iter == fib_inst, because the __iter__()
method returns self, but the for loop doesn’t know  about that.

To "loop through" the iterator, the for loop calls next(fib_iter),
which calls the __next__() method on the fib_iter object, which
does the next-Fibonacci-number calculations and returns a value.

The for loop takes this value and assigns it to n, then executes
the body of the for loop for that value of n.

How does the for loop know when to stop? When next(fib_iter)
raises a StopIteration exception, the for loop will swallow the
exception and gracefully exit.

Reference: http://www.diveintopython3.net/iterators.html
"""


class Fib:

    def __init__(self, max):
        self.max = max

    def __iter__(self):
        self.a = 0
        self.b = 1
        return self

    def __next__(self):
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib

if __name__ == '__main__':
    for n in Fib(1000):
        print(n, end=' ')
    print()
