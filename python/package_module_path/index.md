# Package_module_path



# Searching path of packages and modules

```python
>>> import sys
>>> for i in range(len(sys.path)):
...     print(sys.path[i])
... 

/usr/lib/python38.zip
/usr/lib/python3.8
/usr/lib/python3.8/lib-dynload
/home/vma/.local/lib/python3.8/site-packages
/usr/local/lib/python3.8/dist-packages
/usr/lib/python3/dist-packages
```

# Package and Modules

There is this example package from one entries of searching path.

```bash
$  find /usr -name urllib -type d
/usr/lib/python3.8/urllib
```
Packages are directories in sys.path contain other packages/modules, at least a module as \_\_init__.py.

```python
>>> import urllib 
>>> type(urllib) # this is shown as module
<class 'module'>
>>> import urllib.request # this is also shown as module
>>> type(urllib.request)
<class 'module'>
>>> urllib.__path__  # but urllib is actually a package(folder)
['/usr/lib/python3.8/urllib']  # Same location you found from bash above
>>> urllib.reqeust.__path__
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'urllib' has no attribute 'reqeust'
```
# import a module from some where
Create yourself a module

```bash
$ cat not_path/test_module.py 
def found():
    print("Python found this module")
```

Directly modify sys.path to add a path can load this module

```python
>>> import test_module
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'test_module'
>>> import sys
>>> sys.path.append('not_path')
>>> import test_module
>>> test_module.found()
Python found this module
>>> [p for p in sys.path if 'not_path' in p]
['not_path']
```

another way is $PYTHONPATH environment variable will be added to sys.path when python is started

```bash
$ echo $PYTHONPATH
$ export PYTHONPATH=not_path
$ echo $PYTHONPATH
not_path
$ python3
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sys
>>> [p for p in sys.path if 'not_path' in p]
['/home/vma/decmaxn.github.io/not_path']
>>> import test_module
>>> test_module.found() # Use a method of the module to prove module is imported properly
Python found this module
```

# Import a package and module

Let me move the module inside package

```bash
$ mv not_path/test_module.py not_path/package/
```
You have to import the module with a package name now, and you have to call it with the package name. 

```python
>>> import package # Import package alone
>>> package.test_module.found() # won't includes it's modules yet
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'package' has no attribute 'test_module'
>>> import package.test_module # specifically import the module ...
>>> package.test_module.found()  # makes it work
Python found this module
>>> test_module.found() # Can't call module name alone yet
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'test_module' is not defined
>>> 
```
Note importing the package won't include it's modules above.

Import package will run \_\_init__.py under it.

```bash
$ echo "print('package is being imported')" > not_path/package/__init__.py
$ ls not_path/package/
__init__.py
```
\_\_init__.py is run when package is imported

```python
>>> import package
package is being imported  
>>> package.__file__
'/home/vma/decmaxn.github.io/not_path/package/__init__.py'
```

This can be used to avoid importing each modules in the package one by one

```bash
$ echo "from package.test_module import found as fd" >> not_path/package/__init__.py 
```
Let's import the method of a moudle directly, bypassing the module, to the package.

```python
>>> import package
package is being imported
>>> package.fd() # The as name of found method is attached directly to the package
Python found this module
```
This way can be used to simplify long pathes of package/module...
