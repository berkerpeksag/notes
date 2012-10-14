## Code object

* Byte code produced by the compiler
* Plus other data needed to execute it
* Immutable

  ```py
  >>> code_obj = func.func_code
  >>> code_obj.co_name
  >>> code_obj.co_name = 'spam'  # it won't work
  ```

## `.pyc` file

* `.pyc` files are simply marshal'ed code objects
* 4 bytes: version-specific magic number
* 4 bytes: modification timestamp
* Rest: a code object for the entire module

## Function object

* Mutable in-memory representation

  ```py
  >>> def my_fun(x=12):
  ...     y = x * 3
  ...     return y
  ...
  >>> my_fun.func_code
  <code object my_fun at 000000000217A918, file "<stdin>", line 1>
  >>> my_fun.func_name
  'my_fun'
  >>> my_fun.func_defaults
  (12,)
  >>> my_fun.func_defaults = (27,)
  >>> my_fun()
  81
  ```
* One attribute is the immutable code object.
* Also: method objects, generators, etc.

## Execution model

### Compiler

```
Source -> AST -> Code objects -> Byte code
```

### Interpreter

```
Byte code -> Python objects -> Execution -> Stack frames
```
