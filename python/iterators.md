# Iterators and iterables

Iterators are objects that are implement *both* `__iter__` and `__next__`
methods.

```py
class Iterable:
    def __init__(self):
        self.counter = 0

    def __iter__(self):
        return Iterator(self)


class Iterator:
    def __init__(self, obj):
        self.obj = obj

    def __next__(self):
        if self.obj.counter >= 5:
            raise StopIteration
        self.obj.counter += 1
        return self.obj.counter

    def __iter__(self):
        return self


myiterable = Iterable()

for e in myiterable:
    print(e)
```
