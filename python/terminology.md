# Terminolohy

## Packaging

* **module:** The basic unit of code reusability in Python: a block of code
imported by some other code. Three types of modules are important to us here:
pure Python modules, extension modules and packages.

* **pure Python module:** A module written in Python and contained in a single
`.py` file (and possibly associated `.pyc` and/or `.pyo` files). Sometimes
referred to as a "pure module."

* **extension module:** A module written in the low-level language of the Python
implementation: C/C++ for Python, Java for Jython. Typically contained in a
single dynamically loaded pre-compiled file, e.g. a shared object (`.so`) file
for Python extensions on Unix, a DLL (given the `.pyd` extension) for Python
extensions on Windows, or a Java class file for Jython extensions. Note that
currently Distutils only handles C/C++ extensions for Python.

* **package:** A module that contains other modules, typically contained in a
directory of the filesystem and distinguished from other directories by the
presence of a file `__init__.py`.

* **root package:** The root of the hierarchy of packages. (This isn't really a
package, since it doesn't have an `__init__.py` file. But... we have to call it
something, right?) The vast majority of the standard library is in the root
package, as are many small standalone third-party modules that don't belong to a
larger module collection. Unlike regular packages, modules in the root package
can be found in many directories: in fact, every directory listed in `sys.path`
contributes modules to the root package.

[Source](http://docs.python.org/dev/packaging/introduction.html#general-python-terminology)
