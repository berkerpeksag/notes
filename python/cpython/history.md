## Python 2.0

From Marc-Andre Lemburg on python-ideas:

Python 2.0 was called 2.0 because the BeOpen marketing
department thought it was good idea, not because there were major
incompatible changes going into that release.

Porting code from Python 1.5.2 to 2.0 was relatively straight forward
and not much different from other minor releases.

The first ever major backwards incompatibility release switch we
had in Python after the great renaming of the C APIs between
Python 1.1 and 1.2 (which was only visible to C extensions and
relatively easy to fix using a compatibility header file),
was the transition from Python 2.x to Python 3.x.

IMO, the only reason to do this again would be the removal of
the GIL, but only if there's absolutely no other way to get
around such breakage.

[Reference](https://mail.python.org/pipermail/python-ideas/2017-November/047677.html)
