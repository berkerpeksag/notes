## "Attribute lookup" or "dot notation" in a dictionary

```py
class Dict(dict):
    def __getattr__(self, key):
        return self.get(key)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
```
