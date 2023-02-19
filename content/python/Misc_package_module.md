---
title: "Misc_package_module"
date: 2023-02-18T17:22:55-05:00
draft: false
tags: ["coding","python","course"]
---

# Related imports

Can be used for less typing, and mobilibility. Not recommanded
```python
from .module_name import some_function
from ..module_in_parent_folder import another_fuction
```

# List attribute names imported via from module import *

Without a init py file under compressed folder import star will get every modules 

```python3
>>> from reader.compressed import * # not recommanded way to import
>>> locals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'gzipped': <module 'reader.compressed.gzipped' from '/home/vma/decmaxn.github.io/py_pkg/reader/compressed/gzipped.py'>, 'bzipped': <module 'reader.compressed.bzipped' from '/home/vma/decmaxn.github.io/py_pkg/reader/compressed/bzipped.py'>}
>>> bzipped 
<module 'reader.compressed.bzipped' from '/home/vma/decmaxn.github.io/py_pkg/reader/compressed/bzipped.py'>
>>> gzipped
<module 'reader.compressed.gzipped' from '/home/vma/decmaxn.github.io/py_pkg/reader/compressed/gzipped.py'>
>>> 
```
With this ```py_pkg/reader/compressed/__init__.py ```, we show only those functions imported to this compressed subpackage, not the modules.

```python3
from reader.compressed.bzipped import opener as bz2_opener
from reader.compressed.gzipped import opener as gzip_opener

__all__ = ['bz2_opener','gzip_opener']
```

Only functions inside \_\_all__ list are imported by import star. 

```python3
>>> locals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>}
>>> from reader.compressed import *
>>> locals()
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': None, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, 'bz2_opener': <function open at 0x7fb534c023a0>, 'gzip_opener': <function open at 0x7fb534b34550>}
```
Modules bzipped ang gzipped are just hidden, they call still be imported, just not with import star.

# Namespace Packages

special cases when a package is not a folder with init py files, but spread across multiple folders. They are directories with same name located in different paths, which are all put in sys.path. 

When you importing a foo package, python looks for:
1. foo directory with init py file under it, import if found
2. foo.py file, import if found
3. all foo folders in sys.path, import all founded.

```python
$ mkdir -p path1/foo
$ mkdir -p path2/foo
$ touch path1/foo/m1.py
$ touch path2/foo/m2.py
>>> import sys
>>> sys.path.extend(['path1','path2','path3']) # more pathes in sys.path
>>> import foo 
>>> foo.__path__  # 2 folders imported for the same package
_NamespacePath(['/home/vma/decmaxn.github.io/path1/foo', '/home/vma/decmaxn.github.io/path2/foo'])
>>> import foo.m1 
>>> foo.m1.__file__ # python find right folder where to import the m1 module
'/home/vma/decmaxn.github.io/path1/foo/m1.py'
>>> import foo.m2
>>> foo.m2.__file__
'/home/vma/decmaxn.github.io/path2/foo/m2.py'
```

It's used to splitting large packages into multiple parts. 
There is no init py file, to avoid complex init ordoring problems.

## Executable directory

A directory can be executed if there is a \_\_main__.py file.

```bash
$  ls py_pkg/reader/
__init__.py  __pycache__  compressed  rdm.py
$ python3 py_pkg/reader
/usr/bin/python3: can't find '__main__' module in 'py_pkg/reader/compressed/'
```
Note the readeer.py file has been renamed to rdm.py to avoid a circular import issue casued by the package and module sharing the same name.

After created ``py_pkg/reader/__main__.py``` like this:

```python
import sys
from reader.rdm import Reader

r = Reader(sys.argv[1])
try:
    print(r.read())
finally:
    r.close()
```
It works like a charm.

```bash
$ python3 py_pkg/reader test.bz2
Content compressed by bz2
$ python3 py_pkg/reader test.gzip
Content compressed by gzip
$ python3 py_pkg/reader LICENSE.md
Copyright (c) 2023 Victor Ma ...
```