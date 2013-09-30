TermPy
======

TermPy provides an interface and utilities for the manipulation of terms
including the following

An non-intrusive interface for creating, and accessing operators and children
of terms.  This interface operates on `tuples` and `dicts` by default but can
be easily extended to arbitrary Python objects by implementing a set of methods
or through relatively safe monkey patching.


Dependencies
------------

Python 2.5, 2.6, or 2.7


Install
-------

With `pip` or `easy_install`

    pip install termpy

From source

    git clone git@github.com:logpy/termpy.git
    cd termpy
    python setup.py install

Run tests with nose

    nosetests --with-doctest

TermPy is pure Python

Author
------

[Matthew Rocklin](http://matthewrocklin.com)

License
-------

New BSD license. See LICENSE.txt
