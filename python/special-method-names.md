# Special Method Names

|     | Python code | Internal call |
| --- | --- | --- |
| to get a computed attribute (unconditionally) | `x.my_property` | `x.__getattribute__('my_property')` |
| to get a computed attribute (fallback) | `x.my_property` | `x.__getattr__('my_property')` |
| to set an attribute | `x.my_property = value` | `x.__setattr__('my_property', value)` |
| to get a property’s value | `x.color` | `type(x).__dict__['color'].__get__(x, type(x))` |
| to set a property’s value | `x.color = 'PapayaWhip'` | `type(x).__dict__['color'].__set__(x, 'PapayaWhip')` |
| to control whether an object is an instance of your class | `isinstance(x, MyClass)` | `MyClass.__instancecheck__(x)` |
| to control whether a class is a subclass of your class | `issubclass(C, MyClass)` | `MyClass.__subclasscheck__(C)` |

* If your class defines a `__getattribute__()` method, Python will call it on
  every reference to any attribute or method name (except special method
  names, since that would cause an unpleasant infinite loop).
* If your class defines a `__getattr__()` method, Python will call it only
  after looking for the attribute in all the normal places. If an instance `x`
  defines an attribute `color`, `x.color` will not call
  `x.__getattr__('color')`; it will simply return the already-defined value of
  `x.color`.

**Note:** The `__dir__()` method is useful if you define a `__getattr__()` or
`__getattribute__()` method. Normally, calling `dir(x)` would only list the
regular attributes and methods. If your `__getattr__()` method handles a
`color` attribute dynamically, `dir(x)` would not list `color` as one of the
available attributes.

Reference: http://www.diveintopython3.net/special-method-names.html
