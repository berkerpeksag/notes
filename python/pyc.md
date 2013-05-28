When writing a `.pyc` file, we use the following strategy:
- open the file for writing
- write a dummy header (four null bytes)
- write the `.py` file's mtime
- write the marshalled code object
- replace the dummy header with the correct magic word

Even `py_compile.py` (used by `compileall.py`) uses this strategy.

When reading a `.pyc` file, we ignore it when the magic word isn't there
(or when the mtime doesn't match that of the `.py` file exactly), and
then we will write it back like described above.

**Note:** In importlib we write the entire file to a temp file and then
to an atomic rename. py_compile as of Python 3.4 now just uses importlib
directly, so it matches its semantics.

http://mail.python.org/pipermail/python-dev/2013-May/126268.html
